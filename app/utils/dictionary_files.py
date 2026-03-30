

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
            "base": "Microdados do Enem 2024",
            "ano": 2024,
            "atualizacao": "NA",
            "encoding": "utf8-lossy",
            "caminho_arquivo_origem": ".csv",
            "caminho_arquivo_destino": "data/microdados-enem-2024/microdados-enem-2024.parquet",
            "fields_select": ["NU_INSCRICAO", "NU_ANO", "TP_FAIXA_ETARIA", "TP_SEXO", "TP_ESCOLA", "CO_MUNICIPIO_PROVA", "NO_MUNICIPIO_PROVA", "SG_UF_PROVA"],
            "filters": "SG_UF_PROVA = \'SP\'"
        },
        {
            "id": 2, 
            "base": "Microdados do Enem 2023",
            "ano": 2023,
            "atualizacao": "2024-07-24",
            "encoding": "utf8-lossy",
            "caminho_arquivo_origem": "data/amostra_teste.csv",
            "caminho_arquivo_destino": "data/microdados-enem-2023/microdados-enem-2023.parquet",
            "fields_select": ["NU_INSCRICAO", "NU_ANO", "TP_FAIXA_ETARIA", "TP_SEXO", "TP_ESCOLA", "CO_MUNICIPIO_PROVA", "NO_MUNICIPIO_PROVA", "SG_UF_PROVA"],
            "filters": "SG_UF_PROVA = \'SP\'"
        },
        {
            "id": 3, 
            "base": "Microdados do Enem 2022",
            "ano": 2022,
            "atualizacao": "2024-08-08",
            "encoding": "utf8-lossy",
            "caminho_arquivo_origem": "data/amostra_teste.csv",
            "caminho_arquivo_destino": "data/microdados-enem-2022/microdados-enem-2022.parquet",
            "fields_select": ["NU_INSCRICAO", "NU_ANO", "TP_FAIXA_ETARIA", "TP_SEXO", "TP_ESCOLA", "CO_MUNICIPIO_PROVA", "NO_MUNICIPIO_PROVA", "SG_UF_PROVA"],
            "filters": "SG_UF_PROVA = \'SP\'"
        },
        {
            "id": 4, 
            "base": "Microdados do Enem 2021",
            "ano": 2021,
            "atualizacao": "NA",
            "encoding": "utf8-lossy",
            "caminho_arquivo_origem": "data/amostra_teste.csv",
            "caminho_arquivo_destino": "data/microdados-enem-2021/microdados-enem-2021.parquet",
            "fields_select": ["NU_INSCRICAO", "NU_ANO", "TP_FAIXA_ETARIA", "TP_SEXO", "TP_ESCOLA", "CO_MUNICIPIO_PROVA", "NO_MUNICIPIO_PROVA", "SG_UF_PROVA"],
            "filters": "SG_UF_PROVA = \'SP\'"
        },
        {
            "id": 5, 
            "base": "Microdados do Enem 2020",
            "ano": 2020,
            "atualizacao": "NA",
            "encoding": "utf8-lossy",
            "caminho_arquivo_origem": "data/amostra_teste.csv",
            "caminho_arquivo_destino": "data/microdados-enem-2020/microdados-enem-2020.parquet",
            "fields_select": ["NU_INSCRICAO", "NU_ANO", "TP_FAIXA_ETARIA", "TP_SEXO", "TP_ESCOLA", "CO_MUNICIPIO_PROVA", "NO_MUNICIPIO_PROVA", "SG_UF_PROVA"],
            "filters": "SG_UF_PROVA = \'SP\'"
        }
    ]
