from .loteria_base import LoteriaBase
from .sorteio import Sorteio

class Euromilhoes(LoteriaBase):
    def __init__(self):
        super().__init__(
            nome="Euromilhões",
            label_complementar="Estrelas",
            qtd_principais=5,
            qtd_complementares=2,
            faixa_principais=(1, 50),
            faixa_complementares=(1, 12),
        )

    def validar_sorteio(self, sorteio: Sorteio) -> bool:
        # A validação básica já cobre tudo que precisamos
        return self._validar_basico(sorteio)
