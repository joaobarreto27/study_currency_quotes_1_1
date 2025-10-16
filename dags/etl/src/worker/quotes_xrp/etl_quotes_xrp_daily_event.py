"""Worker responsável por executar o ETL diário de cotações de Xrp."""

from datetime import datetime

from pyspark.sql.functions import lit

from infrastructure.data.currency_quotes.quotes_xrp_daily_event.query import (
    QuotesXrpDailyEventQueryRepository,
)
from infrastructure.data.currency_quotes.quotes_xrp_daily_event.service import (
    QuotesXrpDailyEventService,
)
from infrastructure.data.market_data.quotes_xrp_daily_event.command import (
    QuotesXrpDailyEventCommandRepository,
)
from infrastructure.data.utils import (
    ConnectionDatabaseSpark,
    EnvManager,
    SparkSessionManager,
)


def main() -> None:
    """Executa o ETL."""
    spark = SparkSessionManager()
    USE_SQLITE = False

    connection = ConnectionDatabaseSpark(
        sgbd_name="sqlite" if USE_SQLITE else "postgresql",
        environment="prd" if USE_SQLITE else "prd",
        db_name=(
            "1.1_study_currency_quotes" if USE_SQLITE else "1.1_study_currency_quotes"
        ),
    )

    env_manager = EnvManager()
    api_token = env_manager.get_token()

    query_repository = QuotesXrpDailyEventQueryRepository(
        f"https://economia.awesomeapi.com.br/json/last/XRP-BRL?token={api_token}"
    )

    service = QuotesXrpDailyEventService(respository=query_repository)

    command = QuotesXrpDailyEventCommandRepository(
        service=service,
        spark=spark,  # type:ignore
        connection=connection,
        table_name="quotes_xrp_daily_event",
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
