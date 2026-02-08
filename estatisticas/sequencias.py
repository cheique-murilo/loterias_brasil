from typing import Iterable, List, Dict, Any
from collections import defaultdict
from modelos.sorteio import Sorteio


def sequencias_consecutivas(sorteios: Iterable[Sorteio]) -> List[Dict[str, Any]]:
    """
    Identifica sequências de números consecutivos dentro de cada sorteio.
    Agrupa sequências iguais e conta ocorrências.
    Compatível com Dupla Sena (sorteios 1 e 2 são independentes).
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
            "concursos": sorted(concursos),
        })

    # 3. Ordenar por:
    #   1) tamanho da sequência (desc)
    #   2) número de ocorrências (desc)
    #   3) sequência (asc)
    resultados.sort(
        key=lambda x: (-x["tamanho"], -x["ocorrencias"], x["sequencia"])
    )

    return resultados







