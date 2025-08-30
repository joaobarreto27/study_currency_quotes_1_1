"""Serviço responsável por orquestrar a coleta e processamento.

dos eventos de cotação de BTC.
"""

from typing import Any

from pydantic import ValidationError

from ....utils import SparkSessionManager
from ..query import QuotesBtcDailyEventQueryRepository
from ..validator import QuotesBitcoinEventValidatorSchema


class QuotesBtcDailyEventService:
    """Serviço que executa as operações de coleta e transformação de dados de BTC."""

    def __init__(self, repository: QuotesBtcDailyEventQueryRepository) -> None:
        """Inicializa o serviço com um repositório e sessão Spark."""
        self.repository = repository
        self.session = SparkSessionManager()
        self.data: dict[str, Any] = {}

    def run(self) -> None:
        """Executa a coleta de dados a partir do repositório."""
        self.data = self.repository.fetch()

        try:
            QuotesBitcoinEventValidatorSchema(**self.data)
        except ValidationError as e:
            raise ValueError(f"Data validation error: {e}")

        df = self.session.createDataFrame([self.data])
        df.show(truncate=False)

        self.session.stop()
