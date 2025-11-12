
from datetime import datetime
from typing import List, Optional

class Sorteio:
    def __init__(self, data: str, sorteio_id: str, loteria: str, numeros_sorteados: str,
                 numeros_complementares: str, acumulou: str, premio: Optional[int] = None,
                 jackpot: Optional[int] = None, paises: str = "", vencedores: int = 0):
        self.data = datetime.strptime(data, '%d/%m/%Y')  # String DD/MM/YYYY
        self.sorteio_id = sorteio_id
        self.loteria = loteria
        self.numeros_sorteados = sorted([int(n.strip()) for n in numeros_sorteados.split(',') if n.strip()])
        self.numeros_complementares = sorted([int(n.strip()) for n in numeros_complementares.split(',') if n.strip()])
        self.acumulou = acumulou == 'sim'
        self.premio = premio
        self.jackpot = jackpot
        self.paises = [p.strip() for p in paises.split(',') if p.strip()] if paises else []
        self.vencedores = vencedores

    def get_numeros_completos(self) -> List[int]:
        return sorted(self.numeros_sorteados + self.numeros_complementares)

    def __str__(self):
        return f"{self.loteria} - {self.data.strftime('%d/%m/%Y')}: {self.numeros_sorteados} + {self.numeros_complementares}"