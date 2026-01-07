import os
import sys
from datetime import datetime as dt
import pandas as pd
import streamlit as st
import altair as alt

# ------------------------------------------------------------
# Caminhos e imports do projeto
# ------------------------------------------------------------

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from servicos.construir import carregar_e_processar_loterias
from estatisticas.agregador import calcular_tudo
from visualizacao import graficos

# ------------------------------------------------------------
# TEMA GLOBAL ALTAR — PADRONIZAÇÃO VERDE
# ------------------------------------------------------------

def tema_verde():
    return {
        "config": {
            "range": {
                "category": ["#2ECC71"],
                "ordinal": ["#2ECC71"],
                "heatmap": ["#2ECC71"],
            },
            "mark": {"color": "#2ECC71"},
            "arc": {"color": "#2ECC71"},
            "area": {"color": "#2ECC71"},
            "bar": {"color": "#2ECC71"},
            "line": {"color": "#2ECC71"},
            "trail": {"color": "#2ECC71"},
            "point": {"color": "#2ECC71"},
            "tick": {"color": "#2ECC71"},
            "circle": {"color": "#2ECC71"},
            "square": {"color": "#2ECC71"},
        }
    }

alt.themes.register("tema_verde", tema_verde)
alt.themes.enable("tema_verde")

# ------------------------------------------------------------
# Funções auxiliares de UI
# ------------------------------------------------------------

def mostrar_logo_loteria(nome_loteria: str):
    logos = {
        "Totoloto": os.path.join(ROOT, "logos", "totoloto.png"),
        "Euromilhões": os.path.join(ROOT, "logos", "euromilhoes.png"),
        "Eurodreams": os.path.join(ROOT, "logos", "eurodreams.png"),
    }
    caminho = logos.get(nome_loteria)
    if caminho and os.path.exists(caminho):
        st.image(caminho, width=150)


def titulo_principal():
    col1, col2 = st.columns([2, 2])
    
    with col1:
        st.markdown(
            "<h1 style='margin-top: 10px;'>Análise das loterias de Portugal</h1>",
            unsafe_allow_html=True,
        )

    with col2:
        logo_path = os.path.join(ROOT, "logos", "jogossantacasa.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=150)


def mostrar_data_atualizacao():
    CAMINHO_ARQUIVO = os.path.join(ROOT, "jogos_portugal.xlsx")

    if os.path.exists(CAMINHO_ARQUIVO):
        timestamp = os.path.getmtime(CAMINHO_ARQUIVO)
        data_mod = dt.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M")

        st.markdown(
            f"""
            <p style='font-size:14px; color:gray; margin-top:-10px;'>
                📅 <b>Dados atualizados em:</b> {data_mod}
            </p>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<p style='font-size:14px; color:red;'>⚠️ Arquivo de dados não encontrado.</p>",
            unsafe_allow_html=True
        )

# ------------------------------------------------------------
# Configuração de página
# ------------------------------------------------------------

st.set_page_config(
    page_title="Loterias Portugal",
    layout="wide",
    initial_sidebar_state="expanded",
)

titulo_principal()
mostrar_data_atualizacao()

st.markdown("---")

# ------------------------------------------------------------
# Filtros laterais
# ------------------------------------------------------------

loterias = carregar_e_processar_loterias()
nomes_disponiveis = [nome for nome, lot in loterias.items() if lot.total_sorteios > 0]

nome_lot = st.sidebar.selectbox("Escolha a loteria", nomes_disponiveis)
loto_original = loterias[nome_lot]

mostrar_logo_loteria(nome_lot)

# ------------------------------------------------------------
# Filtro por Data ou Concurso
# ------------------------------------------------------------

tipo_filtro = st.sidebar.radio("Filtrar por:", ["Data", "Concurso"], horizontal=True)

todos_concursos = sorted({s.concurso for s in loto_original.sorteios})

if tipo_filtro == "Data":
    min_date = min(s.data for s in loto_original.sorteios).date()
    max_date = max(s.data for s in loto_original.sorteios).date()

    d_inicio = st.sidebar.date_input("Data inicial", min_date, min_value=min_date, max_value=max_date)
    d_fim = st.sidebar.date_input("Data final", max_date, min_value=min_date, max_value=max_date)

    if d_inicio > d_fim:
        st.sidebar.error("Data inicial não pode ser maior que a final.")
        st.stop()

    inicio_dt = dt.combine(d_inicio, dt.min.time())
    fim_dt = dt.combine(d_fim, dt.max.time())

    sorteios_filtrados = [s for s in loto_original.sorteios if inicio_dt <= s.data <= fim_dt]

else:
    concurso_escolhido = st.sidebar.selectbox("Escolha o concurso", todos_concursos)
    sorteios_filtrados = [s for s in loto_original.sorteios if s.concurso == concurso_escolhido]

if not sorteios_filtrados:
    st.warning("Nenhum sorteio encontrado com o filtro selecionado.")
    st.stop()

# ------------------------------------------------------------
# Download do histórico
# ------------------------------------------------------------

st.sidebar.markdown("### Download do histórico")

df_historico = loto_original.to_dataframe()
csv_bytes = df_historico.to_csv(index=False).encode("utf-8")

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
# Abas principais
# ------------------------------------------------------------

aba_resumo, aba_repet, aba_seq, aba_jackpots, aba_especiais, aba_quentes = st.tabs(
    ["Resumo 📈", "Combinações 🔍", "Sequências 📌", "Jackpots 🎰", "Números extras 🎯", "Números🔥 e ❄️"]
)

# ------------------------------------------------------------
# RESUMO
# ------------------------------------------------------------

with aba_resumo:
    st.subheader("Resumo geral")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total de sorteios", stats["total_sorteios"])

    with col2:
        st.metric("Total de acumulações", stats["total_acumulacoes"])

    with col3:
        st.metric("Total de jackpots pagos", stats["total_jackpots_pagos"])    

    with col4:
        st.metric("Maior streak de acumulações", stats["max_streak_acumulacoes"])

    with col5:
        valor, concurso, data = stats["maior_jackpot"]
        if valor > 0:
            valor_fmt = f"€{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            st.metric("Maior jackpot", valor_fmt)
            st.caption(f"Concurso {concurso} — {data.strftime('%d/%m/%Y')}")
        else:
            st.metric("Maior jackpot", "—")
            st.caption("Nenhum jackpot encontrado")

    st.markdown("### Últimos resultados")

    ultimos = sorted(sorteios_filtrados, key=lambda s: s.data, reverse=True)[:50]

    # Nome correto da coluna de complementares
    if nome_lot == "Totoloto":
        nome_coluna_comp = "Número da sorte"
    elif nome_lot == "Eurodreams":
        nome_coluna_comp = "Número do sonho"
    elif nome_lot == "Euromilhões":
        nome_coluna_comp = "Estrelas"
    else:
        nome_coluna_comp = "Números complementares"

    df_ultimos = pd.DataFrame([
        {
            "Data": s.data.strftime("%d/%m/%Y"),
            "Concurso": s.concurso,
            "Números": ", ".join(map(str, s.principais)),
            nome_coluna_comp: ", ".join(map(str, s.complementares)),
            "Jackpot": s.jackpot_fmt,
            "Acumulou?": "Sim" if s.acumulou else "Não",
        }
        for s in ultimos
    ])

    st.dataframe(df_ultimos, width="stretch", hide_index=True)

# ------------------------------------------------------------
# COMBINAÇÕES
# ------------------------------------------------------------

with aba_repet:
    st.subheader("Combinações Repetidas")

    duplas = stats.get("duplas_repetidas", [])
    trios = stats.get("trios_repetidos", [])
    quadras = stats.get("quadras_repetidas", [])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Duplas mais repetidas**")
        if duplas:
            df_duplas = pd.DataFrame(duplas, columns=["Combinação", "Vezes"])
            st.dataframe(df_duplas, width="stretch", hide_index=True)
        else:
            st.info("Sem duplas repetidas no período filtrado.")

    with col2:
        st.markdown("**Trios mais repetidos**")
        if trios:
            df_trios = pd.DataFrame(trios, columns=["Combinação", "Vezes"])
            st.dataframe(df_trios, width="stretch", hide_index=True)
        else:
            st.info("Sem trios repetidos no período filtrado.")

    with col3:
        st.markdown("**Quadras mais repetidas**")
        if quadras:
            df_quadras = pd.DataFrame(quadras, columns=["Combinação", "Vezes"])
            st.dataframe(df_quadras, width="stretch", hide_index=True)
        else:
            st.info("Sem quadras repetidas no período filtrado.")

# ------------------------------------------------------------
# SEQUÊNCIAS
# ------------------------------------------------------------

with aba_seq:
    st.subheader("Sequências consecutivas")

    seq = stats.get("sequencias_consecutivas")
    if seq is None:
        st.info("Sem dados de sequências para este filtro.")
    else:
        df_seq = pd.DataFrame(seq)
        st.dataframe(df_seq, width="stretch", hide_index=True)

# ------------------------------------------------------------
# JACKPOTS
# ------------------------------------------------------------

with aba_jackpots:
    col1, col2 = st.columns(2)

    with col1:
        premios = stats.get("premios_por_pais", {})
        if premios:
            fig_paises = graficos.grafico_paises(premios)
            st.plotly_chart(fig_paises, use_container_width=True)
        else:
            st.info("Sem dados de países neste período.")

    with col2:
        fig_jack = graficos.grafico_jackpot(sorteios_filtrados)
        st.plotly_chart(fig_jack, use_container_width=True)

    st.markdown("## Ranking de vencedores do jackpot")

    ranking = stats["ranking_vencedores_jackpot"]

    if ranking:
        ranking_filtrado = {k: v for k, v in ranking.items() if k > 0}

        if not ranking_filtrado:
            st.info("Não há jackpots pagos com vencedores.")
        else:
            ranking_ordenado = dict(sorted(ranking_filtrado.items(), key=lambda x: x[1], reverse=True))
            max_freq = max(ranking_ordenado.values())

            linhas = []
            for vencedores, vezes in ranking_ordenado.items():
                blocos = int((vezes / max_freq) * 10)
                barra = "<span style='color:#2ECC71;'>█</span>" * max(blocos, 1)
                label = "vencedor" if vencedores == 1 else "vencedores"
                linhas.append(f"{vencedores} {label} | {barra}  {vezes} vezes")

            st.markdown(
                "<div style='font-family:monospace; font-size:16px; white-space:pre;'>"
                + "<br>".join(linhas) +
                "</div>",
                unsafe_allow_html=True
            )

    else:
        st.info("Não há dados suficientes para exibir o ranking.")

# ------------------------------------------------------------
# NÚMEROS ESPECIAIS
# ------------------------------------------------------------

with aba_especiais:
    esp = stats.get("especiais", {})

    if not esp or esp.get("tipo") is None or esp.get("dados") is None:
        st.info("Esta loteria não possui números especiais ou não há dados disponíveis.")
        st.stop()

    tipo = esp["tipo"]
    dados = esp["dados"]

    st.markdown(f"### {tipo}")

    # Frequências gerais e em jackpots
    freq_geral = dados.get("frequencias_geral", {})
    freq_jack = dados.get("frequencias_jackpots", {})

    # Ordenações
    mais_frequentes = sorted(freq_geral.items(), key=lambda x: x[1], reverse=True)
    menos_frequentes = sorted(freq_geral.items(), key=lambda x: x[1])
    mais_jackpots = sorted(freq_jack.items(), key=lambda x: x[1], reverse=True)

    # ------------------------------------------------------------
    # CASO EUROMILHÕES — estrelas e duplas
    # ------------------------------------------------------------
    if nome_lot == "Euromilhões":

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### Estrela mais frequentes")
            df1 = pd.DataFrame(mais_frequentes, columns=["Estrela", "Frequência"])
            st.dataframe(df1, use_container_width=True, hide_index=True)

        with col2:
            st.markdown("#### Estrela menos frequentes")
            df2 = pd.DataFrame(menos_frequentes, columns=["Estrela", "Frequência"])
            st.dataframe(df2, use_container_width=True, hide_index=True)

        with col3:
            st.markdown("#### Estrela mais frequentes em jackpots")
            df3 = pd.DataFrame(mais_jackpots, columns=["Estrela", "Frequência"])
            st.dataframe(df3, use_container_width=True, hide_index=True)

        # Duplas
        if esp.get("duplas"):
            #st.markdown("###  Duplas de estrelas")

            duplas = esp["duplas"]
            freq_duplas_geral = sorted(
                duplas["frequencias_geral"].items(),
                key=lambda x: x[1],
                reverse=True
            )
            freq_duplas_jack = sorted(
                duplas["frequencias_jackpots"].items(),
                key=lambda x: x[1],
                reverse=True
            )

            colA, colB = st.columns(2)

            with colA:
                st.markdown("#### Estrelas mais frequentes")
                dfA = pd.DataFrame(freq_duplas_geral, columns=["Dupla", "Frequência"])
                st.dataframe(dfA, use_container_width=True, hide_index=True)

            with colB:
                st.markdown("#### Estrelas mais frequentes em jackpots")
                dfB = pd.DataFrame(freq_duplas_jack, columns=["Dupla", "Frequência"])
                st.dataframe(dfB, use_container_width=True, hide_index=True)

    # ------------------------------------------------------------
    # OUTRAS LOTERIAS — comportamento padrão
    # ------------------------------------------------------------
    else:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### Mais frequentes")
            df1 = pd.DataFrame(mais_frequentes, columns=["Valor", "Frequência"])
            st.dataframe(df1, use_container_width=True, hide_index=True)

        with col2:
            st.markdown("#### Menos frequentes")
            df2 = pd.DataFrame(menos_frequentes, columns=["Valor", "Frequência"])
            st.dataframe(df2, use_container_width=True, hide_index=True)

        with col3:
            st.markdown("#### Mais frequentes em jackpots")
            df3 = pd.DataFrame(mais_jackpots, columns=["Valor", "Frequência"])
            st.dataframe(df3, use_container_width=True, hide_index=True)


# ------------------------------------------------------------
# QUENTES & FRIOS
# ------------------------------------------------------------

with aba_quentes:
    st.header("Números🔥 e ❄️")

    # Dados vindos do agregador
    quentes = stats.get("numeros_quentes_50", [])
    frios = stats.get("numeros_atrasados", [])
    
    col_quentes, col_frios = st.columns(2)

    # ---------------------------------------------------------
    # 🔥 NÚMEROS QUENTES — últimos 50 sorteios
    # ---------------------------------------------------------
    #st.subheader("🔥 Números quentes - mais frequentes (últimos 50 sorteios)")
    with col_quentes:
        st.subheader("🔥 Números quentes - mais frequentes (últimos 50 sorteios)")

        if quentes:
            df_quentes = (
                pd.DataFrame(quentes, columns=["Número", "Frequência"])
                .sort_values("Frequência", ascending=False)
                .head(10)
            )
            st.dataframe(df_quentes, use_container_width=True, hide_index=True)
        else:
            st.info("Não há dados suficientes para calcular números quentes.")

    # ---------------------------------------------------------
    # ❄️ NÚMEROS FRIOS — mais atrasados
    # ---------------------------------------------------------
    with col_frios:
        st.subheader("❄️ Números frios - mais atrasados (últimos 50 sorteios)")

        if frios:
            df_frios = (
                pd.DataFrame(frios, columns=["Número", "Atraso"])
                .sort_values("Atraso", ascending=False)
                .head(10)
            )
            st.dataframe(df_frios, use_container_width=True, hide_index=True)
        else:
            st.info("Não há dados suficientes para calcular números frios.")

    # ---------------------------------------------------------
    # Indicadores visuais
    # ---------------------------------------------------------
    st.markdown("---")
    #st.subheader("Indicadores")

    col1, col2 = st.columns(2)

    if quentes:
        num_quente, freq_quente = quentes[0]
        col1.metric(
            label="🔥 Número mais quente",
            value=str(num_quente),
            delta=f"{freq_quente} vezes nos últimos 50 sorteios"
        )

    if frios:
        num_frio, atraso_frio = frios[0]
        col2.metric(
            label="❄️ Número mais frio",
            value=str(num_frio),
            delta=f"{atraso_frio} sorteios sem aparecer"
        )






