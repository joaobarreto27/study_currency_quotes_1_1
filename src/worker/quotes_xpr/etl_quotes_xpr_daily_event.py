"""Worker responsável por executar o ETL diário de cotações de XPR."""

from datetime import datetime

from pyspark.sql.functions import lit

from infrastructure.data.currency_quotes.quotes_xpr_daily_event.query import (
    QuotesXprDailyEventQueryRepository,
)
from infrastructure.data.currency_quotes.quotes_xpr_daily_event.service import (
    QuotesXprDailyEventService,
)
from infrastructure.data.market_data.quotes_xpr_daily_event.command import (
    QuotesXprDailyEventCommandRepository,
)
from infrastructure.data.utils import ConnectionDatabaseSpark, SparkSessionManager


def main() -> None:
    """Executa o ETL."""
    spark = SparkSessionManager()

    connection = ConnectionDatabaseSpark(
        sgbd_name="postgresql", environment="dev", db_name="1.1_study_currency_quotes"
    )

    query_repository = QuotesXprDailyEventQueryRepository(
        "https://economia.awesomeapi.com.br/json/last/XPR-BRL?token=baa309fc2062d04f5346345cc3c13bb3da8202631b73b03d79386593439d0cac"
    )

    service = QuotesXprDailyEventService(respository=query_repository)

    command = QuotesXprDailyEventCommandRepository(
        service=service,
        spark=spark,  # type:ignore
        connection=connection,
        table_name="quotes_xpr_daily_event",
    )

    df = command.command()

    df_clean = df.withColumn(
        "extract_at", lit(datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    )

    df_clean.show(truncate=False)
    command.save(df=df_clean)

    spark.stop()

    if __name__ == "__main__":
        main()
