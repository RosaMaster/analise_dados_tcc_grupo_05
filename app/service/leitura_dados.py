import dask.dataframe as dd
import polars as pl

class LeituraDados:
    
    @staticmethod
    def read_dados_origem(csv_path, encoding):
        """Função para ler os dados de um arquivo CSV usando Dask.

        Returns:
            _type_: Retorna um DataFrame _dd.DataFrame_ do Dask com os dados lidos do arquivo CSV.
        """
        
        dataframe = dd.read_csv(csv_path, encoding=encoding, sep=";", assume_missing=True)

        return dataframe

    
    @staticmethod
    def read_polars(csv_path, encoding):
        """Função para ler os dados de um arquivo CSV usando Polars.

        Returns:
            _type_: Retorna um DataFrame _pl.DataFrame_ do Polars com os dados lidos do arquivo CSV.
        """
        
        dataframe = pl.read_csv(csv_path, encoding=encoding, separator=";")

        return dataframe