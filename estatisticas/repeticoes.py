from collections import Counter
from itertools import combinations
from typing import Iterable, List, Tuple
from modelos.sorteio import Sorteio


def repeticoes(
    sorteios: Iterable[Sorteio],
    tamanho: int,
    limite: int = 15,
) -> List[Tuple[str, int]]:
    """
    Conta combinações de 'tamanho' números que se repetem em sorteios diferentes.
    Cada Sorteio é independente (Dupla Sena já vem separada como 1234-1, 1234-2).
    Retorna lista de (combinação_formatada, ocorrências), ordenada por frequência.
    Só retorna combinações com ocorrências > 1.
    """
    cont = Counter()

    for s in sorteios:
        nums = sorted(set(s.principais))
        if len(nums) < tamanho:
            continue

        for comb in combinations(nums, tamanho):
            cont[comb] += 1

    mais_comuns = [
        (comb, qtd) for comb, qtd in cont.most_common() if qtd > 1
    ][:limite]

    resultado = [
        (" - ".join(f"{n:02d}" for n in comb), qtd)
        for comb, qtd in mais_comuns
    ]

    return resultado



