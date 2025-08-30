"""Módulo para gerenciar conexões JDBC com PySpark para PostgreSQL."""

import time
from pathlib import Path
from typing import Dict, Optional, Tuple

from dotenv import dotenv_values
from pyspark.sql import SparkSession


class ConnectionDatabaseSpark:
    """Gerencia conexão JDBC com PostgreSQL via PySpark."""

    def __init__(
        self,
        sgbd_name: str,
        environment: str,
        db_name: str,
        connection_folder: str = "databases_connection",
    ) -> None:
        """Inicializa os parâmetros de conexão."""
        self.sgbd_name = sgbd_name
        self.environment = environment
        self.db_name = db_name
        self.connection_folder = connection_folder
        self.current_dir: Optional[Path] = None
        self.path_file: Optional[Path] = None
        self.path: Optional[Path] = None
        self.jdbc_url: Optional[str] = None
        self.properties: Optional[Dict[str, str]] = None

    def initialize_jdbc(self) -> Tuple[str, Dict[str, str]]:
        """Cria a URL JDBC e propriedades para conexão com PySpark."""
        self.current_dir = Path(__file__).resolve().parent
        self.path = self.current_dir.parent.joinpath(
            self.connection_folder, self.sgbd_name
        )

        if self.sgbd_name == "postgresql":
            self.path_file = self.path.joinpath(
                f".env.{self.environment}_{self.db_name}"
            )

            if not self.path_file.is_file():
                raise FileNotFoundError(
                    f"Configuration file '{self.path_file}' not found."
                )

            env_vars = dotenv_values(dotenv_path=self.path_file)

            self.jdbc_url = f"jdbc:postgresql://{env_vars['DB_HOST']}:{env_vars['DB_PORT']}/{self.db_name}"
            user = env_vars.get("DB_USER") or ""
            password = env_vars.get("DB_PASSWORD") or ""
            self.properties = {
                "user": user,
                "password": password,
                "driver": "org.postgresql.Driver",
            }
            return self.jdbc_url, self.properties
        else:
            raise ValueError(f"SGBD '{self.sgbd_name}' not supported.")

    def connect_with_retry(
        self, max_retries: int = 5, wait_seconds: int = 5
    ) -> Tuple[str, Dict[str, str]]:
        """Testa a conexão JDBC com retry."""
        for attempt in range(1, max_retries + 1):
            try:
                if self.jdbc_url is None or self.properties is None:
                    self.initialize_jdbc()

                # Cria SparkSession temporária só para testar a conexão
                spark: SparkSession = SparkSession.builder.getOrCreate()
                assert self.jdbc_url is not None and self.properties is not None
                df = spark.read.jdbc(
                    url=self.jdbc_url,
                    table="(SELECT 1) AS test",
                    properties=self.properties,
                )
                df.collect()  # força execução para testar conexão
                print("Connection successful!")
                return self.jdbc_url, self.properties

            except Exception as e:
                print(f"[Attempt {attempt}] Failed to connect: {e}")
                if attempt == max_retries:
                    raise
                time.sleep(wait_seconds)
        assert False, "Should not reach here"
