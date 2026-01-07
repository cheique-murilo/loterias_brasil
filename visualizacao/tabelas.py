from typing import List, Dict, Any
from modelos.loteria_base import LoteriaBase

def dados_ultimos_sorteios(loteria: LoteriaBase) -> List[Dict[str, Any]]:
    ultimos = loteria.ultimos_5
    dados = []
    for s in reversed(ultimos):  # mais recente primeiro
        dados.append(
            {
                "data": s.data,
                "data_str": s.data.strftime("%d/%m/%Y"),
                "concurso": s.concurso,
                "principais": s.principais,
                "complementares": s.complementares,
                "acumulou": s.acumulou,
                "label_complementar": loteria.label_complementar,
                "nome_loteria": loteria.nome,
            }
        )
    return dados
