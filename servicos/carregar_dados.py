# servicos/carregar_dados.py
import pandas as pd
from modelos.totoloto import Totoloto
from modelos.eurodreams import Eurodreams
from modelos.euromilhoes import Euromilhoes
from modelos.sorteio import Sorteio

def carregar_dados():
    df = pd.read_excel('dados_loterias.xlsx')

    # Dicionário que aceita nomes em minúsculo
    loterias = {
        'totoloto': Totoloto(),
        'eurodreams': Eurodreams(),
        'euromilhoes': Euromilhoes(),
        'euromilhões': Euromilhoes(),   # caso tenha acento
    }

    for _, row in df.iterrows():
        try:
            # Data
            data_raw = row['data']
            data_str = data_raw.strftime('%d/%m/%Y') if hasattr(data_raw, 'strftime') else str(data_raw)

            # Nome da loteria em minúsculo
            nome = str(row['loteria']).strip().lower()

            if nome not in loterias:
                continue

            sorteio = Sorteio(
                data=data_str,
                sorteio_id=str(row['sorteio']),
                loteria=nome,   # guarda como veio (minúsculo)
                numeros_sorteados=str(row['numeros_sorteados']),
                numeros_complementares=str(row['numeros_complementares']),
                acumulou=str(row['acumulou']).lower() == 'sim',
                premio=int(row['premio']) if pd.notna(row['premio']) else 0,
                jackpot=int(row['jackpot']) if pd.notna(row['jackpot']) else 0,
                paises=str(row.get('pais', '')).replace('nan', ''),
                vencedores=int(row['vencedores']) if pd.notna(row['vencedores']) else 0
            )

            # Adiciona SEM VALIDAÇÃO (para você ver os dados já)
            loterias[nome].adicionar_sorteio(sorteio)

        except Exception as e:
            print(f"Linha ignorada: {e}")
            continue

    total = sum(len(l.sorteios) for l in loterias.values())
    print(f"Carregamento concluído: {total} sorteios carregados")
    return loterias