

class DicionarioDataFile():
    """Classe retorna um dicionário com as informações das bases por id"""

    @staticmethod    
    def get_dict_data_file(id: int):
        """Função para retornar um dicionário com as informações das bases por id"""

        return next((item for item in DicionarioDataFile.dict_data_file if item["id"] == id), None)
    

    ######################################################
    ### Dicionário com as informações das bases por id ###
    ######################################################
    dict_data_file = [
        {
            "id": 1, 
            "base": "enem_teste_1",
            "ano": 2023,
            "encoding": "utf8-lossy",
            "caminho_arquivo_origem": "data/amostra_teste.csv",
            "caminho_arquivo_destino": "data/microdados-enem-2023-sp/microdados-enem-2023-sp.parquet",
            "fields_select": ["NU_INSCRICAO", "NU_ANO", "TP_FAIXA_ETARIA"]
        },
        {
            "id": 2, 
            "base": "enem_teste_2",
            "ano": 2022,
            "encoding": "utf8-lossy",
            "caminho_arquivo_origem": "data/amostra_teste.csv",
            "caminho_arquivo_destino": "microdados-enem-2022-sp.parquet",
            "fields_select": ["NU_INSCRICAO", "NU_ANO", "TP_FAIXA_ETARIA"]
        }
    ]
