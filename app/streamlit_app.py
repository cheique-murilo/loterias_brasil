import os
import sys
from datetime import datetime as dt
import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from servicos.carregar import carregar_dados_loteria
from servicos.normalizar import normalizar_loteria
from modelos.loteria_base import LoteriaBase
from modelos.sorteio import Sorteio
from estatisticas.agregador import calcular_tudo
from visualizacao import graficos

# Tema Altair
@alt.theme.register("tema_azul", enable=True)
def tema_azul():
    return alt.theme.ThemeConfig(
        config={
            "title": {"color": "#0A4ECF"},
            "axis": {"labelColor": "#063A9B", "titleColor": "#063A9B"},
        }
    )

# ------------------------------------------------------------
# Funções auxiliares de interface
# ------------------------------------------------------------

def mostrar_logo_loteria(nome_loteria: str):
    logos = {
        "Mega-Sena": os.path.join(ROOT, "logos", "mega-sena.png"),
        "Quina": os.path.join(ROOT, "logos", "quina.png"),
        "Dupla Sena": os.path.join(ROOT, "logos", "dupla-sena.png"),
        "Lotofácil": os.path.join(ROOT, "logos", "lotofacil.png"),
    }
    caminho = logos.get(nome_loteria)
    if caminho and os.path.exists(caminho):
        st.image(caminho, width=150)

def titulo_principal():
    col1, col2 = st.columns([2, 2])
    with col1:
        st.markdown(
            "<h1 style='margin-top: 10px;'>Análise das Loterias do Brasil</h1>",
            unsafe_allow_html=True,
        )
    with col2:
        logo_path = os.path.join(ROOT, "logos", "caixa.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=150)

def mostrar_data_arquivo_loteria(nome_loteria: str):
    mapa_arquivos = {
        "Mega-Sena": "Mega_Sena.xlsx",
        "Quina": "Quina.xlsx",
        "Dupla Sena": "Dupla_Sena.xlsx",
        "Lotofácil": "Lotofácil.xlsx",
    }
    nome_arquivo = mapa_arquivos.get(nome_loteria)
    if not nome_arquivo:
        return

    caminho = os.path.join(ROOT, "base", nome_arquivo)
    if os.path.exists(caminho):
        timestamp = os.path.getmtime(caminho)
        data_mod = dt.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M")
        st.markdown(
            f"""
            <p style='font-size:14px; color:gray; margin-top:-10px;'>
                📅 <b>Dados da {nome_loteria} atualizados em:</b> {data_mod}
            </p>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<p style='font-size:14px; color:red;'>⚠️ Arquivo de dados da {nome_loteria} não encontrado.</p>",
            unsafe_allow_html=True
        )

# ------------------------------------------------------------
# Configuração da página
# ------------------------------------------------------------

st.set_page_config(
    page_title="Loterias Brasil",
    layout="wide",
    initial_sidebar_state="expanded",
)

titulo_principal()
st.markdown("---")

# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------

st.sidebar.header("Filtros")

nome_lot = st.sidebar.selectbox(
    "Escolha a loteria",
    ["Mega-Sena", "Quina", "Dupla Sena", "Lotofácil"]
)

mostrar_logo_loteria(nome_lot)
mostrar_data_arquivo_loteria(nome_lot)

CONFIG_LOTERIA = {
    "Mega-Sena": {"qtd_principais": 6, "faixa": (1, 60)},
    "Quina": {"qtd_principais": 5, "faixa": (1, 80)},
    "Dupla Sena": {"qtd_principais": 6, "faixa": (1, 50)},
    "Lotofácil": {"qtd_principais": 15, "faixa": (1, 25)},
}

# ------------------------------------------------------------
# Carregamento e normalização
# ------------------------------------------------------------

df_raw = carregar_dados_loteria(nome_lot)
dados_norm = normalizar_loteria(df_raw, nome_lot)
st.sidebar.write("Qtde linhas normalizadas:", len(dados_norm))

if not dados_norm:
    st.error("Nenhum sorteio válido após normalização.")
    st.stop()

config = CONFIG_LOTERIA[nome_lot]
loteria = LoteriaBase(nome_lot, config["qtd_principais"], config["faixa"])

# Criar objetos Sorteio
for d in dados_norm:
    s = Sorteio(
        data=d["data"],
        concurso=d["concurso"],
        principais=d["principais"],
        acumulou=(d["ganhadores_total"] == 0),
        jackpot_fmt=d["jackpot"],
        locais=d["locais"],
        ganhadores=d["ganhadores_total"],
    )
    loteria.adicionar(s)

# ------------------------------------------------------------
# Filtros
# ------------------------------------------------------------

tipo_filtro = st.sidebar.radio("Filtrar por:", ["Data", "Concurso"], horizontal=True)

min_date = min(s.data for s in loteria.sorteios)
max_date = max(s.data for s in loteria.sorteios)
todos_concursos = sorted({s.concurso for s in loteria.sorteios})

if tipo_filtro == "Data":
    d_inicio = st.sidebar.date_input("Data inicial", value=min_date, min_value=min_date, max_value=max_date, format="DD/MM/YYYY")
    d_fim = st.sidebar.date_input("Data final", value=max_date, min_value=min_date, max_value=max_date, format="DD/MM/YYYY")

    if d_inicio > d_fim:
        st.sidebar.error("Data inicial não pode ser maior que a final.")
        st.stop()

    sorteios_filtrados = [s for s in loteria.sorteios if d_inicio <= s.data <= d_fim]
else:
    concurso_escolhido = st.sidebar.selectbox("Escolha o concurso", todos_concursos)
    sorteios_filtrados = [s for s in loteria.sorteios if s.concurso == concurso_escolhido]

if not sorteios_filtrados:
    st.warning("Nenhum sorteio encontrado com o filtro selecionado.")
    st.stop()

sorteios_filtrados = sorted(sorteios_filtrados, key=lambda s: (s.data, s.concurso))

# ------------------------------------------------------------
# Download CSV
# ------------------------------------------------------------

df_base = loteria.to_dataframe()
csv_bytes = df_base.to_csv(index=False).encode("utf-8")

st.sidebar.markdown("### Download do histórico")
st.sidebar.download_button(
    label="📥 Baixar histórico (CSV)",
    data=csv_bytes,
    file_name=f"historico_{nome_lot.lower()}.csv",
    mime="text/csv",
)

# ------------------------------------------------------------
# Estatísticas
# ------------------------------------------------------------

stats = calcular_tudo(sorteios_filtrados, nome_lot)

if not stats:
    st.warning("Não foi possível calcular estatísticas para este filtro.")
    st.stop()

# ------------------------------------------------------------
# Abas
# ------------------------------------------------------------

aba_resumo, aba_repet, aba_seq, aba_quentes = st.tabs(
    ["Resumo 📈", "Combinações 🔍", "Sequências 📌", "Números🔥 e ❄️"]
)

# ------------------------------------------------------------
# Aba Resumo
# ------------------------------------------------------------

with aba_resumo:
    st.subheader("Resumo geral")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total de sorteios", stats["total_sorteios"])
    with col2:
        st.metric("Total de acumulações", stats["total_acumulacoes"])
    with col3:
        st.metric("Streak máximo", stats["max_streak_acumulacoes"])
    with col4:
        st.metric("Total de jackpots pagos", stats["total_jackpots_pagos"])
    with col5:
        valor, concurso, data = stats["maior_jackpot"]
        st.metric("Maior prêmio", valor if valor else "—")
        if valor and data:
            st.caption(f"Concurso {concurso} — {data.strftime('%d/%m/%Y')}")

    st.markdown("### Últimos resultados")

    ultimos = sorted(sorteios_filtrados, key=lambda s: s.data, reverse=True)[:50]

    df_ultimos = pd.DataFrame([
        {
            "Data": s.data.strftime("%d/%m/%Y"),
            "Concurso": s.concurso,
            "Números": ", ".join(map(str, s.principais)),
            "Prêmio": s.jackpot_fmt,
            "Ganhadores": s.ganhadores,
            "Locais": ", ".join(
                f"{loc['cidade']}/{loc['uf']} ({loc['ganhadores']})"
                for loc in s.locais
            ),
        }
        for s in ultimos
    ])

    st.dataframe(df_ultimos, width="stretch", hide_index=True)

    st.markdown("### Frequência dos números")

    freq = stats.get("frequencias", {})
    if freq:
        freq_items = [{"Número": num, "Frequência": freq[num]} for num in freq]
        df_freq = (
            pd.DataFrame(freq_items)
            .sort_values("Frequência", ascending=False)
            .reset_index(drop=True)
        )
        df_freq["Top 10"] = df_freq.index < 10

        def highlight_top10(row):
            if row["Top 10"]:
                return ["background-color: #FFF3CD"] * len(row)
            return [""] * len(row)

        st.dataframe(
            df_freq.style.apply(highlight_top10, axis=1),
            hide_index=True,
        )
    else:
        st.info("Sem dados de frequência para este filtro.")

    st.markdown("### Acumulações ao longo do tempo")
    fig_acum = graficos.grafico_acumulacoes(sorteios_filtrados)
    st.plotly_chart(fig_acum, use_container_width=True)

    st.markdown("### Distribuição por UF (quando disponível)")
    fig_uf = graficos.grafico_uf(sorteios_filtrados)
    if fig_uf.data:
        st.plotly_chart(fig_uf, use_container_width=True)
    else:
        st.info("Sem dados de UF suficientes para exibir o gráfico.")

# ------------------------------------------------------------
# Aba Combinações
# ------------------------------------------------------------

with aba_repet:
    st.subheader("Combinações Repetidas")
    duplas = stats.get("duplas_repetidas", [])
    trios = stats.get("trios_repetidos", [])
    quadras = stats.get("quadras_repetidas", [])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Duplas mais repetidas**")
        st.dataframe(pd.DataFrame(duplas, columns=["Combinação", "Vezes"]), hide_index=True)
    with col2:
        st.markdown("**Trios mais repetidos**")
        st.dataframe(pd.DataFrame(trios, columns=["Combinação", "Vezes"]), hide_index=True)
    with col3:
        st.markdown("**Quadras mais repetidas**")
        st.dataframe(pd.DataFrame(quadras, columns=["Combinação", "Vezes"]), hide_index=True)

# ------------------------------------------------------------
# Aba Sequências
# ------------------------------------------------------------

with aba_seq:
    st.subheader("Sequências consecutivas dentro do sorteio")

    seq = stats["sequencias_consecutivas"]

    df_seq = pd.DataFrame([
        {
            "Sequência": ", ".join(map(str, item["sequencia"])),
            "Tamanho": item["tamanho"],
            "Ocorrências": item["ocorrencias"],
            "Concursos": ", ".join(item["concursos"]),
        }
        for item in seq
    ])

    st.dataframe(df_seq, hide_index=True)

# ------------------------------------------------------------
# Aba Números Quentes e Frios
# ------------------------------------------------------------

with aba_quentes:
    st.header("Números🔥 e ❄️")
    quentes = stats.get("numeros_quentes_50", [])
    frios = stats.get("numeros_atrasados", [])

    col_quentes, col_frios = st.columns(2)
    with col_quentes:
        st.subheader("🔥 Mais frequentes (últimos 50 sorteios)")
        st.dataframe(pd.DataFrame(quentes, columns=["Número", "Frequência"]), hide_index=True)
    with col_frios:
        st.subheader("❄️ Mais atrasados")
        st.dataframe(pd.DataFrame(frios, columns=["Número", "Atraso"]), hide_index=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    if quentes:
        num_quente, freq_quente = quentes[0]
        col1.metric("🔥 Número mais quente", str(num_quente), f"{freq_quente} vezes")
    if frios:
        num_frio, atraso_frio = frios[0]
        col2.metric("❄️ Número mais frio", str(num_frio), f"{atraso_frio} sorteios sem aparecer")













