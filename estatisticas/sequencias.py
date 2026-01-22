from typing import Iterable, List, Dict, Any
from modelos.sorteio import Sorteio
from collections import defaultdict


def sequencias_consecutivas(sorteios: Iterable[Sorteio]) -> List[Dict[str, Any]]:
    """
    1. Encontra sequências de números consecutivos dentro de cada sorteio.
    2. Agrupa sequências iguais.
    3. Conta quantas vezes cada sequência apareceu.
    4. Lista os concursos onde cada sequência ocorreu.

    Retorna:
        {
            "sequencia": [10, 11, 12],
            "tamanho": 3,
            "ocorrencias": 4,
            "concursos": ["1234-1", "1450-2", "1780-1", "2001-2"]
        }
    """
    grupos = defaultdict(list)  # seq_tuple -> lista de concursos

    # 1. Extrair sequências por sorteio
    for s in sorteios:
        nums = sorted(set(s.principais))
        if len(nums) < 3:
            continue

        atual = [nums[0]]

        for n in nums[1:]:
            if n == atual[-1] + 1:
                atual.append(n)
            else:
                if len(atual) >= 3:
                    grupos[tuple(atual)].append(s.concurso)
                atual = [n]

        if len(atual) >= 3:
            grupos[tuple(atual)].append(s.concurso)

    # 2. Montar resultado final
    resultados = []
    for seq, concursos in grupos.items():
        resultados.append({
            "sequencia": list(seq),
            "tamanho": len(seq),
            "ocorrencias": len(concursos),
            "concursos": concursos,
        })

    # 3. Ordenar por:
   
    resultados.sort(
        key=lambda x: (-x["tamanho"])
    )

    return resultados






