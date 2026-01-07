from .loteria_base import LoteriaBase
from .sorteio import Sorteio

class Eurodreams(LoteriaBase):
    def __init__(self):
        super().__init__(
            nome="Eurodreams",
            label_complementar="Sonho",
            qtd_principais=6,
            qtd_complementares=1,
            faixa_principais=(1, 40),
            faixa_complementares=(1, 5),
        )

    def validar_sorteio(self, sorteio: Sorteio) -> bool:
        return self._validar_basico(sorteio)

