import streamlit as st
import sys
import os
import pandas as pd
from datetime import date
from typing import Dict
import altair as alt
import matplotlib.pyplot as plt  # Adicionado para o gráfico customizado
import base64  # NOVO: Para embed de imagens locais no HTML

# Adiciona path para imports do projeto
sys.path.append('.')

from servicos.carregar_dados import FonteDados
from servicos.validador import Validador
from servicos.estatistica import Estatistica
from servicos.curiosidade import Curiosidade
from visualizacao.graficos import Graficos

st.set_page_config(page_title="Loterias de Portugal", page_icon="🎰", layout="wide")

# CSS simples para subheaders (font-size 20px) - sem mexer em imagens
st.markdown("""
<style>
h3 { font-size: 20px !important; }
</style>
""", unsafe_allow_html=True)

alt.data_transformers.disable_max_rows()

@st.cache_data
def carregar_dados_cache():
    fonte = FonteDados('dados_loterias.xlsx')
    loterias = fonte.carregar_dados()
    Validador.validar_loterias(loterias)
    return loterias

loterias = carregar_dados_cache()

# Sidebar para filtros
st.sidebar.title("🔍 Filtros")
data_inicio = st.sidebar.date_input("Data inicial", value=date(2025, 1, 1))
data_fim = st.sidebar.date_input("Data final", value=date(2025, 12, 31))
sorteio_filtro = st.sidebar.selectbox("Filtrar por sorteio", options=['Todos'] + [s.sorteio_id for lot in loterias.values() for s in lot.sorteios], index=0)

# Função para filtrar
def filtrar_sorteios(loteria, data_inicio, data_fim, sorteio_filtro):
    if sorteio_filtro == 'Todos':
        return [s for s in loteria.sorteios if data_inicio <= s.data.date() <= data_fim]
    return [s for s in loteria.sorteios if data_inicio <= s.data.date() <= data_fim and s.sorteio_id == sorteio_filtro]

# Fallback dummy
class DummyLoteria:
    def __init__(self, nome):
        self.nome = nome
        self.sorteios = []
    def get_todos_numeros(self, tipo):
        return []
    def validar_sorteio(self, sorteio):
        return True
    
# NOVA FUNÇÃO: Converte imagem local para base64 para embed no HTML
@st.cache_data
def img_to_base64(image_path):
    if not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Função para quadro de sorteios recentes (coluna dinâmica e display baseado na loteria)
def quadro_sorteios(sorteios_filtrados, nome_loteria):
    if not sorteios_filtrados:
        st.empty()
        return
    col_comp = "Número sorte" if "totoloto" in nome_loteria.lower() else "Número sonho" if "eurodreams" in nome_loteria.lower() else "Estrelas"
    
    df_sorteios = pd.DataFrame([
        {
            'Data': s.data.strftime('%d/%m/%Y'),
            'Sorteio': s.sorteio_id,
            'Números Sorteados': ', '.join(map(str, s.numeros_sorteados)),
            col_comp: ', '.join(map(str, s.numeros_complementares)) if "euromilhoes" in nome_loteria.lower() else (str(s.numeros_complementares[1]) if s.numeros_complementares else '-'),
            'Acumulou': 'Sim' if s.acumulou else 'Não',
            'Jackpot (€)': f"{s.premio:,}" if s.premio else f"{s.jackpot:,}",
            'Países': ', '.join(s.paises) if s.paises else '-',
            'Vencedores': s.vencedores
        }
        for s in sorteios_filtrados[-5:]
    ])
    st.subheader("📋 Últimos 5 sorteios")
    st.dataframe(df_sorteios, use_container_width=True, hide_index=True)

# Função para ranking países
def ranking_paises_loteria(loteria):
    contagem_paises = {}
    for s in loteria.sorteios:
        if s.premio:  # Só conta se houve prêmio
            for pais in s.paises:
                contagem_paises[pais] = contagem_paises.get(pais, 0) + 1  # +1 por ocorrência
    if contagem_paises:
        df_paises = pd.DataFrame(list(contagem_paises.items()), columns=['País', 'Contagem'])
        df_paises = df_paises.sort_values('Contagem', ascending=False)
        base = alt.Chart(df_paises).mark_bar(color='green').encode(
            x=alt.X('Contagem', scale=alt.Scale(domainMin=0),
                    axis=alt.Axis(title=None, labels=False, ticks=False)),  # Sem título, labels e ticks no X
            y=alt.Y('País', sort='-x',
                    axis=alt.Axis(title=None))  # Sem título no Y, mas labels visíveis
        ).properties(width=300, height=200)
        
        text = alt.Chart(df_paises).mark_text(align='center', baseline='middle').encode(
            x=alt.X('Contagem', scale=alt.Scale(domainMin=0)),
            y=alt.Y('País', sort='-x'),
            text=alt.Text('Contagem', format='.0f')
        )
        
        chart_paises = (base + text).configure_axis(grid=False)  # Remove todas as grades
        st.altair_chart(chart_paises, use_container_width=True)
    else:
        st.empty()

# Função para streak max
def calcular_streak_max_acum(loteria):
    if not loteria.sorteios:
        return 0
    max_streak = 0
    current_streak = 0
    for s in sorted(loteria.sorteios, key=lambda x: x.data):
        if s.acumulou:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
    return max_streak

# Página Principal
# Logo ao lado do título
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    if os.path.exists("imagens/jogossantacasa.PNG"):
        st.image("imagens/jogossantacasa.PNG", width=150)
with col_titulo:
    st.title("Loterias de Portugal")

st.markdown("### Insights estatísticos para as loterias de Portugal")
#st.markdown("Clique em uma loteria para explorar informações estatísticas")

# 3 Cards com Imagens Locais
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<h3>🍀 Totoloto</h3>", unsafe_allow_html=True)
    base64_totoloto = img_to_base64("imagens/totoloto.PNG")
    if base64_totoloto:
        st.markdown(f"""
        <div style="height: 150px; display: flex; justify-content: center; align-items: center; margin-bottom: 10px; border: 1px solid #eee; border-radius: 8px;">
            <img src="data:image/png;base64,{base64_totoloto}" alt="Totoloto" style="max-height: 150px; width: auto; object-fit: contain;">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="height: 150px; display: flex; justify-content: center; align-items: center; margin-bottom: 10px; border: 1px solid #eee; border-radius: 8px; background-color: #f0f0f0;">
            <span>Imagem Totoloto não encontrada</span>
        </div>
        """, unsafe_allow_html=True)
    if st.button("Explorar Totoloto", key="totoloto", use_container_width=True):
        st.session_state.selected_loteria = 'Totoloto'

with col2:
    st.markdown("<h3>🍀 Eurodreams</h3>", unsafe_allow_html=True)
    base64_eurodreams = img_to_base64("imagens/eurodreams.PNG")
    if base64_eurodreams:
        st.markdown(f"""
        <div style="height: 150px; display: flex; justify-content: center; align-items: center; margin-bottom: 10px; border: 1px solid #eee; border-radius: 8px;">
            <img src="data:image/png;base64,{base64_eurodreams}" alt="Eurodreams" style="max-height: 150px; width: auto; object-fit: contain;">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="height: 150px; display: flex; justify-content: center; align-items: center; margin-bottom: 10px; border: 1px solid #eee; border-radius: 8px; background-color: #f0f0f0;">
            <span>Imagem Eurodreams não encontrada</span>
        </div>
        """, unsafe_allow_html=True)
    if st.button("Explorar Eurodreams", key="eurodreams", use_container_width=True):
        st.session_state.selected_loteria = 'Eurodreams'

with col3:
    st.markdown("<h3>🍀 Euromilhões</h3>", unsafe_allow_html=True)
    base64_euromilhoes = img_to_base64("imagens/euromilhoes.PNG")
    if base64_euromilhoes:
        st.markdown(f"""
        <div style="height: 150px; display: flex; justify-content: center; align-items: center; margin-bottom: 10px; border: 1px solid #eee; border-radius: 8px;">
            <img src="data:image/png;base64,{base64_euromilhoes}" alt="Euromilhões" style="max-height: 150px; width: auto; object-fit: contain;">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="height: 150px; display: flex; justify-content: center; align-items: center; margin-bottom: 10px; border: 1px solid #eee; border-radius: 8px; background-color: #f0f0f0;">
            <span>Imagem Euromilhões não encontrada</span>
        </div>
        """, unsafe_allow_html=True)
    if st.button("Explorar Euromilhões", key="euromilhoes", use_container_width=True):
        st.session_state.selected_loteria = 'Euromilhões'

# Se loteria selecionada, mostra seção aprimorada
if 'selected_loteria' in st.session_state:
    nome = st.session_state.selected_loteria
    loteria = loterias.get(nome, DummyLoteria(nome))
    sorteios_filtrados = filtrar_sorteios(loteria, data_inicio, data_fim, sorteio_filtro)
    
    st.header(f"📊 {nome}")
    st.info(f"**{len(sorteios_filtrados)} sorteios filtrados** ({data_inicio} a {data_fim}). Use a sidebar para ajustar filtros.")
    
    # Container para overview
    with st.container():
        col1, col2 = st.columns(2)
        total_premios = sum(s.premio or 0 for s in loteria.sorteios)
        col1.metric("Total Premiações (€)", f"{total_premios:,}")
        col2.metric("Sorteios Totais", len(loteria.sorteios))
    
    # Quadro de sorteios recentes (coluna dinâmica)
    quadro_sorteios(sorteios_filtrados, nome)
    
    # Stats principais
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3 style='font-size: 20px;'>Números mais 😎/menos saíram 🤔</h3>", unsafe_allow_html=True)
        # Top 5 fixo, sem slider
        top_k = 5
        mais, menos = Estatistica.numeros_mais_menos_sairam(loteria, tipo='principais', top_k=top_k)
    
        # Tabs para filtro visual (como duplas/trios/quadras)
        tab_mais, tab_menos = st.tabs(["🔼 Mais Saíram", "🔻 Menos Saíram"])
        
        with tab_mais:
            if mais:
                df_mais = pd.DataFrame(mais, columns=["Número", "Vezes"])
                st.dataframe(df_mais, use_container_width=True, hide_index=True)
            else:
                st.info("Sem dados para mais saídos.")
        
        with tab_menos:
            if menos:
                df_menos = pd.DataFrame(menos, columns=["Número", "Vezes"])
                st.dataframe(df_menos, use_container_width=True, hide_index=True)
            else:
                st.info("Sem dados para menos saídos.")
    
    with col2:
        st.markdown("<h3 style='font-size: 20px;'>Sequências mais comuns 😮</h3>", unsafe_allow_html=True)
        # Tabs para duplas, trios, quadras
        tab1, tab2, tab3 = st.tabs(["Duplas", "Trios", "Quadras"])
        with tab1:
            repetidos2 = Estatistica.conjuntos_repetidos(loteria, tamanho=2)
            if repetidos2:
                df2 = pd.DataFrame(repetidos2, columns=["Dupla", "Vezes"])
                st.dataframe(df2[:5], use_container_width=True, hide_index=True)
            else:
                st.info("Sem duplas repetidas.")
        with tab2:
            repetidos3 = Estatistica.conjuntos_repetidos(loteria, tamanho=3)
            if repetidos3:
                df3 = pd.DataFrame(repetidos3, columns=["Trio", "Vezes"])
                st.dataframe(df3[:5], use_container_width=True, hide_index=True)
            else:
                st.info("Sem trios repetidos.")
        with tab3:
            repetidos4 = Estatistica.conjuntos_repetidos(loteria, tamanho=4)
            if repetidos4:
                df4 = pd.DataFrame(repetidos4, columns=["Quadra", "Vezes"])
                st.dataframe(df4[:5], use_container_width=True, hide_index=True)
            else:
                st.info("Sem quadras repetidas.")
    
    # Gráficos
    st.subheader("📈 Gráficos")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Número de premiações por país**")
        ranking_paises_loteria(loteria)
    
    with col2:
        st.write("**Evolução do jackpot**")
        fig_jack = Graficos.grafico_evolucao_jackpot({nome: loteria}, salvar=False)
        st.pyplot(fig_jack)
    
    # Curiosidades
    st.subheader("Curiosidades 📌")
    insights = Curiosidade.gerar_insights(loteria)
    for insight in insights:
        st.write(f"💡 {insight}")
    

    # Botão para voltar
    if st.button("🔙 Voltar à página principal"):
        del st.session_state.selected_loteria
        st.rerun()

else:
    st.info("Clique em uma loteria para ver as estatísticas detalhadas.")
    st.markdown("**Filtros disponíveis**: Data range e sorteio específico na sidebar.")
