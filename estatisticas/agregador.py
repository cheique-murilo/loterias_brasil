from typing import Dict, Any, Iterable
import unicodedata
from collections import Counter
from modelos.sorteio import Sorteio

from .frequencias import frequencia_principais, frequencia_complementares
from .repeticoes import repeticoes
from .sequencias import sequencias_consecutivas
from .jackpots import (
    maior_jackpot,
    streak_acumulacoes,
    total_acumulacoes,
    total_jackpots_pagos,
)
from .paises import premios_por_pais
from .especiais import (
    totoloto_numero_sorte,
    eurodreams_sonho,
    euromilhoes_estrelas,
    euromilhoes_duplas_estrelas,
)

# 🔥 NOVO
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

    fp = frequencia_principais(sorteios)
    fc = frequencia_complementares(sorteios)

    resultados: Dict[str, Any] = {
        "total_sorteios": formatar_int(len(sorteios)),
        "total_acumulacoes": formatar_int(total_acumulacoes(sorteios)),
        "max_streak_acumulacoes": formatar_int(streak_acumulacoes(sorteios)),

        "maior_jackpot": maior_jackpot(sorteios),

        "frequencias": dict(fp),
        "frequencias_principais": dict(fp),
        "frequencias_complementares": dict(fc),

        "duplas_repetidas": repeticoes(sorteios, tamanho=2, limite=15),
        "trios_repetidos": repeticoes(sorteios, tamanho=3, limite=15),
        "quadras_repetidas": repeticoes(sorteios, tamanho=4, limite=15),

        "sequencias_consecutivas": sequencias_consecutivas(sorteios),

        "premios_por_pais": premios_por_pais(sorteios),

        "total_jackpots_pagos": formatar_int(total_jackpots_pagos(sorteios)),

        "ranking_vencedores_jackpot": ranking_vencedores_jackpot(sorteios),

        # 🔥 NOVAS MÉTRICAS
        "frequencia_recente_50": frequencia_recente(sorteios, 50),
        "numeros_quentes_50": numeros_quentes(sorteios, 50),
        "atraso_numeros": atraso_numeros(sorteios),
        "numeros_atrasados": numeros_atrasados(sorteios),
    }

    nome_normalizado = normalizar_nome(nome_loteria)

    resultados["especiais"] = {
        "tipo": None,
        "dados": None,
        "duplas": None,
    }

    if nome_normalizado == "totoloto":
        resultados["especiais"]["tipo"] = "Totoloto — Número da sorte 🍀"
        resultados["especiais"]["dados"] = totoloto_numero_sorte(sorteios)

    elif nome_normalizado == "eurodreams":
        resultados["especiais"]["tipo"] = "Eurodreams — Número do sonho 😴"
        resultados["especiais"]["dados"] = eurodreams_sonho(sorteios)

    elif nome_normalizado == "euromilhoes":
        resultados["especiais"]["tipo"] = "Euromilhões — Estrelas 🌟"
        resultados["especiais"]["dados"] = euromilhoes_estrelas(sorteios)
        resultados["especiais"]["duplas"] = euromilhoes_duplas_estrelas(sorteios)

    return resultados


def ranking_vencedores_jackpot(sorteios):
    contagem = Counter()

    for s in sorteios:
        n = getattr(s, "num_vencedores_jackpot", None)
        if n is not None:
            contagem[n] += 1

    return dict(sorted(contagem.items(), key=lambda x: x[0]))



