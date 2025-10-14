"""Worker responsável por executar o ETL diário de cotação de USD."""

from datetime import datetime

from pyspark.sql.functions import lit

from infrastructure.data.currency_quotes.quotes_usd_daily_event.query import (
    QuotesUsdDailyEventQueryRepository,
)
from infrastructure.data.currency_quotes.quotes_usd_daily_event.service import (
    QuotesUsdDailyEventService,
)
from infrastructure.data.market_data.quotes_usd_daily_event.command import (
    QuotesUsdDailyEventCommandRepository,
)
from infrastructure.data.utils import ConnectionDatabaseSpark, SparkSessionManager


def main() -> None:
    """Executa todo o ETL."""
    spark = SparkSessionManager()

    USE_SQLITE = True

    connection = ConnectionDatabaseSpark(
        sgbd_name="sqlite" if USE_SQLITE else "postgresql",
        environment="prd" if USE_SQLITE else "prd",
        db_name=(
            "1.1_study_currency_quotes" if USE_SQLITE else "1.1_study_currency_quotes"
        ),
    )

    query_repository = QuotesUsdDailyEventQueryRepository(
        "https://economia.awesomeapi.com.br/json/last/USD-BRL?token=baa309fc2062d04f5346345cc3c13bb3da8202631b73b03d79386593439d0cac"
    )

    service = QuotesUsdDailyEventService(query_repository)

    command = QuotesUsdDailyEventCommandRepository(
        service=service,
        spark=spark,  # type:ignore
        connection=connection,
        table_name="quotes_usd_daily_event",
    )

    df = command.command()

    df_clean = df.withColumn(
        "extract_at", lit(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    df_clean.show()
    command.save(df_clean)

    spark.stop()


if __name__ == "__main__":
    main()
