"""Serviço responsável por orquestrar a coleta e processamento.

dos eventos diários de cotação de CAD.
"""

from typing import Any

from pydantic import ValidationError
from pyspark.sql import DataFrame

from ....utils import SparkSessionManager
from ..query import QuotesCadDailyEventQueryRepository
from ..validator import QuotesCadDailyEventValidatorSchema


class QuotesCadDailyEventService:
    """Serviço que executa as operações de coleta e transformação de dados de CAD."""

    def __init__(self, repository: QuotesCadDailyEventQueryRepository) -> None:
        """Inicializa o serviço com um repositório e sessão Spark."""
        self.repository = repository
        self.session = SparkSessionManager()
        self.data: dict[str, Any] = {}

    def run(self) -> DataFrame:
        """Executa a coleta de dados a partir do repositório."""
        self.data = self.repository.fetch()

        try:
            QuotesCadDailyEventValidatorSchema(**self.data)
        except ValidationError as e:
            raise ValueError(f"Data validation error: {e}")

        df: DataFrame = self.session.createDataFrame([self.data])
        return df
