from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Tuple
from .sorteio import Sorteio
import pandas as pd

class LoteriaBase(ABC):
    def __init__(
        self,
        nome: str,
        label_complementar: str,
        qtd_principais: int,
        qtd_complementares: int,
        faixa_principais: Tuple[int, int],
        faixa_complementares: Tuple[int, int],
    ):
        self.nome = nome
        self.label_complementar = label_complementar
        self.qtd_principais = qtd_principais
        self.qtd_complementares = qtd_complementares
        self.faixa_principais = faixa_principais
        self.faixa_complementares = faixa_complementares
        self._sorteios: List[Sorteio] = []

    def adicionar(self, sorteio: Sorteio) -> None:
        """Adiciona o sorteio se for válido; caso contrário, descarta."""
        if not self.validar_sorteio(sorteio):
            # Em produção, podes trocar print por log
            print(
                f"Aviso: Sorteio {sorteio.concurso} não é válido para {self.nome} e foi descartado."
            )
            return

        self._sorteios.append(sorteio)
        self._sorteios.sort(key=lambda s: s.data)

    @property
    def sorteios(self) -> List[Sorteio]:
        return self._sorteios

    @property
    def total_sorteios(self) -> int:
        return len(self._sorteios)

    @property
    def ultimos_5(self) -> List[Sorteio]:
        return self._sorteios[-5:] if self._sorteios else []

    def _validar_basico(self, sorteio: Sorteio) -> bool:
        """Valida quantidade, faixa e duplicatas."""
        qtd_p = len(sorteio.principais)
        qtd_c = len(sorteio.complementares)

        if qtd_p != self.qtd_principais or qtd_c != self.qtd_complementares:
            return False

        min_p, max_p = self.faixa_principais
        min_c, max_c = self.faixa_complementares

        if not all(min_p <= n <= max_p for n in sorteio.principais):
            return False
        if not all(min_c <= n <= max_c for n in sorteio.complementares):
            return False

        if len(set(sorteio.principais)) != qtd_p:
            return False
        if len(set(sorteio.complementares)) != qtd_c:
            return False

        return True

    @abstractmethod
    def validar_sorteio(self, sorteio: Sorteio) -> bool:
        """Cada loteria pode extender ou sobrescrever a validação básica."""
        ...

    def to_dataframe(self):
        return pd.DataFrame([
        {
            "data": s.data,
            "concurso": s.concurso,
            "principais": s.principais,
            "complementares": s.complementares,
            "acumulou": s.acumulou,
            "jackpot": s.jackpot,
            "pais": s.paises_ganhadores
        }
        for s in self.sorteios
    ])

