"""Worker responsável por executar o ETL diário de cotação de CAD."""

from datetime import datetime

from pyspark.sql.functions import lit

from infrastructure.data.currency_quotes.quotes_cad_daily_event.query import (
    QuotesCadDailyEventQueryRepository,
)
from infrastructure.data.currency_quotes.quotes_cad_daily_event.service import (
    QuotesCadDailyEventService,
)
from infrastructure.data.market_data.quotes_cad_daily_event.command import (
    QuotesCadDailyEventCommandRepository,
)
from infrastructure.data.utils import ConnectionDatabaseSpark, SparkSessionManager


def main() -> None:
    """Executa o ETL."""
    spark = SparkSessionManager()

    connection = ConnectionDatabaseSpark(
        sgbd_name="postgresql", environment="dev", db_name="1.1_study_currency_quotes"
    )

    query_repository = QuotesCadDailyEventQueryRepository(
        "https://economia.awesomeapi.com.br/json/last/CAD-BRL?token=baa309fc2062d04f5346345cc3c13bb3da8202631b73b03d79386593439d0cac"
    )

    service = QuotesCadDailyEventService(query_repository)

    command = QuotesCadDailyEventCommandRepository(
        service=service,
        spark=spark,  # type:ignore
        connection=connection,
        table_name="quotes_cad_daily_event",
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
