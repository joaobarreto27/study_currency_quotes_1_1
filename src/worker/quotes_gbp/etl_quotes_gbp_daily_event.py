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
from infrastructure.data.utils import (
    ConnectionDatabaseSpark,
    EnvManager,
    SparkSessionManager,
)


def main() -> None:
    """Executa o ETL."""
    spark = SparkSessionManager()

    USE_SQLITE = True

    connection = ConnectionDatabaseSpark(
        sgbd_name="sqlite" if USE_SQLITE else "postgresql",
        environment="prd" if USE_SQLITE else "prd",
        db_name=(
            "1.1_study_currency_quotes" if USE_SQLITE else "1.1_study_currency_quotes"
        ),
    )

    env_manager = EnvManager()
    api_token = env_manager.get_token()

    query_repository = QuotesGbpDailyEventQueryRepository(
        f"https://economia.awesomeapi.com.br/json/last/GBP-BRL?token={api_token}"
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
