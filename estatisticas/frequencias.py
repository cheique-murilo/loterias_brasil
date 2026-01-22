from collections import Counter
from typing import Iterable, Dict
from modelos.sorteio import Sorteio


def frequencia_principais(sorteios: Iterable[Sorteio]) -> Dict[int, int]:
    """
    Conta a frequência de cada número nas dezenas principais.
    Cada Sorteio é tratado de forma independente (inclui Dupla Sena naturalmente).
    """
    cont = Counter()
    for s in sorteios:
        cont.update(s.principais)
    return dict(cont)

