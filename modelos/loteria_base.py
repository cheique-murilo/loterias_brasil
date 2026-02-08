from dataclasses import dataclass, field
from typing import List
import pandas as pd

from modelos.sorteio import Sorteio


class LoteriaBase:
    def __init__(self, nome: str, qtd_principais: int, faixa: tuple[int, int]):
        self.nome = nome
        self.qtd_principais = qtd_principais
        self.faixa = faixa
        self.sorteios: List[Sorteio] = []

    def adicionar(self, sorteio: Sorteio):
        self.sorteios.append(sorteio)

    # ------------------------------------------------------------
    # Formatar locais (compatível com Dupla Sena)
    # ------------------------------------------------------------
    def formatar_local(self, s: Sorteio) -> str:
        if not hasattr(s, "locais") or not s.locais:
            return ""

        if len(s.locais) == 1 and s.locais[0]["uf"] == "CANAL ELETRÔNICO":
            return "CANAL ELETRÔNICO"

        return ", ".join(
            f"{loc['cidade']}/{loc['uf']} ({loc['ganhadores']})"
            for loc in s.locais
        )

    # ------------------------------------------------------------
    # Converter sorteios para DataFrame (corrigido)
    # ------------------------------------------------------------
    def to_dataframe(self) -> pd.DataFrame:
        linhas = []

        for s in self.sorteios:
            linhas.append({
                "Data": s.data.strftime("%d/%m/%Y"),
                "Concurso": s.concurso,
                "Sorteio": s.sorteio_num,  # <--- IMPORTANTE PARA DUPLA SENA
                "Números": ", ".join(map(str, s.principais)),
                "Acumulou": "Sim" if s.acumulou else "Não",
                "Jackpot": s.jackpot_fmt,
                "Ganhadores": s.ganhadores_total,  # <--- CAMPO CORRETO
                "Locais": self.formatar_local(s),
            })

        return pd.DataFrame(linhas)





