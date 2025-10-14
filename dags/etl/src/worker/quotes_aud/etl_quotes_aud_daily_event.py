"""Worker responsável por executar o ETL diário de cotações de AUD."""

from datetime import datetime

from pyspark.sql.functions import lit

from infrastructure.data.currency_quotes.quotes_aud_daily_event.query import (
    QuotesAudDailyEventQueryRepository,
)
from infrastructure.data.currency_quotes.quotes_aud_daily_event.service import (
    QuotesAudDailyEventService,
)
from infrastructure.data.market_data.quotes_aud_daily_event.command import (
    QuotesAudDailyEventCommandRepository,
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

    query_repository = QuotesAudDailyEventQueryRepository(
        f"https://economia.awesomeapi.com.br/json/last/AUD-BRL?token={api_token}"
    )

    service = QuotesAudDailyEventService(respository=query_repository)

    command = QuotesAudDailyEventCommandRepository(
        service=service,
        spark=spark,  # type:ignore
        connection=connection,
        table_name="quotes_aud_daily_event",
    )

    df = command.command()

    df_clean = df.withColumn(
        "extract_at", lit(datetime.now().strftime("%Y-%m-%d %H:%M-%S"))
    )

    df_clean.show(truncate=False)
    command.save(df=df_clean)

    spark.stop()


if __name__ == "__main__":
    main()
