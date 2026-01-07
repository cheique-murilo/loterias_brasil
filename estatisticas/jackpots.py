from modelos.sorteio import Sorteio

# ------------------------------------------------------------
# Maior jackpot (valor, concurso, data)
# ------------------------------------------------------------

def maior_jackpot(sorteios):
    """
    Retorna uma tupla:
        (valor_do_jackpot, concurso, data)
    Se não houver sorteios, retorna (0, None, None)
    """
    if not sorteios:
        return (0, None, None)

    s = max(sorteios, key=lambda x: x.jackpot)
    return (s.jackpot, s.concurso, s.data)

# ------------------------------------------------------------
# Total de acumulações
# ------------------------------------------------------------

def total_acumulacoes(sorteios):
    """
    Conta quantas vezes o jackpot acumulou.
    """
    return sum(1 for s in sorteios if s.acumulou)

# ------------------------------------------------------------
# Streak de acumulações
# ------------------------------------------------------------

def streak_acumulacoes(sorteios):
    """
    Retorna o maior número de acumulações consecutivas.
    """
    max_streak = 0
    atual = 0

    for s in sorteios:
        if s.acumulou:
            atual += 1
            max_streak = max(max_streak, atual)
        else:
            atual = 0

    return max_streak

# ------------------------------------------------------------
# Total de jackpots pagos
# ------------------------------------------------------------

def total_jackpots_pagos(sorteios):
    """
    Jackpot pago = NÃO acumulou.
    (Não depende do valor do jackpot.)
    """
    return sum(1 for s in sorteios if not s.acumulou)

