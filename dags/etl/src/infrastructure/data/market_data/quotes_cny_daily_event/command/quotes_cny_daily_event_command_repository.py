"""Gerencia o comando de executar a consulta a API e salva no banco de dados."""

from pyspark.sql import DataFrame, SparkSession

from infrastructure.data.currency_quotes.quotes_cny_daily_event.service import (
    QuotesCnyDailyEventService,
)
from infrastructure.data.utils import ConnectionDatabaseSpark, DatabaseWriter


class QuotesCnyDailyEventCommandRepository:
    """Classe para realizar o comando de executar a API e salvar no banco de dados."""

    def __init__(
        self,
        service: QuotesCnyDailyEventService,
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
        df = self.service.run()
        return df

    def save(self, df: DataFrame, mode: str = "append") -> None:
        """Salva o DataFrame no banco de dados."""
        writer = DatabaseWriter(spark=self.spark, connect=self.connection)
        writer.save_data(df=df, table_name=self.table_name, mode=mode)
