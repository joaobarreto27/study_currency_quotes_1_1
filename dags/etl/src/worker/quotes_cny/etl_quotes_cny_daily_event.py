"""Worker responsável por executar o ETL diário de cotações de CNY."""

from datetime import datetime

from pyspark.sql.functions import lit

from infrastructure.data.currency_quotes.quotes_cny_daily_event.query import (
    QuotesCnyDailyEventQueryRepository,
)
from infrastructure.data.currency_quotes.quotes_cny_daily_event.service import (
    QuotesCnyDailyEventService,
)
from infrastructure.data.market_data.quotes_cny_daily_event.command import (
    QuotesCnyDailyEventCommandRepository,
)
from infrastructure.data.utils import (
    ConnectionDatabaseSpark,
    EnvManager,
    SparkSessionManager,
)


def main() -> None:
    """Executar o ETL."""
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

    query_repository = QuotesCnyDailyEventQueryRepository(
        f"https://economia.awesomeapi.com.br/json/last/CNY-BRL?token={api_token}"
    )

    service = QuotesCnyDailyEventService(respository=query_repository)

    command = QuotesCnyDailyEventCommandRepository(
        service=service,
        spark=spark,  # type:ignore
        connection=connection,
        table_name="quotes_cny_daily_event",
    )

    df = command.command()

    df_clean = df.withColumn(
        "extract_at", lit(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    df_clean.show(truncate=False)
    command.save(df_clean)

    spark.stop()


if __name__ == "__main__":
    main()
