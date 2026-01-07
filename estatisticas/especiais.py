from collections import Counter
from typing import Iterable, Dict, Any
from modelos.sorteio import Sorteio


def _comparativo(f_geral: Counter, f_jack: Counter) -> Dict[str, Any]:
    """
    Estrutura padronizada para comparativos de números especiais.

    Retorna:
        {
            "geral": (valor, qtd) ou None,
            "jackpots": (valor, qtd) ou None,
            "frequencias_geral": {valor: qtd, ...},
            "frequencias_jackpots": {valor: qtd, ...},
        }
    """
    mais_geral = f_geral.most_common(1)[0] if f_geral else None
    mais_jack = f_jack.most_common(1)[0] if f_jack else None

    return {
        "geral": mais_geral,
        "jackpots": mais_jack,
        "frequencias_geral": dict(f_geral),
        "frequencias_jackpots": dict(f_jack),
    }


# ============================================================
# Totoloto — Número da Sorte (complementar único)
# ============================================================

def totoloto_numero_sorte(sorteios: Iterable[Sorteio]) -> Dict[str, Any]:
    """
    Totoloto:
      - usa o primeiro número em `complementares` como Número da Sorte.
      - "em jackpots" = sorteios onde NÃO acumulou (independente de valor).
    """
    # Frequência geral de número da sorte
    comp_geral = Counter(
        s.complementares[0]
        for s in sorteios
        if s.complementares
    )

    # Frequência apenas em jackpots pagos (não acumulou)
    comp_jack = Counter(
        s.complementares[0]
        for s in sorteios
        if s.complementares and not s.acumulou
    )

    return _comparativo(comp_geral, comp_jack)


# ============================================================
# Eurodreams — Número do Sonho (complementar único)
# ============================================================

def eurodreams_sonho(sorteios: Iterable[Sorteio]) -> Dict[str, Any]:
    """
    Eurodreams:
      - usa o primeiro número em `complementares` como Número do Sonho.
      - "em jackpots" = sorteios onde NÃO acumulou.
    """
    comp_geral = Counter(
        s.complementares[0]
        for s in sorteios
        if s.complementares
    )

    comp_jack = Counter(
        s.complementares[0]
        for s in sorteios
        if s.complementares and not s.acumulou
    )

    return _comparativo(comp_geral, comp_jack)


# ============================================================
# Euromilhões — Estrelas (lista de complementares)
# ============================================================

def euromilhoes_estrelas(sorteios: Iterable[Sorteio]) -> Dict[str, Any]:
    """
    Euromilhões:
      - usa todos os números de `complementares` como Estrelas.
      - "em jackpots" = sorteios onde NÃO acumulou.
    """
    comp_geral = Counter(
        n
        for s in sorteios
        for n in s.complementares
    )

    comp_jack = Counter(
        n
        for s in sorteios
        if not s.acumulou
        for n in s.complementares
    )

    return _comparativo(comp_geral, comp_jack)


# ============================================================
# Euromilhões — Duplas de Estrelas
# ============================================================

def euromilhoes_duplas_estrelas(sorteios: Iterable[Sorteio]) -> Dict[str, Any]:
    """
    Euromilhões:
      - considera apenas sorteios com exatamente 2 estrelas em `complementares`.
      - duplas são ordenadas (ex.: (2, 7)).
      - "em jackpots" = sorteios onde NÃO acumulou.
    """
    geral = Counter()
    jack = Counter()

    for s in sorteios:
        if len(s.complementares) == 2:
            dupla = tuple(sorted(s.complementares))
            geral[dupla] += 1

            if not s.acumulou:
                jack[dupla] += 1

    return _comparativo(geral, jack)

