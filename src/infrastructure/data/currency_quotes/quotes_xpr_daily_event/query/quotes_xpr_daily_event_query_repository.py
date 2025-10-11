"""Módulo para buscar dados diários de cotação do XPR."""

from typing import Any

from ....utils import ConnectAPI, SparkSessionManager


class QuotesXprDailyEventQueryRepository:
    """Repositório para consultas diárias a cotações de XPR para BR."""

    def __init__(self, url: str) -> None:
        """Inicializa a consulta a API com a URL."""
        self.data_json: dict[str, Any] = {}
        self.data: dict[str, Any] = {}
        self.session = SparkSessionManager()
        self.url = url

    def fetch(self) -> dict[str, Any]:
        """Busca os dados da API e armazena em data_json."""
        self.data_json = ConnectAPI(url=self.url).connect_api()

        if self.data_json:
            self.data = next(iter(self.data_json.values()))
        else:
            raise ValueError("Empty dictionary try again")
        return self.data
