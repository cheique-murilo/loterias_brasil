from typing import Iterable, Dict, Any
from modelos.sorteio import Sorteio

from .frequencias import frequencia_principais
from .repeticoes import repeticoes
from .sequencias import sequencias_consecutivas
from .jackpots import (
    maior_jackpot,
    total_acumulacoes,
    streak_acumulacoes,
    total_jackpots_pagos,
)
from .atraso import (
    frequencia_recente,
    numeros_quentes,
    atraso_numeros,
    numeros_atrasados,
)


def calcular_tudo(sorteios: Iterable[Sorteio], nome_loteria: str) -> Dict[str, Any]:
    sorteios = list(sorteios)
    if not sorteios:
        return {}

    # -------------------------
    # Frequências gerais
    # -------------------------
    freq = frequencia_principais(sorteios)

    # -------------------------
    # Combinações repetidas
    # -------------------------
    duplas = repeticoes(sorteios, tamanho=2)
    trios = repeticoes(sorteios, tamanho=3)
    quadras = repeticoes(sorteios, tamanho=4)

    # -------------------------
    # Sequências consecutivas
    # -------------------------
    seq = sequencias_consecutivas(sorteios)

    # -------------------------
    # Números quentes e frios
    # -------------------------
    freq_50 = frequencia_recente(sorteios, janela=50)
    quentes_50 = numeros_quentes(sorteios, janela=50)
    atrasados = numeros_atrasados(sorteios)

    # -------------------------
    # Jackpots e acumulações
    # -------------------------
    maior_jp = maior_jackpot(sorteios)
    total_acum = total_acumulacoes(sorteios)
    streak = streak_acumulacoes(sorteios)
    jackpots_pagos = total_jackpots_pagos(sorteios)

    return {
        "total_sorteios": len(sorteios),
        "frequencias": freq,
        "duplas_repetidas": duplas,
        "trios_repetidos": trios,
        "quadras_repetidas": quadras,
        "sequencias_consecutivas": seq,
        "numeros_quentes_50": quentes_50,
        "numeros_atrasados": atrasados,
        "maior_jackpot": maior_jp,
        "total_acumulacoes": total_acum,
        "max_streak_acumulacoes": streak,
        "total_jackpots_pagos": jackpots_pagos,
    }










