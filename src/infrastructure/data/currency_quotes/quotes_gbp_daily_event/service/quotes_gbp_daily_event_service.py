"""Serviço responsável por orquestar a coleta e processamento.

dos eventos de cotação de GBP.
"""

from typing import Any

from pydantic import ValidationError
from pyspark.sql import DataFrame

from ....utils import SparkSessionManager
from ..query import QuotesGbpDailyEventQueryRepository
from ..validator import QuotesGbpDailyEventValidatorSchema


class QuotesGbpDailyEventService:
    """Serviço que executa as operações de coleta e validação de dados de GBP."""

    def __init__(self, repository: QuotesGbpDailyEventQueryRepository) -> None:
        """Inicializa o serviço com um repositório e sessão Spark."""
        self.repository = repository
        self.session = SparkSessionManager()
        self.data: dict[str, Any] = {}

    def run(self) -> DataFrame:
        """Executa a coleta de dados a partir do repositório."""
        self.data = self.repository.fetch()

        try:
            QuotesGbpDailyEventValidatorSchema(**self.data)
        except ValidationError as e:
            raise ValueError(f"Data validation error: {e}")

        df: DataFrame = self.session.createDataFrame([self.data])

        return df
