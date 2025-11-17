
from .loteria import Loteria
from servicos.calculos_estatisticos import CalculosEstatisticos

class Euromilhoes(Loteria):
    def __init__(self):
        super().__init__((1, 50), (1, 12))  # ← Agora aceita

    @property
    def nome(self) -> str:
        return "Euromilhões"

    def ranking(self) -> dict:
        return CalculosEstatisticos(self).calculos_estatisticos()


