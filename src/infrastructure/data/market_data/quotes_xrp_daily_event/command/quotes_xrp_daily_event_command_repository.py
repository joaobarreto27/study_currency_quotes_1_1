"""Gerencia o comando de executar a consulta a API e salva no banco de dados."""

from pyspark.sql import DataFrame, SparkSession

from infrastructure.data.currency_quotes.quotes_xrp_daily_event.service import (
    QuotesXrpDailyEventService,
)
from infrastructure.data.utils import ConnectionDatabaseSpark, DatabaseWriter


class QuotesXrpDailyEventCommandRepository:
    """Classe para realizar o comando de executar a API e salvar no banco de dados."""

    def __init__(
        self,
        service: QuotesXrpDailyEventService,
        spark: SparkSession,
        connection: ConnectionDatabaseSpark,
        table_name: str,
    ) -> None:
        """Inicializa a classe."""
        self.service = service
        self.spark = spark
        self.connection = connection
        self.table_name = table_name

    def command(self) -> DataFrame:
        """Executa o serviço e retorna um DataFrame validado."""
        df: DataFrame = self.service.run()
        return df

    def save(self, df: DataFrame, mode: str = "append") -> None:
        """Salva o DataFrame no banco de dados."""
        writer = DatabaseWriter(spark=self.spark, connect=self.connection)
        writer.save_data(df=df, table_name=self.table_name, mode=mode)
