from datetime import datetime, date
from typing import List
import pandas as pd

COLUNAS_DATA = [
    "Data Sorteio",
    "Data do Sorteio",
    "Data",
    "Dt Sorteio",
    "DATA SORTEIO",
]

MAPA_CONFIG = {
    "Mega-Sena": {
        "qtd_bolas": 6,
        "padrao_bola": "Bola{}",
        "col_jackpot": "Rateio 6 acertos",
        "col_ganhadores": "Ganhadores 6 acertos",
        "dupla": False,
    },
    "Quina": {
        "qtd_bolas": 5,
        "padrao_bola": "Bola{}",
        "col_jackpot": "Rateio 5 acertos",
        "col_ganhadores": "Ganhadores 5 acertos",
        "dupla": False,
    },
    "Lotofácil": {
        "qtd_bolas": 15,
        "padrao_bola": "Bola{}",
        "col_jackpot": "Rateio 15 acertos",
        "col_ganhadores": "Ganhadores 15 acertos",
        "dupla": False,
    },
    "Dupla Sena": {
        "qtd_bolas": 6,
        "dupla": True,
    },
}

# ------------------------------------------------------------
# Funções auxiliares
# ------------------------------------------------------------

def _parse_data_br(valor) -> date | None:
    if not valor or not isinstance(valor, str):
        return None

    valor = valor.strip()

    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(valor, fmt).date()
        except:
            pass

    return None


def _safe_int(x) -> int | None:
    try:
        return int(str(x).strip())
    except:
        return None


def _safe_int_zero(x) -> int:
    try:
        return int(str(x).strip())
    except:
        return 0


def _safe_str(x) -> str:
    if pd.isna(x):
        return ""
    return str(x).strip()


def extrair_cidade_uf(valor: str) -> tuple[str, str]:
    if not valor:
        return "", ""

    v = valor.strip().upper()

    if "CANAL" in v:
        return "", "CANAL ELETRÔNICO"

    if "/" in valor:
        cidade, uf = valor.rsplit("/", 1)
        return cidade.strip(), uf.strip().upper()

    return valor.strip(), ""


# ------------------------------------------------------------
# BUSCA ROBUSTA PARA DUPLA SENA
# ------------------------------------------------------------

def buscar_coluna_bola(row: pd.Series, i: int, n: int) -> int | None:
    """
    Busca robusta: encontra qualquer coluna que contenha:
    - número da bola (i)
    - número do sorteio (n)
    - palavras-chave como 'bola', 'dezena', 'sorteio'
    """
    i_str = str(i)
    n_str = str(n)

    for col in row.index:
        nome = (
            col.lower()
            .replace("º", "")
            .replace("-", " ")
            .replace("_", " ")
            .replace("  ", " ")
        )

        if (
            ("bola" in nome or "dezena" in nome)
            and i_str in nome
            and ("sorteio" in nome or "s " in nome or nome.endswith("s" + n_str))
            and n_str in nome
        ):
            try:
                return int(str(row[col]).strip())
            except:
                return None

    return None


# ------------------------------------------------------------
# NORMALIZADOR PRINCIPAL
# ------------------------------------------------------------

def normalizar_loteria(df: pd.DataFrame, nome: str) -> list[dict]:
    if nome not in MAPA_CONFIG:
        raise ValueError(f"Config para {nome} não encontrada.")

    config = MAPA_CONFIG[nome]
    resultados: List[dict] = []

    col_data = next((c for c in COLUNAS_DATA if c in df.columns), None)
    if not col_data:
        return []

    df["data_parsed"] = df[col_data].apply(_parse_data_br)
    df = df.dropna(subset=["data_parsed"])

    for _, row in df.iterrows():
        cidade, uf = extrair_cidade_uf(_safe_str(row.get("Cidade / UF", "")))

        base = {
            "data": row["data_parsed"],
            "concurso": _safe_str(row.get("Concurso", "")),
            "cidade": cidade,
            "uf": uf,
        }

        # ------------------------------------------------------------
        # DUPLA SENA — 2 SORTEIOS POR LINHA
        # ------------------------------------------------------------
        if config["dupla"]:
            for n in (1, 2):
                bolas = [
                    buscar_coluna_bola(row, i, n)
                    for i in range(1, config["qtd_bolas"] + 1)
                ]
                bolas = [b for b in bolas if b is not None]

                # Jackpot e ganhadores — busca flexível
                jackpot = ""
                ganhadores = 0

                for col in row.index:
                    nome = col.lower().replace("º", "").replace("-", " ")
                    if "rateio" in nome and "6" in nome and str(n) in nome:
                        jackpot = _safe_str(row[col])
                    if "ganhadores" in nome and "6" in nome and str(n) in nome:
                        ganhadores = _safe_int_zero(row[col])

                resultados.append({
                    **base,
                    "concurso": f"{base['concurso']}-{n}",
                    "principais": bolas,
                    "jackpot": jackpot,
                    "ganhadores": ganhadores,
                })

        # ------------------------------------------------------------
        # LOTERIAS NORMAIS
        # ------------------------------------------------------------
        else:
            bolas = [
                _safe_int(row.get(config["padrao_bola"].format(i)))
                for i in range(1, config["qtd_bolas"] + 1)
            ]
            bolas = [b for b in bolas if b is not None]

            resultados.append({
                **base,
                "principais": bolas,
                "jackpot": _safe_str(row.get(config["col_jackpot"], "")),
                "ganhadores": _safe_int_zero(row.get(config["col_ganhadores"], "")),
            })

    return resultados













