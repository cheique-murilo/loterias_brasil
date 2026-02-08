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

# NOVA FUNÇÃO — trata valores separados por ;
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


def normalizar_loteria(df: pd.DataFrame, nome: str) -> list[dict]:
    if nome not in MAPA_CONFIG:
        raise ValueError(f"Config para {nome} não encontrada.")

    config = MAPA_CONFIG[nome]
    resultados = []

    col_data = next((c for c in COLUNAS_DATA if c in df.columns), None)
    if not col_data:
        return []

    df["data_parsed"] = df[col_data].apply(_parse_data_br)
    df = df.dropna(subset=["data_parsed"])

    for _, row in df.iterrows():
        data = row["data_parsed"]
        concurso = _safe_str(row.get("Concurso", ""))

        # LISTA DE CIDADES/UFs
        lista_cidades_ufs = extrair_lista_cidades_ufs(_safe_str(row.get("Cidade / UF", "")))

        # LISTA DE GANHADORES
        lista_ganhadores = [
            _safe_int_zero(x)
            for x in _safe_str(row.get(config.get("col_ganhadores", ""), "")).split(";")
        ]

        # Ajusta tamanhos
        while len(lista_ganhadores) < len(lista_cidades_ufs):
            lista_ganhadores.append(1)

        locais = []
        for (cidade, uf), g in zip(lista_cidades_ufs, lista_ganhadores):
            locais.append({
                "cidade": cidade,
                "uf": uf,
                "ganhadores": g
            })

        # BOLAS
        bolas = [
            _safe_int(row.get(config["padrao_bola"].format(i)))
            for i in range(1, config["qtd_bolas"] + 1)
        ]
        bolas = [b for b in bolas if b is not None]

        jackpot = _safe_str(row.get(config.get("col_jackpot", ""), ""))

        resultados.append({
            "data": data,
            "concurso": concurso,
            "principais": bolas,
            "jackpot": jackpot,
            "locais": locais,
            "ganhadores_total": sum(lista_ganhadores),
        })

    return resultados














