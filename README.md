# Currency Quotes Automation

🚀 **Automatiza a extração de cotação de moedas e salva em um banco de dados.**

## 🛠️ Tecnologias Utilizadas
- Python
- PySpark
- Pandas
- Airflow
- Docker
- Pydantic

## 🐳 Executando via Docker

⚠️ **Requisitos:**
- Docker Desktop instalado
- `docker-compose` disponível

1️⃣ **Clone o repositório:**
```bash
   git clone https://github.com/SEU_USUARIO/currency-quotes-automation.git
   cd currency-quotes-automation
   ```

2️⃣ **Crie o arquivo `.env` na raiz do projeto com as seguintes variáveis:**
   ```env
   API_TOKEN=seu_token_api
   AIRFLOW_IMAGE_NAME=apache/airflow:2.5.1
   AIRFLOW_UID=50000
   ```
🔑 Gerando o API Token

Para gerar o token, acesse: AwesomeAPI - instruções de API Key

Siga as instruções do site para obter seu API_TOKEN e coloque no .env.

3️⃣ **Suba os serviços:**
   ```bash
   docker-compose up -d
   ```

✅ O Airflow estará disponível em [http://localhost:8080](http://localhost:8080).

## 🗂️ Estrutura do Projeto
```
├── dags/                           # Definições dos pipelines do Airflow
│   └── etl/
│       ├── dags/                   # Arquivos DAG do Airflow
│       └── src/                    # Código fonte do ETL
│           ├── infrastructure/
│           │   ├── data/
│           │   │   ├── currency_quotes/  # Módulos para extração de cotações
│           │   │   │   ├── quotes_ars_daily_event/   # Cotação ARS (Peso Argentino)
│           │   │   │   │   ├── query/
│           │   │   │   │   ├── service/
│           │   │   │   │   └── validator/
│           │   │   │   ├── quotes_aud_daily_event/   # Cotação AUD (Dólar Australiano)
│           │   │   │   ├── quotes_btc_daily_event/   # Cotação BTC (Bitcoin)
│           │   │   │   ├── quotes_btcbr_daily_event/ # Cotação BTC no Brasil
│           │   │   │   ├── quotes_cad_daily_event/   # Cotação CAD (Dólar Canadense)
│           │   │   │   ├── quotes_chf_daily_event/   # Cotação CHF (Franco Suíço)
│           │   │   │   ├── quotes_cny_daily_event/   # Cotação CNY (Yuan Chinês)
│           │   │   │   ├── quotes_eth_daily_event/   # Cotação ETH (Ethereum)
│           │   │   │   ├── quotes_eur_daily_event/   # Cotação EUR (Euro)
│           │   │   │   ├── quotes_gbp_daily_event/   # Cotação GBP (Libra Esterlina)
│           │   │   │   ├── quotes_jpy_daily_event/   # Cotação JPY (Iene Japonês)
│           │   │   │   ├── quotes_usd_daily_event/   # Cotação USD (Dólar Americano)
│           │   │   │   └── quotes_xrp_daily_event/   # Cotação XRP (Ripple)
│           │   │   ├── databases_connection/         # Conexões com bancos de dados
│           │   │   │   ├── mysql/
│           │   │   │   ├── postgresql/
│           │   │   │   └── sqlite/
│           │   │   ├── market_data/                  # Comandos para manipulação de dados de mercado
│           │   │   │   ├── quotes_ars_daily_event/
│           │   │   │   │   └── command/
│           │   │   │   ├── quotes_aud_daily_event/
│           │   │   │   ├── quotes_btc_daily_event/
│           │   │   │   ├── quotes_btcbr_daily_event/
│           │   │   │   ├── quotes_cad_daily_event/
│           │   │   │   ├── quotes_chf_daily_event/
│           │   │   │   ├── quotes_cny_daily_event/
│           │   │   │   ├── quotes_eth_daily_event/
│           │   │   │   ├── quotes_eur_daily_event/
│           │   │   │   ├── quotes_gbp_daily_event/
│           │   │   │   ├── quotes_jpy_daily_event/
│           │   │   │   ├── quotes_usd_daily_event/
│           │   │   │   └── quotes_xrp_daily_event/
│           │   │   └── utils/                       # Utilitários para o ETL
│           │   └── worker/                          # Workers para processamento de cotações
│           │       ├── quotes_ars/
│           │       ├── quotes_aud/
│           │       ├── quotes_btc/
│           │       ├── quotes_btcbr/
│           │       ├── quotes_cad/
│           │       ├── quotes_chf/
│           │       ├── quotes_cny/
│           │       ├── quotes_eth/
│           │       ├── quotes_eur/
│           │       ├── quotes_gbp/
│           │       ├── quotes_jpy/
│           │       ├── quotes_usd/
│           │       └── quotes_xrp/
├── logs/                           # Logs gerados pelo Airflow
├── plugins/                        # Plugins personalizados para o Airflow
```

## 💾 Banco de Dados

O projeto roda com **PostgreSQL** em ambiente de produção, mas para testes foi configurado **SQLite**.  
Exemplo de configuração no código:

```python
USE_SQLITE = True

connection = ConnectionDatabaseSpark(
    sgbd_name="sqlite" if USE_SQLITE else "postgresql",
    environment="prd" if USE_SQLITE else "prd",
    db_name=(
        "1.1_study_currency_quotes" if USE_SQLITE else "1.1_study_currency_quotes"
    ),
)
```
