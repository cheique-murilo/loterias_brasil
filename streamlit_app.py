# streamlit_app.py
import streamlit as st
import pandas as pd
import os
import base64
from collections import Counter
from itertools import combinations
import matplotlib.pyplot as plt

st.set_page_config(page_title="Loterias de Portugal", page_icon="🎰", layout="wide")

# CSS bonito (mantido do seu original)
st.markdown("""
<style>
    .big-font { font-size: 50px !important; font-weight: bold; color: #1E90FF; text-align: center; }
    .card { padding: 20px; border-radius: 15px; background: linear-gradient(90deg, #1E90FF, #00BFFF); color: white; text-align: center; box-shadow: 5px 5px 15px rgba(0,0,0,0.3); margin: 10px; }
    h3 { font-size: 22px !important; }
</style>
""", unsafe_allow_html=True)

def img_to_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# CARREGAMENTO SIMPLES E FUNCIONAL (testado com seu Excel)
@st.cache_data
def carregar_dados():
    df = pd.read_excel('dados_loterias.xlsx')
    sorteios = []
    for _, row in df.iterrows():
        try:
            data_raw = row['data']
            data_str = data_raw.strftime('%d/%m/%Y') if hasattr(data_raw, 'strftime') else str(data_raw)

            nome_raw = str(row['loteria']).strip().lower()
            if 'totoloto' in nome_raw:
                nome = "Totoloto"
                comp_label = "Número da Sorte"
            elif 'eurodreams' in nome_raw:
                nome = "Eurodreams"
                comp_label = "Número do Sonho"
            elif 'euromilhoes' in nome_raw or 'euromilhões' in nome_raw:
                nome = "Euromilhões"
                comp_label = "Estrelas"
            else:
                continue

            principais = [int(x.strip()) for x in str(row['numeros_sorteados']).split(',') if x.strip().isdigit()]
            complementares = [int(x.strip()) for x in str(row['numeros_complementares']).split(',') if x.strip().isdigit()]

            sorteios.append({
                'data': data_str,
                'sorteio_id': str(row['sorteio']),
                'loteria': nome,
                'comp_label': comp_label,
                'principais': sorted(principais),
                'complementares': sorted(complementares),
                'acumulou': str(row['acumulou']).lower() == 'sim',
                'jackpot': int(row['jackpot']) if pd.notna(row['jackpot']) else 0,
                'vencedores': int(row['vencedores']) if pd.notna(row['vencedores']) else 0
            })
        except:
            continue
    return sorteios

sorteios = carregar_dados()

<<<<<<< Updated upstream
# Função para quadro de sorteios recentes (coluna dinâmica e display baseado na loteria)
def quadro_sorteios(sorteios_filtrados, nome_loteria):
    if not sorteios_filtrados:
        st.empty()
        return
    
    # Helper pra parsear complementares
    def parse_complementares(comps, loteria_nome):
        nome_lower = loteria_nome.lower()
        parsed = []
        if isinstance(comps, str):
            if ',' in comps and "euromilhoes" in nome_lower:  # Sem acento: match exato
                # Split Euromilhões: "2, 5" -> [2, 5]
                nums = [x.strip() for x in comps.split(',')]
                parsed = [int(num) for num in nums if num.isdigit() and num != '0']  # Ignora 0 e não-dígitos
            else:
                # Pros outros: string única como "3" -> [3]
                num = comps.strip()
                if num.isdigit() and num != '0':  # Evita mostrar 0 default
                    parsed = [int(num)]
                # Se "0" ou vazio, parsed = [] -> "-"
        elif isinstance(comps, list):
            # Se já lista
            if "euromilhoes" in nome_lower:
                parsed = [int(x) for x in comps if isinstance(x, (int, str)) and str(x).isdigit() and str(x) != '0']
            else:
                parsed = [int(comps[0])] if comps and isinstance(comps[0], (int, str)) and str(comps[0]).isdigit() and str(comps[0]) != '0' else []
        
        # Debug temporário (remove depois de testar):
        # st.write(f"🔍 Debug {loteria_nome} raw: '{comps}' | Parseado: {parsed}")
        return parsed if parsed else []
    
    # Título da coluna
    nome_lower = nome_loteria.lower()
    if "totoloto" in nome_lower:
        col_comp = "Número sorteado"
    elif "eurodreams" in nome_lower:
        col_comp = "Número sonho"
    else:  # Euromilhões
        col_comp = "Estrelas"
    
    # Cria o DF
    df_sorteios = pd.DataFrame([
        {
            'Data': s.data.strftime('%d/%m/%Y'),
            'Sorteio': s.sorteio_id,
            'Números Sorteados': ', '.join(map(str, s.numeros_sorteados)),
            col_comp: ', '.join(map(str, parse_complementares(s.numeros_complementares, nome_loteria))) if parse_complementares(s.numeros_complementares, nome_loteria) else '-',  # Junta ou "-"
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
=======
if not sorteios:
    st.error("Nenhum sorteio carregado. Verifique o Excel.")
    st.stop()

st.success(f"Carregados {len(sorteios)} sorteios com sucesso!")
>>>>>>> Stashed changes

# Logo + título
col1, col2 = st.columns([1, 5])
with col1:
<<<<<<< Updated upstream
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
=======
    logo = img_to_base64("imagens/jogossantacasa.PNG")
    if logo:
        st.image(f"data:image/png;base64,{logo}", width=150)
with col2:
    st.markdown("<p class='big-font'>Loterias de Portugal</p>", unsafe_allow_html=True)

# Cards
loterias_dict = {}
for s in sorteios:
    nome = s['loteria']
    loterias_dict.setdefault(nome, []).append(s)

cols = st.columns(3)
cards = [
    ("Totoloto", "totoloto.PNG"),
    ("Eurodreams", "eurodreams.PNG"),
    ("Euromilhões", "euromilhoes.PNG")
]

for col, (nome, img_file) in zip(cols, cards):
    with col:
        img_b64 = img_to_base64(f"imagens/{img_file}")
        card_html = f"""
        <div class="card">
            <h3>🍀 {nome}</h3>
            {f'<img src="data:image/png;base64,{img_b64}" style="max-height: 150px;">' if img_b64 else ''}
            <p style="margin-top: 20px;">
                <b>{len(loterias_dict.get(nome, []))} sorteios</b>
            </p>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        if st.button(f"Explorar {nome}", key=nome, use_container_width=True):
            st.session_state.selected = nome
            st.rerun()

if "selected" in st.session_state:
    nome = st.session_state.selected
    dados = loterias_dict[nome]
    comp_label = dados[0]['comp_label'] if dados else "Complementar"
>>>>>>> Stashed changes

    st.header(f"📊 {nome}")

    col1, col2 = st.columns(2)
    col1.metric("Total de Sorteios", len(dados))
    col2.metric("Acumulações", sum(1 for s in dados if s['acumulou']))

    # Últimos 5 sorteios
    st.subheader("Últimos 5 sorteios")
    ultimos = dados[-5:]
    df_ultimos = pd.DataFrame([{
        'Data': s['data'],
        'Principais': ', '.join(map(str, s['principais'])),
        comp_label: ', '.join(map(str, s['complementares'])),
        'Acumulou': 'Sim' if s['acumulou'] else 'Não',
        'Jackpot': f"€{s['jackpot']:,}"
    } for s in ultimos])
    st.dataframe(df_ultimos, hide_index=True, width='stretch')

    # Números mais/menos saíram
    todos_princ = [n for s in dados for n in s['principais']]
    todos_comp = [n for s in dados for n in s['complementares']]
    freq_princ = Counter(todos_princ)
    freq_comp = Counter(todos_comp)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Principais - Mais saíram**")
        df = pd.DataFrame(freq_princ.most_common(10), columns=["Número", "Vezes"])
        st.dataframe(df, hide_index=True, width='stretch')
    with col2:
        st.markdown("**Principais - Menos saíram**")
        df = pd.DataFrame(sorted(freq_princ.items(), key=lambda x: x[1])[:10], columns=["Número", "Vezes"])
        st.dataframe(df, hide_index=True, width='stretch')

    # Tabs para Duplas, Trios, Quadras
    st.subheader("Combinações Mais Repetidas")
    tab1, tab2, tab3 = st.tabs(["Duplas", "Trios", "Quadras"])

    def repetidas(tamanho):
        c = Counter()
        for s in dados:
            for combo in combinations(sorted(s['principais']), tamanho):
                c[combo] += 1
        return [(str(k), v) for k, v in c.most_common(10) if v >= 2]

    with tab1:
        df = pd.DataFrame(repetidas(2), columns=["Dupla", "Vezes"])
        st.dataframe(df if not df.empty else "Nenhuma", hide_index=True, width='stretch')
    with tab2:
        df = pd.DataFrame(repetidas(3), columns=["Trio", "Vezes"])
        st.dataframe(df if not df.empty else "Nenhuma", hide_index=True, width='stretch')
    with tab3:
        df = pd.DataFrame(repetidas(4), columns=["Quadra", "Vezes"])
        st.dataframe(df if not df.empty else "Nenhuma", hide_index=True, width='stretch')

    # Sequências consecutivas
    st.subheader("🔢 Sequências Consecutivas")
    seqs = []
    for s in dados:
        nums = sorted(s['principais'])
        i = 0
        while i < len(nums):
            start = i
            while i + 1 < len(nums) and nums[i + 1] == nums[i] + 1:
                i += 1
            if i - start + 1 >= 3:
                seqs.append((s['data'], ', '.join(map(str, nums[start:i+1]))))
            i += 1
    if seqs:
        df_seq = pd.DataFrame(seqs, columns=["Data", "Sequência"])
        st.dataframe(df_seq, hide_index=True, width='stretch')
    else:
        st.info("Nenhuma sequência consecutiva encontrada.")

    # Gráficos
    st.subheader("📈 Gráficos")

    col1, col2 = st.columns(2)
    with col1:
        # Evolução do jackpot
        df_jack = pd.DataFrame([{
            'data': pd.to_datetime(s['data'], format='%d/%m/%Y'),
            'jackpot': s['jackpot']
        } for s in dados if s['jackpot'] > 0])
        if not df_jack.empty:
            fig, ax = plt.subplots()
            ax.plot(df_jack['data'], df_jack['jackpot'], marker='o')
            ax.set_title('Evolução do Jackpot')
            ax.set_ylabel('Jackpot (€)')
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.info("Sem dados de jackpot")

    with col2:
        # Ranking de países (se houver dados)
        paises = Counter()
        for s in dados:
            if s['vencedores'] > 0 and s['jackpot'] > 0:
                for p in s.get('paises', []):
                    paises[p] += s['jackpot']
        if paises:
            df_p = pd.DataFrame(paises.most_common(5), columns=["País", "Total (€)"])
            fig, ax = plt.subplots()
            ax.barh(df_p['País'], df_p['Total (€)'])
            ax.set_title('Ranking de Premiações por País')
            st.pyplot(fig)
        else:
            st.info("Sem dados de países")

    # Curiosidades
    st.subheader("💡 Curiosidades")
    if todos_princ:
        mais = freq_princ.most_common(1)[0]
        curiosidades = [
            f"O número **{mais[0]}** é o mais sorteado: **{mais[1]} vezes**!",
            f"Acumulou **{sum(1 for s in dados if s['acumulou'])} vezes**.",
            f"Jackpot ganho por 1 pessoa: **{sum(1 for s in dados if s['vencedores'] == 1 and not s['acumulou'])} vezes**",
            f"Jackpot dividido: **{sum(1 for s in dados if s['vencedores'] > 1 and not s['acumulou'])} vezes**"
        ]
        for c in curiosidades:
            st.write(c)

<<<<<<< Updated upstream
    # Botão para voltar
    if st.button("🔙 Voltar à página principal"):
        del st.session_state.selected_loteria
        st.rerun()

else:
    st.info("Clique em uma loteria para ver as estatísticas detalhadas.")
    st.markdown("**Filtros disponíveis**: Data range e sorteio específico na sidebar.")
=======
    if st.button("🔙 Voltar"):
        del st.session_state.selected
        st.rerun()
>>>>>>> Stashed changes
