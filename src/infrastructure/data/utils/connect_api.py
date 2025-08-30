"""Módulo responsável por conectar na API."""

from typing import Any

import requests


class ConnectAPI:
    """Gerencia conexão com a API."""

    def __init__(self, url: str) -> None:
        """Inicializa a conexão com a API.

        Args:
            url (str): URL base da API.

        """
        self.url: str = url
        self.data_json: dict[str, Any] = {}

    def connect_api(self) -> dict[str, Any]:
        """Realiza a conexão com a API."""
        url: str = self.url
        response = requests.get(url=url, timeout=10)

        if response.status_code == 200:
            self.data_json = response.json()
        else:
            raise ValueError("Connection error: Please try again.")
        return self.data_json
