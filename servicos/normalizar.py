import pandas as pd
import re

def _extrair_numeros(txt) -> list[int]:
    if pd.isna(txt):
        return []
    return [int(n) for n in re.findall(r"\d+", str(txt))]


def _normalizar_pais(valor) -> str:
    if pd.isna(valor):
        return ""
    txt = str(valor).strip()
    if not txt:
        return ""
    partes = [p.strip().title() for p in txt.split(",") if p.strip()]
    return ", ".join(partes)


def _formatar_jackpot(valor) -> str:
    """
    Converte valores crus como '1000000' em '€1.000.000,00'.
    """
    txt = str(valor).strip()
    txt = re.sub(r"[^\d]", "", txt)

    if not txt:
        return "€0,00"

    numero = int(txt)

    return f"€{numero:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# 🔥 CORREÇÃO CRÍTICA: jackpot para inteiro sem multiplicações indevidas
def _jackpot_para_int(valor) -> int:
    if pd.isna(valor):
        return 0

    txt = str(valor).strip()

    # remove espaços
    txt = txt.replace(" ", "")

    # remove separadores de milhar e decimais
    txt = txt.replace(".", "").replace(",", "")

    # remove qualquer coisa que não seja número
    txt = re.sub(r"[^\d]", "", txt)

    return int(txt) if txt else 0


def normalizar_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["loteria_norm"] = (
        df["loteria"]
        .astype(str)
        .str.strip()
        .str.title()
        .replace({"Euromilhoes": "Euromilhões"})
    )

    df["data_dt"] = pd.to_datetime(df["data"], errors="coerce")
    df = df[df["data_dt"].notna()]

    df["principais"] = df["numeros_sorteados"].apply(_extrair_numeros)

    def parse_complementares(row):
        txt = str(row["numeros_complementares"]).strip()

        if row["loteria_norm"] == "Euromilhões":
            txt = txt.replace(" ", "").replace(".", ",")
            if "," in txt:
                a, b = txt.split(",", 1)
                return [int(a), int(b)]
            return _extrair_numeros(txt)

        return _extrair_numeros(txt)

    df["complementares"] = df.apply(parse_complementares, axis=1)

    # jackpot formatado
    df["jackpot_fmt"] = df["jackpot"].apply(_formatar_jackpot)

    # jackpot inteiro (corrigido)
    df["jackpot_int"] = df["jackpot"].apply(_jackpot_para_int)

    if "acumulou" in df.columns:
        df["acumulou_bool"] = (
            df["acumulou"]
            .astype(str)
            .str.strip()
            .str.lower()
            .isin(["true", "1", "sim", "s", "yes", "y"])
        )
    else:
        df["acumulou_bool"] = False

    if "pais_vencedor" in df.columns:
        df["pais"] = df["pais_vencedor"].apply(_normalizar_pais)
    else:
        df["pais"] = ""

    if "num_vencedores_jackpot" in df.columns:
        df["num_vencedores_jackpot"] = (
            df["num_vencedores_jackpot"]
            .astype(str)
            .str.replace(r"[^\d]", "", regex=True)
            .replace("", "0")
            .astype(int)
        )
    else:
        df["num_vencedores_jackpot"] = 0

    return df

