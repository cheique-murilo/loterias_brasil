from typing import Dict, Any, Iterable
import unicodedata

from modelos.sorteio import Sorteio

from .frequencias import frequencia_principais
from .repeticoes import repeticoes
from .sequencias import sequencias_consecutivas
from .jackpots import (
    maior_jackpot,
    streak_acumulacoes,
    total_acumulacoes,
    total_jackpots_pagos,
)
from .atraso import (
    frequencia_recente,
    numeros_quentes,
    atraso_numeros,
    numeros_atrasados,
)


def formatar_int(n: int) -> str:
    return format(n, ",").replace(",", ".")


def normalizar_nome(nome: str) -> str:
    nome = nome.lower().strip()
    nome = unicodedata.normalize("NFD", nome)
    nome = "".join(c for c in nome if unicodedata.category(c) != "Mn")
    return nome


def calcular_tudo(sorteios: Iterable[Sorteio], nome_loteria: str) -> Dict[str, Any]:
    sorteios = list(sorteios)

    if not sorteios:
        return {}

    sorteios.sort(key=lambda s: (s.data, s.concurso_base, s.sorteio_num))

    fp = frequencia_principais(sorteios)

    resultados: Dict[str, Any] = {
        "total_sorteios": formatar_int(len(sorteios)),
        "total_acumulacoes": formatar_int(total_acumulacoes(sorteios)),
        "max_streak_acumulacoes": formatar_int(streak_acumulacoes(sorteios)),
        "maior_jackpot": maior_jackpot(sorteios),
        "frequencias": dict(fp),
        "frequencias_principais": dict(fp),
        "duplas_repetidas": repeticoes(sorteios, tamanho=2, limite=15),
        "trios_repetidos": repeticoes(sorteios, tamanho=3, limite=15),
        "quadras_repetidas": repeticoes(sorteios, tamanho=4, limite=15),
        "sequencias_consecutivas": sequencias_consecutivas(sorteios),
        "total_jackpots_pagos": formatar_int(total_jackpots_pagos(sorteios)),
        "frequencia_recente_50": frequencia_recente(sorteios, 50),
        "numeros_quentes_50": numeros_quentes(sorteios, 50),
        "atraso_numeros": atraso_numeros(sorteios),
        "numeros_atrasados": numeros_atrasados(sorteios),
    }

    resultados["especiais"] = {
        "tipo": None,
        "dados": None,
        "duplas": None,
    }

    return resultados








