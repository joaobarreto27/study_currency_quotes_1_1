"""Serviço responsável por orquestrar a coleta e processamento.

dos eventos de cotação de EUR.
"""

from typing import Any

from pydantic import ValidationError
from pyspark.sql import DataFrame

from ....utils import SparkSessionManager
from ..query import QuotesEurDailyEventQueryRepository
from ..validator import QuotesUsdDailyEventValidatorSchema


class QuotesEurDailyEventService:
    """Serviço que executa as operações de coleta e trasformação de dados de EUR."""

    def __init__(self, repository: QuotesEurDailyEventQueryRepository) -> None:
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
            raise ValidationError(f"Data validation error: {e}")

        df: DataFrame = self.session.createDataFrame([self.data])
        return df
