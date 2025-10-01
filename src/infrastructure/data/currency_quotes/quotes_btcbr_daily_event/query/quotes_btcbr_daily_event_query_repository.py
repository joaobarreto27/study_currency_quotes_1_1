"""Módulo para buscar dados diários de cotações de BTCBR."""

from typing import Any

from ....utils import ConnectAPI, SparkSessionManager


class QuotesBtcbrDailyEventQueryRepository:
    """Repositório para consulta diárias a cotações de BTC para BR."""

    def __init__(self, url: str) -> None:
        """Inicializa a consulta a API com URL."""
        self.data_json: dict[str, Any] = {}
        self.data: dict[str, Any] = {}
        self.session = SparkSessionManager()
        self.url = url

    def fetch(self) -> dict[str, Any]:
        """Busca os dados da API."""
        self.data_json = ConnectAPI(url=self.url).connect_api()
        if self.data_json:
            self.data = next(iter(self.data_json.values()))
        else:
            raise ValueError("Empty dictionary try again!")
        return self.data
