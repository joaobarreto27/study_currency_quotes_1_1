"""Serviço responsável por orquestar a coleta e processamento.

dos eventos de cotação de USD.
"""

from typing import Any

from pydantic import ValidationError
from pyspark.sql import DataFrame

from ....utils import SparkSessionManager
from ..query import QuotesUsdDailyEventQueryRepository
from ..validator import QuotesUsdDailyEventValidatorSchema


class QuotesUsdDailyEventService:
    """Serviço que executa as operações de coleta e transformação de dados de USD."""

    def __init__(self, repository: QuotesUsdDailyEventQueryRepository) -> None:
        """Inicializa o serviço com um repositório e sessão Spark."""
        self.repository = repository
        self.session = SparkSessionManager()
        self.data: dict[str, Any] = {}

    def run(self) -> DataFrame:
        """Executa a coleta de dados a partir do repositório."""
        self.data = self.repository.fetch()

        try:
            QuotesUsdDailyEventValidatorSchema(**self.data)
        except ValidationError as e:
            raise ValueError(f"Data validation erro: {e}")

        df: DataFrame = self.session.createDataFrame([self.data])
        df.show(truncate=False)

        return df
