"""Serviço responsável por orquestrar a coleta e processamento.

dos eventos de cotação de ARS.
"""

from typing import Any

from pydantic import ValidationError
from pyspark.sql import DataFrame

from ....utils import SparkSessionManager
from ..query import QuotesArsDailyEventQueryRepository
from ..validator import QuotesArsDailyEventValidatorSchema


class QuotesArsDailyEventService:
    """Serviço que executa as operações de coleta e transformação de dados de ARS."""

    def __init__(self, respository: QuotesArsDailyEventQueryRepository) -> None:
        """Inicializa o serviço com um repositório e sessão Spark."""
        self.repository = respository
        self.session = SparkSessionManager()
        self.data: dict[str, Any] = {}

    def run(self) -> DataFrame:
        """Executa a coleta de dados a partir do repositório."""
        self.data = self.repository.fetch()

        try:
            QuotesArsDailyEventValidatorSchema(**self.data)
        except ValidationError as e:
            raise ValueError(f"Erro na validação dos dados: {e}")

        df: DataFrame = self.session.createDataFrame([self.data])
        return df
