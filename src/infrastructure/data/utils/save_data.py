"""Módulo que gerencia a carga em banco de dados, utilizando o Pyspark."""

from typing import Literal

import pandas as pd
from pyspark.sql import DataFrame, SparkSession

from .connect_database import ConnectionDatabaseSpark


class DatabaseWriter:
    """Gerencia a carga em banco de dados com Spark."""

    def __init__(self, spark: SparkSession, connect: ConnectionDatabaseSpark) -> None:
        """Inicializa a conexão para realizar a carga no banco de dados."""
        self.spark = spark
        self.connect = connect

    def save_data(self, df: DataFrame, table_name: str, mode: str = "append") -> None:
        """Salva um DataFrame PySpark no banco de dados.

        :param df: PySpark DataFrame
        :param table_name: nome da tabela no banco
        :param mode: 'append', 'overwrite', 'ignore', 'error'
        """
        if self.connect.sgbd_name == "sqlite":
            if self.connect.sqlite_conn is None:
                self.connect.initialize_jdbc()

            df_pandas: pd.DataFrame = df.toPandas()

            PandasIfExists = Literal["fail", "replace", "append"]

            pandas_mode: PandasIfExists

            if mode == "overwrite":
                pandas_mode = "replace"
            elif mode == "ignore":
                pandas_mode = "fail"
            else:
                pandas_mode = "append"

            df_pandas.to_sql(
                name=table_name,
                con=self.connect.sqlite_conn,
                if_exists=pandas_mode,
                index=False,
            )
            print(f"DataFrame escrito na tabela '{table_name}' do SQLite com sucesso.")

        elif self.connect.sgbd_name == "postgresql":
            jdbc_url, properties = self.connect.initialize_jdbc()
            if jdbc_url is None:
                raise ValueError("JDBC URL não foi inicializada.")
            df.write.jdbc(
                url=jdbc_url, table=table_name, mode=mode, properties=properties
            )
            print(
                f"DataFrame escrito na tabela '{table_name}' do PostgreSQL com sucesso."
            )

        else:
            raise ValueError(f"SGBD '{self.connect.sgbd_name}' não suportado.")
