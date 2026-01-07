import os
import pandas as pd
import streamlit as st

CAMINHO_ARQUIVO = "jogos_portugal.xlsx"

@st.cache_data(show_spinner="Lendo Excel...")
def carregar_dados_brutos() -> pd.DataFrame:
    """Lê o Excel como texto, sem nenhuma lógica de negócio."""
    if not os.path.exists(CAMINHO_ARQUIVO):
        st.error(f"Arquivo {CAMINHO_ARQUIVO} não encontrado.")
        return pd.DataFrame()

    try:
        df = pd.read_excel(
            CAMINHO_ARQUIVO,
            dtype={
                "jackpot": str,                 # <--- ESSENCIAL
                "numeros_sorteados": str,
                "num_vencedores_jackpot": str,
                "numeros_complementares": str,
                "pais_vencedor": str,
                "acumulou": str,
            }
        )

        return df

    except Exception as e:
        st.error(f"Erro ao ler Excel: {e}")
        return pd.DataFrame()

