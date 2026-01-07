from typing import Dict, Iterable

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modelos.sorteio import Sorteio

VERDE = "#2ECC71"


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
        color_discrete_sequence=[VERDE],
    )

    fig.update_traces(textposition="outside")

    return fig


def grafico_paises(premios: Dict[str, int]) -> go.Figure:
    df_paises = (
        pd.DataFrame(list(premios.items()), columns=["País", "Qtd"])
        .sort_values("Qtd", ascending=True)
    )

    fig = px.bar(
        df_paises,
        x="Qtd",
        y="País",
        orientation="h",
        text="Qtd",
        title="Qtde de prémios por país",
        color_discrete_sequence=[VERDE],
    )

    fig.update_traces(textposition="outside")

    # ✔ MOSTRA APENAS LABELS (Países + valores)
    fig.update_layout(
        xaxis=dict(
            showticklabels=False,   # remove números do eixo X
            title=None              # remove título do eixo X
        ),
        yaxis=dict(
            showticklabels=True,    # mantém nomes dos países
            title=None              # remove título do eixo Y
        ),
        showlegend=False
    )

    return fig


def grafico_jackpot(sorteios: Iterable[Sorteio]) -> go.Figure:
    sorteios = list(sorteios)

    df = pd.DataFrame(
        {
            "Data": [s.data for s in sorteios],
            "JackpotMilhoes": [
                getattr(s, "jackpot_int", s.jackpot) / 1_000_000 for s in sorteios],
        }
    ).sort_values("Data")

    fig = px.line(
        df,
        x="Data",
        y="JackpotMilhoes",
        markers=True,
        title="Evolução do prémio do jackpot",
        color_discrete_sequence=[VERDE],
    )

    fig.update_traces(
        marker=dict(color=VERDE),
        line=dict(color=VERDE),
    )
    # limites dinâmicos do eixo Y com pequena folga 
    min_y = df["JackpotMilhoes"].min() 
    max_y = df["JackpotMilhoes"].max()

    padding_inf = max(min_y * 0.9, 0) # não deixa ir abaixo de 0
    padding_sup = max_y * 1.05

    # ✔ MOSTRA APENAS LABELS (datas e valores)
    fig.update_layout(
        xaxis=dict(
            showticklabels=True,   # mantém datas
            title=None             # remove título do eixo X
        ),
        yaxis=dict(
            showticklabels=True,   # mantém valores
            title=None,            # remove título do eixo Y
            range=[padding_inf, padding_sup],
            tickformat=",.1f",
            ticksuffix="M"
        ),
        showlegend=False
    )

    return fig





