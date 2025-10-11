"""Worker responsável por executar o ETL diário de cotação de BTC."""

from datetime import datetime

from pyspark.sql.functions import lit

from infrastructure.data.currency_quotes.quotes_btc_daily_event.query import (
    QuotesBtcDailyEventQueryRepository,
)
from infrastructure.data.currency_quotes.quotes_btc_daily_event.service import (
    QuotesBtcDailyEventService,
)
from infrastructure.data.market_data.quotes_btc_daily_event.command import (
    QuotesBtcDailyEventCommandRepository,
)
from infrastructure.data.utils import ConnectionDatabaseSpark, SparkSessionManager


def main() -> None:
    """Executa todo o ETL."""
    # 1. Spark Session
    spark = SparkSessionManager()

    # 2. Conexão com banco
    connection = ConnectionDatabaseSpark(
        sgbd_name="postgresql",
        environment="prd",
        db_name="1.1_study_currency_quotes",
    )

    # 3. Repository de leitura (extrai dados da API)
    query_repository = QuotesBtcDailyEventQueryRepository(
        "https://api.coinbase.com/v2/prices/spot"
    )

    # 4. Service (valida e transforma)
    service = QuotesBtcDailyEventService(query_repository)

    # 5. CommandRepository (roda ETL + salva no banco)
    command = QuotesBtcDailyEventCommandRepository(
        service=service,
        spark=spark,  # type:ignore
        connection=connection,
        table_name="quotes_btc_daily_event",
    )

    # 6. Executa pipeline
    df = command.command()
    df_clean = df.withColumn(
        "extract_at", lit(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    df_clean.show()
    command.save(df_clean)

    # 7. Finaliza Spark
    spark.stop()


if __name__ == "__main__":
    main()
