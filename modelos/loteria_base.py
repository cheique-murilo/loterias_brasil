from __future__ import annotations
from typing import List, Tuple
import pandas as pd
from .sorteio import Sorteio

class LoteriaBase:
    def __init__(
        self,
        nome: str,
        qtd_principais: int,
        faixa_principais: Tuple[int, int],
    ):
        self.nome = nome
        self.qtd_principais = qtd_principais
        self.faixa_principais = faixa_principais
        self._sorteios: List[Sorteio] = []

    def adicionar(self, sorteio: Sorteio) -> None:
        self._sorteios.append(sorteio)
        self._sorteios.sort(key=lambda s: (s.data, s.concurso_base, s.sorteio_num))


    def adicionar_multiplos(self, lista: List[Sorteio]) -> None:
        for s in lista:
            self.adicionar(s)

    @property
    def sorteios(self) -> List[Sorteio]:
        return self._sorteios

    @property
    def total_sorteios(self) -> int:
        return len(self._sorteios)

    @property
    def ultimos_5(self) -> List[Sorteio]:
        return self._sorteios[-5:] if self._sorteios else []

    def to_dataframe(self) -> pd.DataFrame:
        def formatar_local(s: Sorteio) -> str:
            # Caso especial: Canal Eletrônico
            if s.uf == "CANAL ELETRÔNICO":
                return "CANAL ELETRÔNICO"

            # Cidade + UF
            if s.cidade and s.uf:
                return f"{s.cidade}/{s.uf}"

            # Só cidade
            if s.cidade:
                return s.cidade

            # Só UF
            if s.uf:
                return s.uf

            return ""

        return pd.DataFrame([
            {
                "Data": s.data,
                "Concurso": s.concurso,
                "Números": s.principais,
                "Acumulou": s.acumulou,
                "Jackpot": s.jackpot_fmt,
                "Ganhadores": s.ganhadores,
                "Local": formatar_local(s),
            }
            for s in self.sorteios
        ])




