

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
            "encoding": "latin1",
            "caminho_arquivo_origem": "data/amostra_teste.csv",
            "caminho_arquivo_destino": "data/teste1/microdados-enem-2023-sp.parquet",
            "fields_drop": ["TP_ESTADO_CIVIL", "TP_COR_RACA", "TP_NACIONALIDADE", "TP_ST_CONCLUSAO", "TP_DEPENDENCIA_ADM_ESC", "TP_LOCALIZACAO_ESC", "TP_SIT_FUNC_ESC", "CO_MUNICIPIO_PROVA", "NO_MUNICIPIO_PROVA", "CO_UF_PROVA", "SG_UF_PROVA", "TP_PRESENCA_CN", "TP_PRESENCA_CH", "TP_PRESENCA_LC", "TP_PRESENCA_MT", "CO_PROVA_CN", "CO_PROVA_CH", "CO_PROVA_LC", "CO_PROVA_MT", "NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "TX_RESPOSTAS_CN", "TX_RESPOSTAS_CH", "TX_RESPOSTAS_LC", "TX_RESPOSTAS_MT", "TP_LINGUA", "TX_GABARITO_CN", "TX_GABARITO_CH", "TX_GABARITO_LC", "TX_GABARITO_MT", "TP_STATUS_REDACAO", "NU_NOTA_COMP1", "NU_NOTA_COMP2", "NU_NOTA_COMP3", "NU_NOTA_COMP4", "NU_NOTA_COMP5", "NU_NOTA_REDACAO", "Q001", "Q002", "Q003", "Q004", "Q005", "Q006", "Q007", "Q008", "Q009", "Q010", "Q011", "Q012", "Q013", "Q014", "Q015", "Q016", "Q017", "Q018", "Q019", "Q020", "Q021", "Q022", "Q023", "Q024", "Q025"]
        },
        {
            "id": 2, 
            "base": "enem_teste_2",
            "ano": 2023,
            "encoding": "latin1",
            "caminho_arquivo_origem": "data/dados_completos.csv",
            "caminho_arquivo_destino": "data/teste1/microdados-enem-2023-sp.parquet",
            "fields_drop": ["TP_ESTADO_CIVIL", "TP_COR_RACA", "TP_NACIONALIDADE", "TP_ST_CONCLUSAO", "TP_DEPENDENCIA_ADM_ESC", "TP_LOCALIZACAO_ESC", "TP_SIT_FUNC_ESC", "CO_MUNICIPIO_PROVA", "NO_MUNICIPIO_PROVA", "CO_UF_PROVA", "SG_UF_PROVA", "TP_PRESENCA_CN", "TP_PRESENCA_CH", "TP_PRESENCA_LC", "TP_PRESENCA_MT", "CO_PROVA_CN", "CO_PROVA_CH", "CO_PROVA_LC", "CO_PROVA_MT", "NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "TX_RESPOSTAS_CN", "TX_RESPOSTAS_CH", "TX_RESPOSTAS_LC", "TX_RESPOSTAS_MT", "TP_LINGUA", "TX_GABARITO_CN", "TX_GABARITO_CH", "TX_GABARITO_LC", "TX_GABARITO_MT", "TP_STATUS_REDACAO", "NU_NOTA_COMP1", "NU_NOTA_COMP2", "NU_NOTA_COMP3", "NU_NOTA_COMP4", "NU_NOTA_COMP5", "NU_NOTA_REDACAO", "Q001", "Q002", "Q003", "Q004", "Q005", "Q006", "Q007", "Q008", "Q009", "Q010", "Q011", "Q012", "Q013", "Q014", "Q015", "Q016", "Q017", "Q018", "Q019", "Q020", "Q021", "Q022", "Q023", "Q024", "Q025"]
        }
    ]
