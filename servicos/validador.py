# servicos/validador.py
from __future__ import annotations
from modelos.sorteio import Sorteio

class Validador:
    @staticmethod
    def validar(sorteio: Sorteio, loteria) -> bool:
        nome = loteria.nome

        qtd_princ = len(sorteio.numeros_sorteados)
        qtd_comp = len(sorteio.numeros_complementares)

        if nome == "Euromilhões":
            if qtd_princ != 5 or qtd_comp != 2: return False
        elif nome == "Totoloto":
            if qtd_princ != 5 or qtd_comp != 1: return False
        elif nome == "Eurodreams":
            if qtd_princ != 6 or qtd_comp != 1: return False
        else:
            return False

        min_p, max_p = loteria.faixa_principais
        min_c, max_c = loteria.faixa_complementares

        if not all(min_p <= n <= max_p for n in sorteio.numeros_sorteados): return False
        if not all(min_c <= n <= max_c for n in sorteio.numeros_complementares): return False

        if len(set(sorteio.numeros_sorteados)) != qtd_princ: return False
        if len(set(sorteio.numeros_complementares)) != qtd_comp: return False

        return True