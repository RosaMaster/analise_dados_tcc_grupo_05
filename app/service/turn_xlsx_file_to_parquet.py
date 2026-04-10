import polars as pl
import polars.selectors as cs

# OBS: Antes de rodar os scripts baixar os dados baixar os dados no link abaixo
# https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/taxas-de-rendimento-escolar

# 1. Carrega apenas as linhas do cabeçalho
def turn_xlsx_in_parquet(file): 
    header_rows = pl.read_excel(
        file,
        has_header=False,
        read_options={"n_rows": 3, "skip_rows": 6} # Ajuste conforme necessário
    )

    # 2. Transpor e aplicar forward_fill
    header_long = (
        header_rows.transpose()
        .select([
            pl.all().forward_fill()
        ])
    )

    # 3. Criar a lista de nomes únicos para as colunas
    new_columns = [
        "_".join([str(item).strip().replace(" ", "_") for item in row if item is not None and str(item) != "None"])
        for row in header_long.iter_rows()
    ]

    # 4. Ler os dados (sem o cabeçalho)
    df = pl.read_excel(
        file,
        has_header=False,
        read_options={"skip_rows": 9},
    )

    # 5. Aplicar os novos nomes às colunas do DataFrame
    df.columns = new_columns

    df = df.filter(
        pl.col("SG_UF") == "SP"
        ).drop([
    
    # 1. IDENTIFICADORES NÃO SINTÁTICOS
    "NO_REGIAO",
    "SG_UF",
    "NO_CATEGORIA",
    "NO_DEPENDENCIA",
    "NO_MUNICIPIO", 

    # 2. TAXAS DE APROVAÇÃO (CAT 1)
    # Motivo: Aprovação = 100 - (Reprovação + Abandono). 
    "Ensino_Fundamental_de_8_e_9_anos_1º_Ano_1_CAT_FUN_01",
    "Ensino_Fundamental_de_8_e_9_anos_2º_Ano_1_CAT_FUN_02",
    "Ensino_Fundamental_de_8_e_9_anos_3º_Ano_1_CAT_FUN_03",
    "Ensino_Fundamental_de_8_e_9_anos_4º_Ano_1_CAT_FUN_04",
    "Ensino_Fundamental_de_8_e_9_anos_5º_Ano_1_CAT_FUN_05",
    "Ensino_Fundamental_de_8_e_9_anos_6º_Ano_1_CAT_FUN_06",
    "Ensino_Fundamental_de_8_e_9_anos_7º_Ano_1_CAT_FUN_07",
    "Ensino_Fundamental_de_8_e_9_anos_8º_Ano_1_CAT_FUN_08",
    "Ensino_Fundamental_de_8_e_9_anos_9º_Ano_1_CAT_FUN_09",
    "Ensino_Médio_1ª_série_1_CAT_MED_01",
    "Ensino_Médio_2ª_série_1_CAT_MED_02",
    "Ensino_Médio_3ª_série_1_CAT_MED_03",
    "Ensino_Médio_4ª_série_1_CAT_MED_04",
    "Ensino_Médio_Não-Seriado_1_CAT_MED_NS",

    # 3. SÉRIES ESPECÍFICAS DE REPROVAÇÃO (CAT 2)
    "Ensino_Fundamental_de_8_e_9_anos_1º_Ano_2_CAT_FUN_01",
    "Ensino_Fundamental_de_8_e_9_anos_2º_Ano_2_CAT_FUN_02",
    "Ensino_Fundamental_de_8_e_9_anos_3º_Ano_2_CAT_FUN_03",
    "Ensino_Fundamental_de_8_e_9_anos_4º_Ano_2_CAT_FUN_04",
    "Ensino_Fundamental_de_8_e_9_anos_5º_Ano_2_CAT_FUN_05",
    "Ensino_Fundamental_de_8_e_9_anos_6º_Ano_2_CAT_FUN_06",
    "Ensino_Fundamental_de_8_e_9_anos_7º_Ano_2_CAT_FUN_07",
    "Ensino_Fundamental_de_8_e_9_anos_8º_Ano_2_CAT_FUN_08",
    "Ensino_Fundamental_de_8_e_9_anos_9º_Ano_2_CAT_FUN_09",
    "Ensino_Médio_1ª_série_2_CAT_MED_01",
    "Ensino_Médio_2ª_série_2_CAT_MED_02",
    "Ensino_Médio_3ª_série_2_CAT_MED_03",

    # 4. COLUNAS COM ALTA TAXA DE VALORES NULOS (NULLS)
    "Ensino_Médio_4ª_série_2_CAT_MED_04",
    "Ensino_Médio_Não-Seriado_2_CAT_MED_NS",
    "Ensino_Médio_4ª_série_3_CAT_MED_04",
    "Ensino_Médio_Não-Seriado_3_CAT_MED_NS",

    # 5. DETALHAMENTO EXCESSIVO DE ABANDONO (CAT 3)
    "Ensino_Fundamental_de_8_e_9_anos_1º_Ano_3_CAT_FUN_01",
    "Ensino_Fundamental_de_8_e_9_anos_2º_Ano_3_CAT_FUN_02",
    "Ensino_Fundamental_de_8_e_9_anos_3º_Ano_3_CAT_FUN_03",
    "Ensino_Fundamental_de_8_e_9_anos_4º_Ano_3_CAT_FUN_04",
    "Ensino_Fundamental_de_8_e_9_anos_5º_Ano_3_CAT_FUN_05",
    "Ensino_Fundamental_de_8_e_9_anos_6º_Ano_3_CAT_FUN_06",
    "Ensino_Fundamental_de_8_e_9_anos_7º_Ano_3_CAT_FUN_07",
    "Ensino_Fundamental_de_8_e_9_anos_8º_Ano_3_CAT_FUN_08",
    "Ensino_Fundamental_de_8_e_9_anos_9º_Ano_3_CAT_FUN_09",
    "Ensino_Médio_1ª_série_3_CAT_MED_01",
    "Ensino_Médio_2ª_série_3_CAT_MED_02",
    "Ensino_Médio_3ª_série_3_CAT_MED_03"
        ])
    df = df.with_columns(
            cs.string().replace("--", None)
        )
    
    
    file_name = file.replace(".xlsx", "")
    df.write_parquet(f"./{file_name}.parquet")

xlsx_paths = [
    "app/Rendimentos_TCC/tx_rend_municipios_2020.xlsx",
    "app/Rendimentos_TCC/tx_rend_municipios_2021.xlsx",
    "app/Rendimentos_TCC/tx_rend_municipios_2022.xlsx",
    "app/Rendimentos_TCC/tx_rend_municipios_2023.xlsx",
    "app/Rendimentos_TCC/tx_rend_municipios_2024.xlsx"
    ]


for i in xlsx_paths:
    print(f"Iniciando arquivo: {i}")
    try:
        turn_xlsx_in_parquet(i)
        print('Arquivo .parquet criado com Sucesso')
    except Exception as e:
        print(f"Erro ao processar {i}: {e}")