import re
from typing import Iterable, Tuple
from modelos.sorteio import Sorteio


def _jackpot_to_float(valor: str) -> float:
    if not valor:
        return 0.0

    v = re.sub(r"[R$\s\.]", "", valor)
    v = v.replace(",", ".")

    try:
        return float(v)
    except:
        return 0.0


def maior_jackpot(sorteios: Iterable[Sorteio]) -> Tuple[str, str, object]:
    """
    Retorna (valor_fmt, concurso, data).
    Ignora sorteios sem jackpot (ex: 2º sorteio da Dupla Sena).
    """
    sorteios = list(sorteios)
    if not sorteios:
        return ("R$ 0,00", None, None)

    validos = [s for s in sorteios if _jackpot_to_float(s.jackpot_fmt) > 0]

    if not validos:
        return ("R$ 0,00", None, None)

    s = max(validos, key=lambda x: _jackpot_to_float(x.jackpot_fmt))
    return (s.jackpot_fmt, s.concurso, s.data)


def total_acumulacoes(sorteios: Iterable[Sorteio]) -> int:
    return sum(1 for s in sorteios if s.acumulou)


def streak_acumulacoes(sorteios: Iterable[Sorteio]) -> int:
    """
    Maior sequência consecutiva de sorteios acumulados.
    Ordena internamente por (data, concurso_base, sorteio_num) para Dupla Sena.
    """
    sorteios = sorted(sorteios, key=lambda s: (s.data, s.concurso_base, s.sorteio_num))

    max_streak = 0
    atual = 0

    for s in sorteios:
        if s.acumulou:
            atual += 1
            max_streak = max(max_streak, atual)
        else:
            atual = 0

    return max_streak


def total_jackpots_pagos(sorteios: Iterable[Sorteio]) -> int:
    """
    Total de sorteios em que houve ganhadores (não acumulou).
    """
    return sum(1 for s in sorteios if not s.acumulou)




