import os
import datetime
from service.etl_dados import EtlDados
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
    print(dict_data_file["fields_select"])

    print(type(dict_data_file["fields_select"]))


    # Verifica se o arquivo CSV existe
    if not os.path.exists(dict_data_file["caminho_arquivo_origem"]):
        print(f"Arquivo CSV não encontrado: {dict_data_file['caminho_arquivo_origem']}")
        return

    # Leitura dos dados usando biblioteca Polars
    dados_extraidos = EtlDados.save_parquet(dict_data_file["caminho_arquivo_origem"], dict_data_file["caminho_arquivo_destino"], dict_data_file["fields_select"], dict_data_file["encoding"])

    print(dados_extraidos)
    

if __name__ == "__main__":
    main()
