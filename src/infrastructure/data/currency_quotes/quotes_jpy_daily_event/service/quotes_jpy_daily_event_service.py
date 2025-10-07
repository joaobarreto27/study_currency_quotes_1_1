"""Serviço responsável por orquestrar a coleta e processamento.

dos eventos de cotação de JPY.
"""

from typing import Any

from pydantic import ValidationError
from pyspark.sql import DataFrame

from ....utils import SparkSessionManager
from ..query import QuotesJpyDailyEventQueryRepository
from ..validator import QuotesJpyDailyEventValidatorSchema


class QuotesJpyDailyEventService:
    """Serviço que executa as operações de coleta e transformação de dados de JPY."""

    def __init__(self, repository: QuotesJpyDailyEventQueryRepository) -> None:
        """Inicializa o serviço com um repositório e sessão Spark."""
        self.repository = repository
        self.session = SparkSessionManager()
        self.data: dict[str, Any] = {}

    def run(self) -> DataFrame:
        """Executa a coleta de dados a partir do repositorio."""
        self.data = self.repository.fetch()

        try:
            QuotesJpyDailyEventValidatorSchema(**self.data)
        except ValidationError as e:
            raise ValueError(f"Data validation error: {e}")

        df: DataFrame = self.session.createDataFrame([self.data])
        return df
