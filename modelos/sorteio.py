from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Sorteio:
    data: datetime
    codigo: str
    loteria: str
    numeros_principais: List[int]
    numeros_complementares: List[int]
    acumulou: Optional[bool]
    premio: Optional[int]
    jackpot: Optional[int]
    paises: List[str]
    vencedores: Optional[int]

