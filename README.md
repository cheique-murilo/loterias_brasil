# 🍀 Análise das loterias de Portugal

Um dashboard interativo desenvolvido em **Python** e **Streamlit** para análise estatística, visualização de tendências e histórico de sorteios das principais loterias de Portugal: **Euromilhões**, **Totoloto** e **Eurodreams**.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Online-brightgreen)

## 📊 Funcionalidades

- **Dashboard interativo:** Visão geral com KPIs de sorteios, curiosidades, acumulações e jackpots.

- **Análise Estatística:**
  - Frequência de números (mais e menos sorteados).
  - Identificação de combinações repetidas (Duplas, Trios).
  - Detecção de sequências consecutivas.

- **Visualização de dados:**
  - Gráficos de evolução do Jackpot.
  - Ranking de países vencedores.
  - Representação visual das bolas sorteadas.

- **Filtros inteligentes:** Filtragem dinâmica por intervalo de datas e/ou sorteios.

- **Cache de dados:** Carregamento otimizado usando `st.cache_data` para alta performance.

## 🛠️ Tecnologias utilizadas

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Manipulação de dados:** [Pandas](https://pandas.pydata.org/)
- **Visualização:** [Matplotlib](https://matplotlib.org/)
- **Excel engine:** OpenPyXL

## 📂 Estrutura do projeto
<!-- TREE_START -->

```text
📁 projeto_loterias
├── 📄 .gitignore
├── 📄 index.html
├── 📄 jogos_portugal.xlsx
├── 📄 lembrar.txt
├── 📄 README.md
├── 📄 requirements.txt
│
├── 📁 .streamlit
│   └── 📄 config.toml
│
├── 📁 app
│   ├── 📄 streamlit_app.py
│   └── 📄 __init__.py
│
├── 📁 estatisticas
│   ├── 📄 agregador.py
│   ├── 📄 atraso.py
│   ├── 📄 especiais.py
│   ├── 📄 frequencias.py
│   ├── 📄 jackpots.py
│   ├── 📄 paises.py
│   ├── 📄 repeticoes.py
│   ├── 📄 sequencias.py
│   └── 📄 __init__.py
│
├── 📁 logos
│   ├── 🖼️ eurodreams.PNG
│   ├── 🖼️ euromilhoes.PNG
│   ├── 🖼️ jogossantacasa.PNG
│   └── 🖼️ totoloto.PNG
│
├── 📁 modelos
│   ├── 📄 eurodreams.py
│   ├── 📄 euromilhoes.py
│   ├── 📄 loteria_base.py
│   ├── 📄 sorteio.py
│   ├── 📄 totoloto.py
│   └── 📄 __init__.py
│
├── 📁 servicos
│   ├── 📄 carregar.py
│   ├── 📄 construir.py
│   ├── 📄 normalizar.py
│   └── 📄 __init__.py
│
└── 📁 visualizacao
    ├── 📄 graficos.py
    ├── 📄 tabelas.py
    └── 📄 __init__.py
    ``` text

<!-- TREE_END -->

## 📊 Tabela Comparativa das Loterias de Portugal

| Loteria        | Ano de criação | Países participantes | Formato inicial              | Principais alterações                                                                 | Formato atual                                |
|----------------|----------------|----------------------|------------------------------|----------------------------------------------------------------------------------------|-----------------------------------------------|
| **Totoloto**   | 1985           | Portugal             | 6/49 + Suplementar           | 2011: reformulação total (5+1), novas categorias, 2 sorteios/semana                    | 5 números (1–49) + Número da Sorte (1–13)     |
| **EuroDreams** | 2023           | 9 países europeus    | 6/40 + Número de Sonho       | Nenhuma alteração até o momento                                                        | 6 números (1–40) + Número de Sonho (1–5)      |
| **Euromilhões**| 2004           | 9 países europeus    | 5/50 + 2 estrelas (1–9)      | 2011: 2 sorteios/semana; 2016: estrelas 1–12; jackpots maiores                         | 5 números (1–50) + 2 estrelas (1–12)          |


## Sempre a atualizar 🔄️

