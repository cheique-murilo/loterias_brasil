from typing import List, Dict
from modelos.sorteio import Sorteio
from collections import Counter

# ============================================================
# 1) Atraso: há quantos sorteios este número não sai?
# ============================================================

def atraso_numeros(sorteios: List[Sorteio]) -> Dict[int, int]:
    """
    Retorna {numero: atraso_em_sorteios}.
    Atraso = quantos sorteios passaram desde a última vez que o número saiu.
    """
    atraso = {}
    vistos = set()

    # percorre do mais recente para o mais antigo
    for idx, s in enumerate(reversed(sorteios)):
        for n in s.principais:
            if n not in vistos:
                atraso[n] = idx  # idx = quantos sorteios atrás
                vistos.add(n)

    # números que nunca saíram (raro, mas possível)
    todos = set(n for s in sorteios for n in s.principais)
    for n in todos:
        atraso.setdefault(n, len(sorteios))

    return atraso


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
