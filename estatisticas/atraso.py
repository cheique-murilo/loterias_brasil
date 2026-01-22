from collections import Counter
from typing import Iterable, Dict, List, Tuple
from modelos.sorteio import Sorteio


def frequencia_recente(sorteios: Iterable[Sorteio], janela: int) -> Dict[int, int]:
    """
    Frequência dos números nos últimos 'janela' sorteios.
    """
    sorteios = list(sorteios)
    if not sorteios:
        return {}

    recentes = sorteios[-janela:]
    cont = Counter()
    for s in recentes:
        cont.update(s.principais)
    return dict(cont)


def numeros_quentes(sorteios: Iterable[Sorteio], janela: int) -> List[Tuple[int, int]]:
    """
    Top números mais frequentes nos últimos 'janela' sorteios.
    Retorna lista de (numero, frequencia), ordenada desc.
    """
    freq = frequencia_recente(sorteios, janela)
    return sorted(freq.items(), key=lambda x: (-x[1], x[0]))


def atraso_numeros(sorteios: Iterable[Sorteio]) -> Dict[int, int]:
    """
    Calcula o atraso (quantos sorteios desde a última aparição) de cada número.
    Considera todos os números que já apareceram em algum sorteio.
    """
    sorteios = list(sorteios)
    if not sorteios:
        return {}

    # Índice do último sorteio em que cada número apareceu
    ultimo_indice = {}
    for idx, s in enumerate(sorteios):
        for n in s.principais:
            ultimo_indice[n] = idx

    max_idx = len(sorteios) - 1
    atraso = {n: max_idx - idx for n, idx in ultimo_indice.items()}

    return atraso


def numeros_atrasados(sorteios: Iterable[Sorteio], limite: int = 15) -> List[Tuple[int, int]]:
    """
    Retorna os números mais atrasados (maior atraso primeiro).
    """
    atraso = atraso_numeros(sorteios)
    ordenado = sorted(atraso.items(), key=lambda x: (-x[1], x[0]))
    return ordenado[:limite]



# ============================================================
# 2) Frequência recente: quantas vezes saiu nos últimos N sorteios?
# ============================================================

def frequencia_recente(sorteios: List[Sorteio], N: int = 50) -> Dict[int, int]:
    """
    Conta quantas vezes cada número saiu nos últimos N sorteios.
    """
    ultimos = sorteios[-N:]
    freq = Counter(n for s in ultimos for n in s.principais)
    return dict(freq)


# ============================================================
# 3) Ranking dos números mais quentes (mais saíram recentemente)
# ============================================================

def numeros_quentes(sorteios: List[Sorteio], N: int = 50) -> List[tuple]:
    """
    Retorna lista ordenada: [(numero, freq_recente), ...]
    """
    freq = frequencia_recente(sorteios, N)
    return sorted(freq.items(), key=lambda x: x[1], reverse=True)


# ============================================================
# 4) Ranking dos números mais atrasados
# ============================================================

def numeros_atrasados(sorteios: List[Sorteio]) -> List[tuple]:
    """
    Retorna lista ordenada: [(numero, atraso), ...]
    """
    atraso = atraso_numeros(sorteios)
    return sorted(atraso.items(), key=lambda x: x[1], reverse=True)
