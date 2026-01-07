from datetime import datetime
from .loteria_base import LoteriaBase
from .sorteio import Sorteio

class Totoloto(LoteriaBase):
    def __init__(self):
        # Valores padrão não são usados diretamente para validação,
        # porque a regra muda com a data, mas mantemos algo coerente.
        super().__init__(
            nome="Totoloto",
            label_complementar="Chave",
            qtd_principais=5,
            qtd_complementares=1,
            faixa_principais=(1, 49),
            faixa_complementares=(1, 13),
        )
        self.data_corte = datetime(2011, 3, 13)

    def validar_sorteio(self, sorteio: Sorteio) -> bool:
        if sorteio.data < self.data_corte:
            # Regra antiga: 6/49 + 1 suplementar (todos 1-49, 7 números distintos)
            principais = sorteio.principais
            comp = sorteio.complementares

            if len(principais) != 6:
                return False
            if len(comp) != 1:
                return False

            nums = principais + comp
            if any(n < 1 or n > 49 for n in nums):
                return False

            if len(set(nums)) != 7:
                return False

            return True

        # Regra nova: 5/49 + 1/13
        principais = sorteio.principais
        comp = sorteio.complementares

        if len(principais) != 5 or len(comp) != 1:
            return False

        if any(n < 1 or n > 49 for n in principais):
            return False

        if comp[0] < 1 or comp[0] > 13:
            return False

        if len(set(principais)) != 5:
            return False

        return True
