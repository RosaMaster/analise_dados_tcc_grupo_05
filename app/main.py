import os
import datetime
from service.leitura_dados import LeituraDados
from utils.dict_data_file import DicionarioDataFile


def main():
    """Função principal para extrair, processar e salvar os dados."""

    id = 1

    dict_data_file = DicionarioDataFile.get_dict_data_file(id)
    print(dict_data_file["id"])
    print(dict_data_file["base"])
    print(dict_data_file["ano"])
    print(dict_data_file["encoding"])
    print(dict_data_file["caminho_arquivo_origem"])
    print(dict_data_file["caminho_arquivo_destino"])
    print(dict_data_file["fields_drop"])


    # Verifica se o arquivo CSV existe
    if not os.path.exists(dict_data_file["caminho_arquivo_origem"]):
        print(f"Arquivo CSV não encontrado: {dict_data_file['caminho_arquivo_origem']}")
        return

    # Extrai e processa os dados
    dados_extraidos = LeituraDados.read_dados_origem(dict_data_file["caminho_arquivo_origem"], encoding=dict_data_file["encoding"])

    # print(type(dados_extraidos))
    # # Count the number of rows in the Dask DataFrame
    # num_rows = dados_extraidos.shape[0].compute()
    # print(f"Número de linhas no DataFrame: {num_rows}")

    # print schema para ver as colunas disponíveis
    # print("Colunas do CSV:")
    # print(dados_extraidos.columns.tolist())

    # print(dados_extraidos.head())  # Exibe as primeiras linhas do DataFrame para verificar os dados
    print(dados_extraidos.head())
    
    
    # ddf = dados_extraidos.extrair_e_processar_dados()

    # # Converter para Parquet
    # parquet_path = "data/teste1/microdados-enem-2023-sp.parquet"
    # ddf.to_parquet(parquet_path, engine='pyarrow', write_index=False)
    # print(f"Arquivo Parquet criado em: {parquet_path}")
    

if __name__ == "__main__":
    main()
