
from .loteria import Loteria
from servicos.calculos_estatisticos import CalculosEstatisticos

class Totoloto(Loteria):
    def __init__(self):
        super().__init__((1, 49), (1, 13))  # ← Agora aceita

    @property
    def nome(self) -> str:
        return "Totoloto"

    def ranking(self) -> dict:
        return CalculosEstatisticos(self).calculos_estatisticos()