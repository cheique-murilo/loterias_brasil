import os
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.join(ROOT, "base")

MAPA_ARQUIVOS = {
    "Mega-Sena": "Mega_Sena.xlsx",
    "Quina": "Quina.xlsx",
    "Dupla Sena": "Dupla_Sena.xlsx",
    "Lotofácil": "Lotofácil.xlsx",
}

def carregar_dados_loteria(nome: str) -> pd.DataFrame:
    if nome not in MAPA_ARQUIVOS:
        raise ValueError(f"Loteria {nome} não encontrada.")

    caminho = os.path.join(BASE_DIR, MAPA_ARQUIVOS[nome])
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo {caminho} não encontrado.")

    df = pd.read_excel(caminho, dtype=str)

    df = df.dropna(axis=1, how="all")
    df = df.dropna(axis=0, how="all")
    df.columns = [c.strip() for c in df.columns]

    return df











