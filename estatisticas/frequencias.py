from collections import Counter
from typing import Iterable
from modelos.sorteio import Sorteio

def frequencia_principais(sorteios: Iterable[Sorteio]) -> Counter:
    return Counter(n for s in sorteios for n in s.principais)

def frequencia_complementares(sorteios: Iterable[Sorteio]) -> Counter:
    return Counter(n for s in sorteios for n in s.complementares)
