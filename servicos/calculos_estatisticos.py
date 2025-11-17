# servicos/calculo_estatisticos.py
from typing import List, Tuple, Dict, Any
from collections import Counter
from itertools import combinations
from modelos.loteria import Loteria

class CalculosEstatisticos:
    def __init__(self, loteria: Loteria):
        self.loteria = loteria

    def _todos_numeros(self, tipo: str = 'principais') -> List[int]:
        if tipo == 'principais':
            return [n for s in self.loteria.sorteios for n in s.numeros_sorteados]
        return [n for s in self.loteria.sorteios for n in s.numeros_complementares]

    def _frequencia(self, tipo: str = 'principais') -> Counter:
        return Counter(self._todos_numeros(tipo))

    def _repeticoes_conjuntos(self, tamanho: int = 2) -> List[Tuple[Tuple[int, ...], int]]:
        contador = Counter()
        for sorteio in self.loteria.sorteios:
            nums = tuple(sorted(sorteio.numeros_sorteados))
            for combo in combinations(nums, tamanho):
                contador[combo] += 1
        return [(combo, count) for combo, count in contador.most_common(10) if count >= 2]

    def _sequencias_consecutivas(self) -> Dict[str, Any]:
        if not self.loteria.sorteios:
            return {'contagem_total': 0, 'sorteios_com_sequencia': []}
        total = 0
        ocorrencias = []
        for sorteio in self.loteria.sorteios:
            nums = sorted(sorteio.numeros_sorteados)
            i = 0
            while i < len(nums):
                start = i
                while i + 1 < len(nums) and nums[i + 1] == nums[i] + 1:
                    i += 1
                if i - start + 1 >= 3:
                    seq = tuple(nums[start:i + 1])
                    total += 1
                    ocorrencias.append((sorteio.sorteio_id, seq))
                i += 1
        return {
            'contagem_total': total,
            'sorteios_com_sequencia': ocorrencias[:10]
        }

    def _streak_acumulacoes(self) -> int:
        if not self.loteria.sorteios:
            return 0
        max_streak = current = 0
        for s in sorted(self.loteria.sorteios, key=lambda x: x.data):
            if s.acumulou:
                current += 1
                max_streak = max(max_streak, current)
            else:
                current = 0
        return max_streak

    def _jackpots_divididos(self) -> Dict[int, int]:
        contagem = Counter()
        for s in self.loteria.sorteios:
            if s.jackpot and not s.acumulou and s.vencedores > 1:
                contagem[s.vencedores] += 1
        return dict(contagem)

    def _premios_por_pais(self) -> Dict[str, int]:
        total = Counter()
        for s in self.loteria.sorteios:
            if s.premio:
                for pais in s.paises:
                    total[pais] += s.premio
        return dict(total)

    def calculos_estatisticos(self) -> Dict[str, Any]:
        freq_princ = self._frequencia('principais')
        freq_comp = self._frequencia('complementares')

        return {
            'nome': self.loteria.nome,
            'total_sorteios': len(self.loteria.sorteios),

            # Sempre existem (lista vazia se 0 sorteios)
            'numeros_mais_sairam': freq_princ.most_common(10) if freq_princ else [],
            'numeros_menos_sairam': sorted(freq_princ.items(), key=lambda x: x[1])[:10] if freq_princ else [],
            'estrelas_mais_sairam': freq_comp.most_common(10) if freq_comp else [],
            'estrelas_menos_sairam': sorted(freq_comp.items(), key=lambda x: x[1])[:10] if freq_comp else [],

            'duplas_repetidas': self._repeticoes_conjuntos(2),
            'trios_repetidos': self._repeticoes_conjuntos(3),
            'quadras_repetidas': self._repeticoes_conjuntos(4),

            'sequencias_consecutivas': self._sequencias_consecutivas(),

            'total_acumulacoes': sum(1 for s in self.loteria.sorteios if s.acumulou),
            'streak_max_acumulacoes': self._streak_acumulacoes(),

            'jackpots_divididos': self._jackpots_divididos(),
            'premios_por_pais': self._premios_por_pais(),
        }