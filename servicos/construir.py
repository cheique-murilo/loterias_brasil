from typing import Dict
from modelos.sorteio import Sorteio
from modelos.totoloto import Totoloto
from modelos.eurodreams import Eurodreams
from modelos.euromilhoes import Euromilhoes
from .carregar import carregar_dados_brutos
from .normalizar import normalizar_df

def construir_loterias(df_norm) -> Dict[str, object]:
    loterias = {
        "Totoloto": Totoloto(),
        "Eurodreams": Eurodreams(),
        "Euromilhões": Euromilhoes(),
    }

    for _, row in df_norm.iterrows():
        nome = row["loteria_norm"]
        if nome not in loterias:
            continue

        sorteio = Sorteio(
            data=row["data_dt"],
            concurso=str(row["sorteio"]),
            principais=row["principais"],
            complementares=row["complementares"],
            acumulou=row["acumulou_bool"],
            jackpot=row["jackpot_int"],
            jackpot_fmt=row["jackpot_fmt"],
            paises_ganhadores=row["pais"],
            num_vencedores_jackpot=row["num_vencedores_jackpot"],
        )

        loterias[nome].adicionar(sorteio)

    return loterias


def carregar_e_processar_loterias() -> Dict[str, object]:
    df = carregar_dados_brutos()
    if df.empty:
        return {}

    df_norm = normalizar_df(df)
    return construir_loterias(df_norm)
