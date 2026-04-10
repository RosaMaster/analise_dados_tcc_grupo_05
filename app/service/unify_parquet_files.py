import polars as pl
import polars.selectors as cs


df_tx_rend_municipios_2020 = pl.read_parquet("app/Rendimentos_TCC/tx_rend_municipios_2020.parquet")
df_tx_rend_municipios_2021 = pl.read_parquet("app/Rendimentos_TCC/tx_rend_municipios_2021.parquet")
df_tx_rend_municipios_2022 = pl.read_parquet("app/Rendimentos_TCC/tx_rend_municipios_2022.parquet")
df_tx_rend_municipios_2023 = pl.read_parquet("app/Rendimentos_TCC/tx_rend_municipios_2023.parquet")
df_tx_rend_municipios_2024 = pl.read_parquet("app/Rendimentos_TCC/tx_rend_municipios_2024.parquet")

unified_tx_rend_municipios = pl.concat(
    [
        df_tx_rend_municipios_2020,
        df_tx_rend_municipios_2021,
        df_tx_rend_municipios_2022,
        df_tx_rend_municipios_2023,
        df_tx_rend_municipios_2024,
    ],
    how='vertical'
)

unified_tx_rend_municipios.write_parquet(f"app/Rendimentos_TCC/unified_tx_rend_municipios.parquet")