import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Iterable

from modelos.sorteio import Sorteio
from estatisticas.jackpots import _jackpot_to_float

AZUL = "#0A4ECF"
AZUL_ESCURO = "#063A9B"
AZUL_CLARO = "#4C7DFF"


# ------------------------------------------------------------
# FREQUÊNCIA DOS NÚMEROS
# ------------------------------------------------------------
def grafico_frequencias(freq_dict: Dict[int, int]) -> go.Figure:
    df = (
        pd.DataFrame(
            {"Número": list(freq_dict.keys()), "Frequência": list(freq_dict.values())}
        )
        .sort_values("Frequência", ascending=False)
        .reset_index(drop=True)
    )

    fig = px.bar(
        df,
        x="Número",
        y="Frequência",
        text="Frequência",
        title="Frequência dos Números",
        color_discrete_sequence=[AZUL],
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
        title_font_color=AZUL_ESCURO,
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False,
    )

    return fig


# ------------------------------------------------------------
# ACUMULAÇÕES AO LONGO DO TEMPO
# ------------------------------------------------------------
def grafico_acumulacoes(sorteios: Iterable[Sorteio]) -> go.Figure:
    df = pd.DataFrame(
        [
            {
                "Data": s.data,
                "Jackpot": _jackpot_to_float(s.jackpot_fmt),
                "Acumulou": s.acumulou,
            }
            for s in sorteios
        ]
    )

    if df.empty:
        return go.Figure()

    fig = px.line(
        df,
        x="Data",
        y="Jackpot",
        title="Evolução do Jackpot",
        markers=False,
    )

    df_acum = df[df["Acumulou"]]
    if not df_acum.empty:
        fig.add_scatter(
            x=df_acum["Data"],
            y=df_acum["Jackpot"],
            mode="markers",
            marker=dict(size=10, color="red"),
            name="Acumulou",
        )

    fig.update_layout(
        title_font_color=AZUL_ESCURO,
        xaxis_title=None,
        yaxis_title="Jackpot (R$)",
        showlegend=True,
    )

    return fig


# ------------------------------------------------------------
# DISTRIBUIÇÃO POR UF (NOVO PIPELINE)
# ------------------------------------------------------------
def grafico_uf(sorteios: Iterable[Sorteio]) -> go.Figure:
    df = pd.DataFrame(
        [
            {"UF": s.uf}
            for s in sorteios
            if s.uf  # ignora sem UF
        ]
    )

    if df.empty:
        return go.Figure()

    df = df.value_counts("UF").reset_index(name="Ocorrências")
    df = df.sort_values("Ocorrências", ascending=False)

    fig = px.bar(
        df,
        x="Ocorrências",
        y="UF",
        orientation="h",
        text="Ocorrências",
        color_discrete_sequence=[AZUL],
    )

    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(title=None, showticklabels=True),
        showlegend=False,
        height=500,
        margin=dict(l=20, r=20, t=20, b=20),
    )

    fig.update_yaxes(autorange="reversed")
    fig.update_traces(textposition="outside")

    return fig











