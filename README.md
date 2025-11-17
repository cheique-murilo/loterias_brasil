# Análise de Loterias Portuguesas

Projeto em Python para gerar informações estatísticas sobre as loterias de Portugal (Totoloto, Eurodreams, Euromilhões).

## Como Rodar
1. Instale dependências: "pip install -r requirements.txt"
2. Coloque as informações dos sorteios ("dados_loterias.xlsx") na raiz do sistema.
3. Rode "python streamlit_app.py" para gerar curiosidades estatísticas sobre cada loteria.

## Web App
Rode "streamlit run streamlit_app.py" para versão interativa com filtros.

## Estrutura
- modelos/: classes para Sorteio e Loterias.
- servicos/: carregamento dos dados, validações e cálculos estatísticos.
- visualizacao/: métodos para gerar tabelas e gráficos
- streamlit_app.py: execução principal.

Dependências: pandas, openpyxl, matplotlib, seaborn (verificar requirements)
