import dask.dataframe as dd
import pyarrow as pa

csv_path = "microdados-enem-2023.csv"
ddf = dd.read_csv(csv_path, encoding="latin1", sep=";", assume_missing=True)  # dask lê com encoding latin1

# print schema para ver as colunas disponíveis
print("Colunas do CSV:")
print(ddf.columns.tolist())

# quero removemor colunas que não são necessárias para a análise, como por exemplo: 'SG_UF_RESIDENCIA', 'SG_UF_ESCOLA', 'SG_UF_PROVA_CN', 'SG_UF_PROVA_CH', 'SG_UF_PROVA_LC', 'SG_UF_PROVA_MT'
columns_to_drop = ['TP_ESTADO_CIVIL', 'TP_COR_RACA', 'TP_NACIONALIDADE', 'TP_ST_CONCLUSAO', 'TP_DEPENDENCIA_ADM_ESC', 'TP_LOCALIZACAO_ESC', 'TP_SIT_FUNC_ESC', 'CO_MUNICIPIO_PROVA', 'NO_MUNICIPIO_PROVA', 'CO_UF_PROVA', 'SG_UF_PROVA', 'TP_PRESENCA_CN', 'TP_PRESENCA_CH', 'TP_PRESENCA_LC', 'TP_PRESENCA_MT', 'CO_PROVA_CN', 'CO_PROVA_CH', 'CO_PROVA_LC', 'CO_PROVA_MT', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'TX_RESPOSTAS_CN', 'TX_RESPOSTAS_CH', 'TX_RESPOSTAS_LC', 'TX_RESPOSTAS_MT', 'TP_LINGUA', 'TX_GABARITO_CN', 'TX_GABARITO_CH', 'TX_GABARITO_LC', 'TX_GABARITO_MT', 'TP_STATUS_REDACAO', 'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5', 'NU_NOTA_REDACAO', 'Q001', 'Q002', 'Q003', 'Q004', 'Q005', 'Q006', 'Q007', 'Q008', 'Q009', 'Q010', 'Q011', 'Q012', 'Q013', 'Q014', 'Q015', 'Q016', 'Q017', 'Q018', 'Q019', 'Q020', 'Q021', 'Q022', 'Q023', 'Q024', 'Q025']

ddf = ddf.drop(columns=columns_to_drop)

# Filtro para manter apenas os registros de São Paulo (SG_UF_ESC == 'SP')
ddf = ddf[ddf['SG_UF_ESC'] == 'SP']

# Converter para Parquet
parquet_path = "microdados-enem-2023-sp.parquet"
ddf.to_parquet(parquet_path, engine='pyarrow', write_index=False)
print(f"Arquivo Parquet criado em: {parquet_path}")
