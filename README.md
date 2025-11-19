# 🍀 Análise de Loterias de Portugal

Um dashboard interativo desenvolvido em **Python** e **Streamlit** para análise estatística, visualização de tendências e histórico de sorteios das principais loterias de Portugal: **Euromilhões**, **Totoloto** e **Eurodreams**.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://seu-link-do-deploy-aqui.streamlit.app)

## 📊 Funcionalidades

- **Dashboard Interativo:** Visão geral com KPIs de sorteios, acumulações e jackpots.
- **Análise Estatística:**
  - Frequência de números (mais e menos sorteados).
  - Identificação de combinações repetidas (Duplas, Trios).
  - Detecção de sequências consecutivas.
- **Visualização de Dados:**
  - Gráficos de evolução do Jackpot.
  - Ranking de países vencedores.
  - Representação visual das bolas sorteadas.
- **Filtros Inteligentes:** Filtragem dinâmica por intervalo de datas.
- **Cache de Dados:** Carregamento otimizado usando `st.cache_data` para alta performance.

## 🛠️ Tecnologias Utilizadas

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Manipulação de Dados:** [Pandas](https://pandas.pydata.org/)
- **Visualização:** [Matplotlib](https://matplotlib.org/)
- **Excel Engine:** OpenPyXL

## 📂 Estrutura do Projeto

O projeto foi refatorado seguindo o padrão MVC (Model-View-Controller) adaptado para scripts de dados:

```text
├── 📂 modelos/             # Definição das Classes (OOP)
│   ├── loteria_base.py     # Classe Abstrata com regras de validação
│   ├── sorteio.py          # Dataclass imutável do Sorteio
│   ├── euromilhoes.py      # Regras específicas (5+2)
│   ├── totoloto.py         # Regras específicas (5+1)
│   └── eurodreams.py       # Regras específicas (6+1)
│
├── 📂 servicos/            # Lógica de Negócio e I/O
│   ├── carregar_dados.py   # Leitura robusta de Excel/CSV
│   ├── validador.py        # Limpeza e Factory de objetos
│   ├── calculos_estatisticos.py # Matemática e Agregações
│   └── filtros.py          # Utilitários de filtro
│
├── 📂 visualizacao/        # Preparação de Dados para UI
│   ├── visual_graficos.py  # Dados para Matplotlib
│   └── visual_tabelas.py   # Dados para tabelas HTML
│
├── 📂 imagens/             # Assets (Logos)
├── dados_loterias.xlsx     # Base de dados (Excel)
├── streamlit_app.py        # Aplicação Principal (Entry Point)
└── requirements.txt        # Dependências