"""Módulo responsável por gerenciar a SparkSession do PySpark."""

from typing import Any, Dict, Optional

from pyspark.sql import SparkSession


class SparkSessionManager:
    """Singleton que inicializa e retorna uma SparkSession."""

    _instance: Optional["SparkSessionManager"] = None
    _spark: Optional[SparkSession] = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "SparkSessionManager":
        """Garantir apenas uma instância (singleton)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        app_name: str = "MySparkApp",
        master: str = "local[*]",
        configs: Optional[Dict[str, str]] = None,
    ) -> None:
        """Inicializa a SparkSession automaticamente na primeira instância.

        Args:
            app_name (str): Nome da aplicação Spark.
            master (str): Master URL, ex: 'local[*]' ou 'yarn'.
            configs (Optional[Dict[str, str]]): Configurações adicionais do Spark.

        """
        if self._spark is not None:
            return  # sessão já inicializada

        builder = SparkSession.builder.appName(app_name).master(master)
        if configs:
            for key, value in configs.items():
                builder = builder.config(key, value)

        self._spark = builder.getOrCreate()

    def __getattr__(self, item: str) -> Any:
        """Delegue acesso de atributo ao SparkSession.

        Permite chamar qualquer método ou acessar qualquer atributo da
        SparkSession diretamente na instância do manager.

        Exemplo:
            session.createDataFrame(...)

        """
        if self._spark is None:
            raise AttributeError("SparkSession not yet initialized.")
        return getattr(self._spark, item)

    def stop(self) -> None:
        """Encerra a SparkSession, liberando recursos."""
        if self._spark:
            self._spark.stop()
            self._spark = None
