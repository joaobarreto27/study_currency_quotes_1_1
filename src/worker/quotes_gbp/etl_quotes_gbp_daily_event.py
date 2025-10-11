"""Worker responsável por executar o ETL diário de cotação de GBP."""

from datetime import datetime

from pyspark.sql.functions import lit

from infrastructure.data.currency_quotes.quotes_gbp_daily_event.query import (
    QuotesGbpDailyEventQueryRepository,
)
from infrastructure.data.currency_quotes.quotes_gbp_daily_event.service import (
    QuotesGbpDailyEventService,
)
from infrastructure.data.market_data.quotes_gbp_daily_event.command import (
    QuotesGbpDailyEventCommandRepository,
)
from infrastructure.data.utils import ConnectionDatabaseSpark, SparkSessionManager


def main() -> None:
    """Executa o ETL."""
    spark = SparkSessionManager()

    connection = ConnectionDatabaseSpark(
        sgbd_name="postgresql", environment="prd", db_name="1.1_study_currency_quotes"
    )

    query_repository = QuotesGbpDailyEventQueryRepository(
        "https://economia.awesomeapi.com.br/json/last/EUR-BRL?token=baa309fc2062d04f5346345cc3c13bb3da8202631b73b03d79386593439d0cac"
    )

    service = QuotesGbpDailyEventService(query_repository)

    command = QuotesGbpDailyEventCommandRepository(
        service=service,
        spark=spark,  # type:ignore
        connection=connection,
        table_name="quotes_gbp_daily_event",
    )

    df = command.command()

    df_clean = df.withColumn(
        "extract_at", lit(datetime.now().strftime("%Y-%m-%dd %H:%M:%S"))
    ).withColumnRenamed("code", "currency")

    df_clean.show(truncate=False)
    command.save(df_clean)

    spark.stop()


if __name__ == "__main__":
    main()
