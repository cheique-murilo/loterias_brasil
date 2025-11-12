
import sys
from os.path import join, dirname, abspath
import pandas as pd
from typing import Dict, Optional

projeto_root = abspath(join(dirname(__file__), '..'))
sys.path.insert(0, projeto_root)

from modelos.sorteio import Sorteio
from modelos.loteria import Loteria
from modelos.totoloto import Totoloto
from modelos.eurodreams import Eurodreams
from modelos.euromilhoes import Euromilhoes


class FonteDados:
    def __init__(self, caminho_arquivo: str):
        self.caminho = caminho_arquivo
        self.loterias: Dict[str, Loteria] = {
            'Totoloto': Totoloto(),
            'Eurodreams': Eurodreams(),
            'Euromilhões': Euromilhoes()
        }

    def carregar_dados(self) -> Dict[str, Loteria]:
        df = pd.read_excel(self.caminho)
        print(f"Excel carregado: {len(df)} linhas lidas.")
        for _, row in df.iterrows():
            try:
                # Data: Timestamp → date string
                data_raw = row['data']
                data_str = data_raw.strftime('%d/%m/%Y') if hasattr(data_raw, 'strftime') else str(data_raw)

                # Complementares: Handle float/string
                comp_raw = str(row['numeros_complementares']).strip()
                if '.' in comp_raw:
                    nums_comp = [int(float(p)) for p in comp_raw.split('.')]
                else:
                    nums_comp = [int(float(comp_raw))] if comp_raw and comp_raw != 'nan' else []
                comp_str = ','.join(map(str, nums_comp)) if len(nums_comp) > 1 else str(nums_comp[0]) if nums_comp else ''

                acumulou_str = str(row['acumulou']).lower()
                paises_str = str(row.get('pais', '')).replace('nan', '')

                sorteio = Sorteio(
                    data=data_str,
                    sorteio_id=str(row['sorteio']),
                    loteria=str(row['loteria']),
                    numeros_sorteados=str(row['numeros_sorteados']),
                    numeros_complementares=comp_str,
                    acumulou=acumulou_str,
                    premio=int(row['premio']) if pd.notna(row['premio']) else None,
                    jackpot=int(row['jackpot']) if pd.notna(row['jackpot']) else None,
                    paises=paises_str,
                    vencedores=int(row['vencedores'])
                )

                nome_loteria = self._normalizar_loteria(sorteio.loteria)
                if nome_loteria in self.loterias:
                    self.loterias[nome_loteria].adicionar_sorteio(sorteio)
            except Exception:
                continue  # Ignora erros – lê o que pode

        print("Sorteios adicionados!")
        return self.loterias

    def _normalizar_loteria(self, loteria: str) -> str:
        normalized = loteria.strip().title()
        normalized = normalized.replace('Euromilhao', 'Euromilhões').replace('Euromilhoes', 'Euromilhões')
        return normalized 