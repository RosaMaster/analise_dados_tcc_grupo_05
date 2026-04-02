import os
from service.etl_dados import ExtracTransformLoadData
from utils.dictionary_files import DicionarioDataFile


def main():
    """Função principal para extrair, processar e salvar os dados."""

    lista_ids = [2]

    try:
        for id in lista_ids:
            dict_data_file = DicionarioDataFile.get_dict_data_file(id)
            
            print(dict_data_file["id"])
            print(dict_data_file["base"])
            print(dict_data_file["ano"])
            print(dict_data_file["encoding"])
            print(dict_data_file["caminho_arquivo_origem"])
            print(dict_data_file["caminho_arquivo_destino"])
            print(dict_data_file["fields_select"])
            print(dict_data_file["filters"])

            print(type(dict_data_file["filters"]))

            # Validador de existência do arquivo de origem
            if not os.path.exists(dict_data_file["caminho_arquivo_origem"]):
                print(f"❌ Arquivo não encontrado: {dict_data_file['caminho_arquivo_origem']}. Verifique o caminho e tente novamente!")
                return
            
            # ETL usando a lib polars
            dados_extraidos = ExtracTransformLoadData.csv_to_parquet(dict_data_file["caminho_arquivo_origem"], dict_data_file["caminho_arquivo_destino"], dict_data_file["fields_select"], dict_data_file["filters"], dict_data_file["encoding"])

            print(dados_extraidos)

            print(f"✅ Processamento concluído para o ID: {id}. Base: {dict_data_file['base']}")

        print("✅ Todos os arquivos foram processados com sucesso!")

    except Exception as e:
        print(f"❌ Ocorreu um error: {e}")
    
if __name__ == "__main__":
    main()
