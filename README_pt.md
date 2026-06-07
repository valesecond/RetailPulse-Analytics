# RetailPulse Analytics — Documentação do Projeto

Foco: transformar dados de vendas em insights acionáveis. Este README concentra-se nas partes essenciais do projeto: dados, notebooks, SQL e código fonte (`src`).

Visão geral rápida
- Origem dos dados: `data/raw/sales.csv` (arquivo CSV bruto)
- Saídas principais: `data/processed/clean_sales.csv` (inglês) e `data/processed/clean_sales_pt_br.csv` (pt-BR)
- Notebooks: análises exploratórias e visualizações em `notebooks/`
- SQL: views e consultas em `sql/`
- Código: ETL em `src/` e scripts utilitários em `metabase/`

Estrutura e responsabilidades
- `data/`
	- `raw/`: dados brutos importados
	- `processed/`: datasets limpos e traduzidos prontos para análise

- `notebooks/`
	- `01_data_exploration.ipynb`: inspeção inicial dos dados, verificações de qualidade e perfilamento
	- `02_sales_visual_analysis.ipynb`: gráficos de vendas, séries temporais e distribuições
	- `03_business_insights.ipynb`: KPIs e análises acionáveis

- `sql/`
	- `schema.sql`: definição de tabelas (se aplicável)
	- `queries.sql`: consultas reutilizáveis
	- `views.sql`: views úteis (inclui versões em português, que consultam `sales_pt_br`)

- `src/` (ETL)
	- `extract.py`: leitura do CSV original e extração inicial
	- `transform.py`: limpeza, normalização e função `translate_to_pt_br(df)`
	- `load.py`: carregamento para PostgreSQL; utiliza `DELETE` + `INSERT` para preservar dependências de views

Como rodar o pipeline (local)
1. Suba os serviços necessários:

```powershell
docker compose up -d
```

2. Execute o pipeline principal (gera CSVs limpos e carrega o banco):

```powershell
python main.py
```

Notas importantes
- Tradução: o pipeline gera uma versão em pt-BR do dataset sem substituir o original — arquivos e tabelas paralelas permitem comparações.
- Banco: as credenciais padrão usadas pelo `docker-compose` são `postgres:postgres` para `retailpulse`; scripts `src/load.py` usam SQLAlchemy/psycopg2.
- Notebooks: comece pelo `01_data_exploration.ipynb` para entender colunas, tipos e valores faltantes antes de editar queries ou painéis.

Boas práticas para desenvolvimento
- Ao ajustar transformação, escreva um notebook curto (ex.: `notebooks/99_dev_test.ipynb`) para validar visualmente as mudanças.
- Versione alterações de SQL em `sql/` e mantenha consultas parametrizáveis (evite placeholders incompatíveis com Postgres).

Agenda de melhorias (sugestões)
- Normalizar nomes de colunas e tipos no carregamento para facilitar consultas SQL.
- Adicionar testes unitários simples para as funções de `src/transform.py`.
- Documentar as colunas e dicionário de dados em `docs/data_dictionary.md`.

Se precisar que eu priorize qualquer item (ex.: criar testes, documentar dicionário de dados ou melhorar notebooks), diga qual e eu inicio.
