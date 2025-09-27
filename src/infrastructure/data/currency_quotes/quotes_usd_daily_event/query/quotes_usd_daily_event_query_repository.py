"""Módulo para buscar dados diários de cotações do Dólar."""

from typing import Any

from .... import ConnectAPI, SparkSessionManager


class QuotesUsdDailyEventQueryRepository:
    """Repositório para consultas diárias a cotações de USD para BR."""

    def __init__(self, url: str) -> None:
        """Inicializa a consulta a API com a URL."""
        self.data_json: dict[str, Any] = {}
        self.data: dict[str, Any] = {}
        self.session = SparkSessionManager()
        self.url = url

    def fetch(self) -> dict[str, Any]:
        """Busca os dados da API."""
        self.data_json = ConnectAPI(self.url).connect_api()
        if self.data_json:
            self.data = next(iter(self.data_json.values()))
        else:
            raise ValueError("Empty dictionary try again!")
        return self.data
