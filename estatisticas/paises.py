from collections import Counter
from modelos.sorteio import Sorteio

def premios_por_pais(sorteios: list[Sorteio]) -> dict[str, int]:
    cont = Counter()
    for s in sorteios:
        if not s.acumulou and s.jackpot > 0:
            paises = [p.strip().title() for p in s.paises_ganhadores.split(",") if p.strip()]
            for p in paises:
                cont[p] += 1
    return dict(cont)


