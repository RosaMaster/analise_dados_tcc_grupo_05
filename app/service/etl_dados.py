import polars as pl

class EtlDados:
    
    # @staticmethod
    # def read_polars(csv_path, encoding):
    #     """Função para ler os dados de um arquivo CSV usando Polars.

    #     Returns:
    #         _type_: Retorna um DataFrame _pl.DataFrame_ do Polars com os dados lidos do arquivo CSV.
    #     """
        
    #     dataframe = pl.read_csv(csv_path, encoding=encoding, separator=";")

    #     return dataframe
    

    @staticmethod
    def save_parquet(dados_origem, dados_destino, lista_colunas, encoding):
        """_summary_

        Args:
            dados_origem (_type_): _description_
            dados_destino (_type_): _description_
            lista_colunas (_type_): _description_
        """

        try:
            (
                pl.scan_csv(dados_origem, encoding=encoding, separator=",")
                    .select(lista_colunas)
                    #filter(pl.col("coluna_que_eu_quero_1").is_not_null())
                    .sink_parquet(dados_destino) 
            )

            # retornar amostra de 5 linhas do DataFrame para verificar os dados
            return pl.read_parquet(dados_destino).head(5)

        except Exception as e:
            print(f"Erro ao processar: {e}")