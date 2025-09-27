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

    def connect_api(
        self,
        auth: tuple[str, str] | None = None,
        token: str | None = None,
        params_query: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Conecta a uma API com autenticação flexível.

        Args:
            auth (tuple[str, str] | None): Para Basic Auth.
            token (str | None): Token de autenticação para header.
            params_query (dict[str, str] | None): Query parameters opcionais,
            incluindo token via query.

        Returns:
            dict[str, Any]: Resposta JSON da API.

        Raises:
            ValueError: Se os parâmetros de autenticação forem inválidos
            ou a requisição falhar.
        """
        methods_used = sum(x is not None for x in [auth, token, params_query])
        if methods_used > 1:
            raise ValueError(
                "Escolha apenas um método de autenticação: auth, token ou params_query."
            )

        request_auth = auth
        headers: dict[str, str] = {}
        params: dict[str, str] = params_query or {}

        if token is not None:
            headers = headers = {"Authorization": f"Token {token}"}

        response = requests.get(
            url=self.url,
            auth=request_auth,
            headers=headers if headers else None,
            params=params if params else None,
            timeout=10,
        )

        if response.status_code == 200:
            self.data_json = response.json()
        else:
            raise ValueError("Connection error: Please try again.")
        return self.data_json
