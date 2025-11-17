
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict
from modelos.loteria import Loteria

class VisualGraficos:
    @staticmethod
    def evolucao_jackpot(loterias: Dict[str, Loteria], salvar=False):
        fig, ax = plt.subplots(figsize=(12, 6))
        tem_dados = False
        for nome, loteria in loterias.items():
            df = loteria.to_dataframe()
            if df.empty or 'jackpot' not in df.columns:
                continue
            df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
            df = df[df['jackpot'] > 0].sort_values('data')
            if not df.empty:
                ax.plot(df['data'], df['jackpot'], label=nome, marker='o')
                tem_dados = True
        if tem_dados:
            plt.title('Evolução do Jackpot')
            plt.legend()
            plt.grid(True, alpha=0.3)
        else:
            ax.text(0.5, 0.5, 'Sem dados de jackpot', ha='center', va='center')
        plt.tight_layout()
        if salvar:
            plt.savefig('jackpot_evolucao.png', dpi=300)
        return fig

    @staticmethod
    def ranking_paises(premios: Dict[str, int], salvar=False):
        if not premios:
            return plt.gcf()
        df = pd.DataFrame(list(premios.items()), columns=['País', 'Total'])
        df = df.sort_values('Total', ascending=False)
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.barh(df['País'], df['Total'])
        plt.title('Ranking de Premiações por País')
        plt.tight_layout()
        if salvar:
            plt.savefig('ranking_paises.png', dpi=300)
        return fig