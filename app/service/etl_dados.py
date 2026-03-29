import polars as pl
from pathlib import Path


class ExtracTransformLoadData:

    @staticmethod
    def csv_to_parquet(dados_origem: str, dados_destino: str, lista_colunas: list, encoding: str) -> pl.DataFrame:
        """ Extrai dados de um arquivo CSV, seleciona colunas específicas, filtra os dados e salva em formato Parquet.

        Args:
            dados_origem (str): Caminho para o arquivo CSV de origem
            dados_destino (str): Caminho para o arquivo Parquet de destino
            lista_colunas (list): Lista de nomes de colunas a serem selecionadas
            encoding (str): Codificação do arquivo CSV
        """

        try:
            path_destino = Path(dados_destino)                                  # Criar o objeto Path para o destino
            path_destino.parent.mkdir(parents=True, exist_ok=True)              # Criar diretórios pai, se necessário

            (
                pl.scan_csv(dados_origem, encoding=encoding, separator=",")
                    .select(lista_colunas)
                    #filter(pl.col("coluna_que_eu_quero_1").is_not_null())
                    .sink_parquet(dados_destino) 
            )

            print(f"✅ Arquivo salvo com sucesso em: {dados_destino}")
            
            return pl.read_parquet(dados_destino).head(5)                       # Retornar amostra de 5 linhas do DataFrame para verificar os dados

        except Exception as e:
            print(f"❌ Erro ao processar: {e}")
