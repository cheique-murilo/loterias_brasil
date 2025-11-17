# visualizacao/visual_tabelas.py
import streamlit as st
import pandas as pd
from modelos.loteria import Loteria

class VisualTabelas:
    @staticmethod
    def _to_dataframe(loteria: Loteria) -> pd.DataFrame:
        if not loteria.sorteios:
            return pd.DataFrame()
        return pd.DataFrame([{
            'data': s.data.strftime('%d/%m/%Y'),
            'sorteio_id': s.sorteio_id,
            'numeros_sorteados': ', '.join(map(str, s.numeros_sorteados)),
            'numeros_complementares': ', '.join(map(str, s.numeros_complementares)),
            'acumulou': 'Sim' if s.acumulou else 'Não',
            'jackpot': s.jackpot or 0,
            'vencedores': s.vencedores
        } for s in loteria.sorteios])

    @staticmethod
    def ultimos_sorteios(loteria: Loteria):
        df = VisualTabelas._to_dataframe(loteria).tail(5)
        st.subheader("Últimos 5 sorteios")
        if df.empty:
            st.info("Nenhum sorteio carregado.")
        else:
            st.dataframe(df, width='stretch', hide_index=True)

    @staticmethod
    def numeros_mais_menos(stats):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Números mais saíram**")
            df = pd.DataFrame(stats['numeros_mais_sairam'], columns=["Número", "Vezes"]) if stats['numeros_mais_sairam'] else pd.DataFrame()
            if df.empty:
                st.info("Nenhum dado")
            else:
                st.dataframe(df, width='stretch', hide_index=True)
        with col2:
            st.markdown("**Números menos saíram**")
            df = pd.DataFrame(stats['numeros_menos_sairam'], columns=["Número", "Vezes"]) if stats['numeros_menos_sairam'] else pd.DataFrame()
            if df.empty:
                st.info("Nenhum dado")
            else:
                st.dataframe(df, width='stretch', hide_index=True)

    @staticmethod
    def combinacoes_repetidas(stats):
        st.subheader("Sequências Mais Comuns")
        tab1, tab2, tab3 = st.tabs(["Duplas", "Trios", "Quadras"])
        with tab1:
            df = pd.DataFrame(stats['duplas_repetidas'], columns=["Dupla", "Vezes"]) if stats['duplas_repetidas'] else pd.DataFrame()
            if df.empty:
                st.info("Nenhuma")
            else:
                st.dataframe(df, width='stretch', hide_index=True)
        with tab2:
            df = pd.DataFrame(stats['trios_repetidos'], columns=["Trio", "Vezes"]) if stats['trios_repetidos'] else pd.DataFrame()
            if df.empty:
                st.info("Nenhuma")
            else:
                st.dataframe(df, width='stretch', hide_index=True)
        with tab3:
            df = pd.DataFrame(stats['quadras_repetidas'], columns=["Quadra", "Vezes"]) if stats['quadras_repetidas'] else pd.DataFrame()
            if df.empty:
                st.info("Nenhuma")
            else:
                st.dataframe(df, width='stretch', hide_index=True)

    @staticmethod
    def sequencias_consecutivas(stats):
        st.subheader("🔢 Sequências Consecutivas")
        seq = stats['sequencias_consecutivas']
        if seq['contagem_total'] > 0:
            st.metric("Total encontradas", seq['contagem_total'])
            df = pd.DataFrame(seq['sorteios_com_sequencia'], columns=["Sorteio", "Sequência"])
            st.dataframe(df, width='stretch', hide_index=True)
        else:
            st.info("Nenhuma sequência consecutiva encontrada.")