from .loteria import Loteria
from servicos.calculos_estatisticos import CalculosEstatisticos

class Eurodreams(Loteria):
    def __init__(self):
        super().__init__((1, 40), (1, 5))  # ← Agora aceita

    @property
    def nome(self) -> str:
        return "Eurodreams"

    def ranking(self) -> dict:
        return CalculosEstatisticos(self).calculos_estatisticos()

    

