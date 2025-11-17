# modelos/loteria.py
from abc import ABC, abstractmethod
from typing import List
from .sorteio import Sorteio
import pandas as pd

class Loteria(ABC):
    def __init__(self, faixa_principais: tuple, faixa_complementares: tuple):
        self.faixa_principais = faixa_principais
        self.faixa_complementares = faixa_complementares
        self.sorteios: List[Sorteio] = []

    @property
    @abstractmethod
    def nome(self) -> str:
        pass

    @abstractmethod
    def ranking(self) -> dict:
        pass

    def adicionar_sorteio(self, sorteio: Sorteio):
        self.sorteios.append(sorteio)  # Adiciona SEM qualquer validação

    def to_dataframe(self) -> pd.DataFrame:
        if not self.sorteios:
            return pd.DataFrame()
        return pd.DataFrame([{
            'data': s.data.strftime('%d/%m/%Y'),
            'sorteio_id': s.sorteio_id,
            'numeros_sorteados': ', '.join(map(str, s.numeros_sorteados)),
            'numeros_complementares': ', '.join(map(str, s.numeros_complementares)),
            'acumulou': 'Sim' if s.acumulou else 'Não',
            'jackpot': s.jackpot,
            'vencedores': s.vencedores
        } for s in self.sorteios])