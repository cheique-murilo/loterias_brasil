from collections import Counter
from itertools import combinations
from typing import Iterable, List, Tuple
from modelos.sorteio import Sorteio

def repeticoes(
    sorteios: Iterable[Sorteio],
    tamanho: int = 2,
    minimo: int = 2,
    limite: int = 10,
) -> List[Tuple[Tuple[int, ...], int]]:
    c = Counter()
    for s in sorteios:
        for combo in combinations(s.principais, tamanho):
            c[combo] += 1
    return [(k, v) for k, v in c.most_common(limite) if v >= minimo]

