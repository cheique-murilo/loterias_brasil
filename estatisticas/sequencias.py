from typing import Iterable, List, Dict, Any
from modelos.sorteio import Sorteio

def sequencias_consecutivas(
    sorteios: Iterable[Sorteio], min_tamanho: int = 3, limite: int = 1000
) -> List[Dict[str, Any]]:
    """
    Retorna lista de dicts:
      { "data": ..., "concurso": ..., "sequencia": [1,2,3] }
    """
    ocorrencias = []
    for s in sorteios:
        nums = s.principais
        i = 0
        while i < len(nums):
            inicio = i
            while i + 1 < len(nums) and nums[i + 1] == nums[i] + 1:
                i += 1
            if i - inicio + 1 >= min_tamanho:
                ocorrencias.append(
                    {
                        "data": s.data,
                        "concurso": s.concurso,
                        "sequencia": nums[inicio : i + 1],
                    }
                )
            i += 1
    return ocorrencias[-limite:]

