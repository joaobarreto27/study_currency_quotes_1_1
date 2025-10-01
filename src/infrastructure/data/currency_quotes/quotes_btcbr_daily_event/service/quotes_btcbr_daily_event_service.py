"""Serviço responsável por orquestrar a coleta e processamento.

dos eventos de cotação de BTCBR.
"""

from typing import Any

from pydantic import ValidationError
from pyspark.sql import DataFrame

from ....utils import SparkSessionManager
from ..query import QuotesBtcbrDailyEventQueryRepository
from ..validator import QuotesBtcbrDailyEventValidatorSchema


class QuotesBtcbrDailyEventService:
    """Serviço que executa as operações de coleta e validação de dados de BTCBR."""

    def __init__(self, repository: QuotesBtcbrDailyEventQueryRepository) -> None:
        """Inicializa o serviço com um repositório e sessão Spark."""
        self.repository = repository
        self.session = SparkSessionManager()
        self.data: dict[str, Any] = {}

    def run(self) -> DataFrame:
        """Executa a coleta de dados a partir do repositório."""
        self.data = self.repository.fetch()

        try:
            QuotesBtcbrDailyEventValidatorSchema(**self.data)
        except ValidationError as e:
            raise ValueError(f"Data validation error: {e}")

        df: DataFrame = self.session.createDataFrame([self.data])
        return df
