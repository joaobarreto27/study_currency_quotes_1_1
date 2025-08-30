"""Módulo que gerencia a carga em banco de dados, utilizando o Pyspark."""

from pyspark.sql import DataFrame, SparkSession

from .connect_database import ConnectionDatabaseSpark


class DatabaseWriter:
    """Gerencia a carga em banco de dados com Spark."""

    def __init__(self, spark: SparkSession, connect: ConnectionDatabaseSpark) -> None:
        """Inicializa a conexão para realizar a carga no banco de dados."""
        self.spark = spark
        self.connect = connect

    def save_data(self, df: DataFrame, table_name: str, mode: str = "append") -> None:
        """Salva um DataFrame PySpark no banco via JDBC.

        :param df: PySpark DataFrame
        :param table_name: nome da tabela no banco
        :param mode: 'append', 'overwrite', 'ignore', 'error'

        """
        jdbc_url, properties = self.connect.initialize_jdbc()
        df.write.jdbc(url=jdbc_url, table=table_name, mode=mode, properties=properties)

        print(f"DataFrame written to table {table_name} successfully.")
