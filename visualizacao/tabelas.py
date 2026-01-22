import pandas as pd
from typing import List, Dict, Any

from modelos.loteria_base import LoteriaBase


# ------------------------------------------------------------
# ÚLTIMOS SORTEIOS
# ------------------------------------------------------------
def dados_ultimos_sorteios(loteria: LoteriaBase) -> List[Dict[str, Any]]:
    ultimos = loteria.ultimos_5
    dados = []

    for s in reversed(ultimos):
        dados.append(
            {
                "Data": s.data.strftime("%d/%m/%Y"),
                "Concurso": s.concurso,
                "Números": ", ".join(map(str, s.principais)),
                "Prêmio": s.jackpot_fmt,
                "Acumulou?": "Sim" if s.acumulou else "Não",
                "Local": s.local_ganhadores,
            }
        )
    return dados


# ------------------------------------------------------------
# TABELA DE FREQUÊNCIAS
# ------------------------------------------------------------
def tabela_frequencias(freq_dict: Dict[int, int]) -> pd.DataFrame:
    df = pd.DataFrame(
        {"Número": list(freq_dict.keys()), "Frequência": list(freq_dict.values())}
    ).sort_values("Frequência", ascending=False)

    return df.reset_index(drop=True)


# ------------------------------------------------------------
# TABELA DE NÚMEROS QUENTES
# ------------------------------------------------------------
def tabela_quentes(quentes: List[tuple]) -> pd.DataFrame:
    return (
        pd.DataFrame(quentes, columns=["Número", "Frequência"])
        .sort_values("Frequência", ascending=False)
        .reset_index(drop=True)
    )


# ------------------------------------------------------------
# TABELA DE NÚMEROS FRIOS
# ------------------------------------------------------------
def tabela_frios(frios: List[tuple]) -> pd.DataFrame:
    return (
        pd.DataFrame(frios, columns=["Número", "Atraso"])
        .sort_values("Atraso", ascending=False)
        .reset_index(drop=True)
    )


