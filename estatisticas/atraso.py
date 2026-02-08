from collections import Counter
from typing import Iterable, Dict, List, Tuple
from modelos.sorteio import Sorteio


# ============================================================
# 1) Frequência recente
# ============================================================

def frequencia_recente(sorteios: Iterable[Sorteio], janela: int = 50) -> Dict[int, int]:
    """
    Conta quantas vezes cada número saiu nos últimos 'janela' sorteios.
    Funciona naturalmente para Dupla Sena porque cada sorteio é um objeto separado.
    """
    sorteios = list(sorteios)
    if not sorteios:
        return {}

    ultimos = sorteios[-janela:]
    cont = Counter()

    for s in ultimos:
        cont.update(s.principais)

    return dict(cont)


# ============================================================
# 2) Números quentes
# ============================================================

def numeros_quentes(sorteios: Iterable[Sorteio], janela: int = 50) -> List[Tuple[int, int]]:
    """
    Retorna os números mais frequentes nos últimos 'janela' sorteios.
    """
    freq = frequencia_recente(sorteios, janela)
    return sorted(freq.items(), key=lambda x: (-x[1], x[0]))


# ============================================================
# 3) Atraso dos números
# ============================================================

def atraso_numeros(sorteios: Iterable[Sorteio]) -> Dict[int, int]:
    """
    Calcula o atraso (quantos sorteios desde a última aparição) de cada número.
    """
    sorteios = list(sorteios)
    if not sorteios:
        return {}

    ultimo_indice = {}

    for idx, s in enumerate(sorteios):
        for n in s.principais:
            ultimo_indice[n] = idx

    max_idx = len(sorteios) - 1
    atraso = {n: max_idx - idx for n, idx in ultimo_indice.items()}

    return atraso


# ============================================================
# 4) Números mais atrasados
# ============================================================

def numeros_atrasados(sorteios: Iterable[Sorteio], limite: int = 15) -> List[Tuple[int, int]]:
    """
    Retorna os números mais atrasados, ordenados do maior atraso para o menor.
    """
    atraso = atraso_numeros(sorteios)
    ordenado = sorted(atraso.items(), key=lambda x: (-x[1], x[0]))
    return ordenado[:limite]

