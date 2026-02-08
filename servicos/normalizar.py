from datetime import datetime, date
from typing import List
import pandas as pd

# ------------------------------------------------------------
# CONFIGURAÇÕES
# ------------------------------------------------------------

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
        "dupla": True,
    },
}

# ------------------------------------------------------------
# FUNÇÕES AUXILIARES
# ------------------------------------------------------------

def encontrar_coluna(df, *possiveis):
    """
    Procura uma coluna no DataFrame ignorando maiúsculas/minúsculas e espaços.
    Exemplo:
        encontrar_coluna(df, "Bola1 sorteio1", "Bola1 Sorteio 1")
    """
    colunas_norm = {c.lower().replace(" ", ""): c for c in df.columns}

    for p in possiveis:
        chave = p.lower().replace(" ", "")
        if chave in colunas_norm:
            return colunas_norm[chave]

    return None

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


def _safe_int_zero(x) -> int:
    try:
        return int(str(x).strip())
    except:
        return 0


def _safe_int(x):
    try:
        return int(str(x).strip())
    except:
        return None


def _safe_str(x) -> str:
    if pd.isna(x):
        return ""
    return str(x).strip()


# ------------------------------------------------------------
# TRATAR CIDADES/UF SEPARADAS POR ";"
# ------------------------------------------------------------

def extrair_lista_cidades_ufs(valor: str):
    if not valor:
        return []

    partes = [v.strip() for v in valor.split(";") if v.strip()]
    resultado = []

    for p in partes:
        p_up = p.upper()

        if "CANAL" in p_up:
            resultado.append(("", "CANAL ELETRÔNICO"))
            continue

        if "/" in p:
            cidade, uf = p.rsplit("/", 1)
            resultado.append((cidade.strip(), uf.strip().upper()))
        else:
            resultado.append((p.strip(), ""))

    return resultado


# ------------------------------------------------------------
# NORMALIZADOR PRINCIPAL
# ------------------------------------------------------------

def normalizar_loteria(df: pd.DataFrame, nome: str) -> list[dict]:
    if nome not in MAPA_CONFIG:
        raise ValueError(f"Config para {nome} não encontrada.")

    config = MAPA_CONFIG[nome]
    resultados = []

    # Identificar coluna de data
    col_data = next((c for c in COLUNAS_DATA if c in df.columns), None)
    if not col_data:
        return []

    df["data_parsed"] = df[col_data].apply(_parse_data_br)
    df = df.dropna(subset=["data_parsed"])


    # CASO ESPECIAL: DUPLA SENA (ROBUSTO E FLEXÍVEL)
    # ------------------------------------------------------------
    if config.get("dupla", False):

        for _, row in df.iterrows():
            data = row["data_parsed"]
            concurso = _safe_str(row.get("Concurso", ""))

            # -------------------------
            # SORTEIO 1
            # -------------------------
            bolas_1 = []
            for i in range(1, 7):
                col = encontrar_coluna(
                    df,
                    f"Bola{i} sorteio1",
                    f"Bola{i} sorteio 1",
                    f"Bola{i} Sorteio1",
                    f"Bola{i} Sorteio 1",
                )
                bolas_1.append(_safe_int(row.get(col)))

            bolas_1 = [b for b in bolas_1 if b is not None]

            col_ganh_1 = encontrar_coluna(
                df,
                "Ganhadores 6 acertos Sorteio1",
                "Ganhadores 6 acertos sorteio1",
            )
            col_rateio_1 = encontrar_coluna(
                df,
                "Rateio 6 acertos Sorteio1",
                "Rateio 6 acertos sorteio1",
            )
            col_cidade = encontrar_coluna(df, "Cidade / UF", "Cidade/UF")

            ganhadores_1 = _safe_int_zero(row.get(col_ganh_1))
            jackpot_1 = _safe_str(row.get(col_rateio_1))
            lista_cidades_ufs = extrair_lista_cidades_ufs(_safe_str(row.get(col_cidade)))

            locais_1 = []
            if ganhadores_1 > 0 and lista_cidades_ufs:
                qtd = len(lista_cidades_ufs)
                base = ganhadores_1 // qtd
                resto = ganhadores_1 % qtd

                for idx, (cidade, uf) in enumerate(lista_cidades_ufs):
                    g = base + (1 if idx < resto else 0)
                    locais_1.append({"cidade": cidade, "uf": uf, "ganhadores": g})

            resultados.append({
                "data": data,
                "concurso": f"{concurso}-1",
                "principais": bolas_1,
                "jackpot": jackpot_1,
                "locais": locais_1,
                "ganhadores_total": ganhadores_1,
            })

            # -------------------------
            # SORTEIO 2
            # -------------------------
            bolas_2 = []
            for i in range(1, 7):
                col = encontrar_coluna(
                    df,
                    f"Bola{i} Sorteio2",
                    f"Bola{i} sorteio2",
                    f"Bola{i} Sorteio 2",
                    f"Bola{i} sorteio 2",
                )
                bolas_2.append(_safe_int(row.get(col)))

            bolas_2 = [b for b in bolas_2 if b is not None]

            col_ganh_2 = encontrar_coluna(df, "Ganhadores 6 acertos Sorteio2")
            col_rateio_2 = encontrar_coluna(df, "Rateio 6 acertos Sorteio2")

            ganhadores_2 = _safe_int_zero(row.get(col_ganh_2))
            jackpot_2 = _safe_str(row.get(col_rateio_2))

            resultados.append({
                "data": data,
                "concurso": f"{concurso}-2",
                "principais": bolas_2,
                "jackpot": jackpot_2,
                "locais": [],
                "ganhadores_total": ganhadores_2,
            })

        return resultados


    # ------------------------------------------------------------
    # LOTERIAS NORMAIS
    # ------------------------------------------------------------
    for _, row in df.iterrows():
        data = row["data_parsed"]
        concurso = _safe_str(row.get("Concurso", ""))

        bolas = [
            _safe_int(row.get(config["padrao_bola"].format(i)))
            for i in range(1, config["qtd_bolas"] + 1)
        ]
        bolas = [b for b in bolas if b is not None]

        jackpot = _safe_str(row.get(config["col_jackpot"], ""))
        ganhadores = _safe_int_zero(row.get(config["col_ganhadores"], ""))

        lista_cidades_ufs = extrair_lista_cidades_ufs(_safe_str(row.get("Cidade / UF", "")))

        locais = []
        if ganhadores > 0 and lista_cidades_ufs:
            qtd = len(lista_cidades_ufs)
            base = ganhadores // qtd
            resto = ganhadores % qtd

            for idx, (cidade, uf) in enumerate(lista_cidades_ufs):
                g = base + (1 if idx < resto else 0)
                locais.append({"cidade": cidade, "uf": uf, "ganhadores": g})

        resultados.append({
            "data": data,
            "concurso": concurso,
            "principais": bolas,
            "jackpot": jackpot,
            "locais": locais,
            "ganhadores_total": ganhadores,
        })

    return resultados
















