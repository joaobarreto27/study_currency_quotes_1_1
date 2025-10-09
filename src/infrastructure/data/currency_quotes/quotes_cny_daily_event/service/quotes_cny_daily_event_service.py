"""Serviço responsável por orquestrar a coleta e processamento.

dos eventos de cotação de CNY.
"""

from typing import Any

from pydantic import ValidationError
from pyspark.sql import DataFrame

from ....utils import SparkSessionManager
from ..query import QuotesCnyDailyEventQueryRepository
from ..validator import QuotesCnyDailyEventValidatorSchema


class QuotesCnyDailyEventService:
    """Serviço que executa as operações de coleta e transformação de dados de CNY."""

    def __init__(self, respository: QuotesCnyDailyEventQueryRepository) -> None:
        """Inicializa o serviço com um repositório e sessão Spark."""
        self.repository = respository
        self.session = SparkSessionManager()
        self.data: dict[str, Any] = {}

    def run(self) -> DataFrame:
        """Executa a coleta de dados a partir do repositório."""
        self.data = self.repository.fetch()

        try:
            QuotesCnyDailyEventValidatorSchema(**self.data)
        except ValidationError as e:
            raise ValueError(f"Data validation error: {e}")

        df: DataFrame = self.session.createDataFrame([self.data])
        return df
