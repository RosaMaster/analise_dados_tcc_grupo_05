import polars as pl
from pathlib import Path


def main():
    
    # leitura do arquivo parquet
    caminho_arquivo_parquet = Path("data/microdados-enem-2023")
    df = pl.read_parquet(caminho_arquivo_parquet)

    print(df.head())


if __name__ == "__main__":
    main()
