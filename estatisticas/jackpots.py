from modelos.sorteio import Sorteio
import re
from typing import Iterable, Tuple


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
    """
    sorteios = list(sorteios)
    if not sorteios:
        return ("R$ 0,00", None, None)

    s = max(sorteios, key=lambda x: _jackpot_to_float(x.jackpot_fmt))
    return (s.jackpot_fmt, s.concurso, s.data)


def total_acumulacoes(sorteios: Iterable[Sorteio]) -> int:
    return sum(1 for s in sorteios if s.acumulou)


def streak_acumulacoes(sorteios: Iterable[Sorteio]) -> int:
    """
    Maior sequência consecutiva de sorteios acumulados.
    Ordena internamente por (data, concurso) para garantir consistência.
    """
    sorteios = sorted(sorteios, key=lambda s: (s.data, s.concurso_base, s.sorteio_num))

    max_streak = 0
    atual = 0

    for s in sorteios:
        if s.acumulou:
            atual += 1
            if atual > max_streak:
                max_streak = atual
        else:
            atual = 0

    return max_streak


def total_jackpots_pagos(sorteios: Iterable[Sorteio]) -> int:
    """
    Total de sorteios em que houve ganhadores (não acumulou).
    """
    return sum(1 for s in sorteios if not s.acumulou)



