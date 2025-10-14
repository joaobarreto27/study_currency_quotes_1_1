"""Módulo que gerencia variáveis de ambiente e tokens de API."""

from pathlib import Path
from typing import Optional

from dotenv import dotenv_values


class EnvManager:
    """Classe para gerenciar variáveis de ambiente e tokens de API."""

    def __init__(self, env_file: Optional[str] = None) -> None:
        """Inicializa o manager e carrega o arquivo .env.

        :param env_file: Caminho para arquivo .env. Se None, procura na raiz do projeto.
        """
        if env_file is None:
            # Procura automaticamente o .env na raiz do projeto
            self.env_file = Path(".env").resolve()
        else:
            self.env_file = Path(env_file).resolve()

        if not self.env_file.is_file():
            raise FileNotFoundError(f"Arquivo '{self.env_file}' não encontrado.")

        # Carrega todas as variáveis do .env
        self.env_vars = dotenv_values(dotenv_path=self.env_file)

    def get_token(self, token_name: Optional[str] = None) -> Optional[str]:
        """Retorna o token da API a partir do .env.

        :param token_name: Nome da variável no .env que contém o token
        :return: token como string ou None se não encontrado
        """
        token_name = token_name or "API_TOKEN"
        token = self.env_vars.get(token_name)
        if token is None:
            print(f"Atenção: variável '{token_name}' não encontrada no arquivo .env")
        return token

    def get_variable(self, var_name: str) -> Optional[str]:
        """Retorna qualquer variável do .env.

        :param var_name: Nome da variável
        :return: valor da variável ou None se não encontrada
        """
        value = self.env_vars.get(var_name)
        if value is None:
            print(f"Atenção: variável '{var_name}' não encontrada no arquivo .env")
        return value
