import zipfile
import pandas as pd
from pathlib import Path
from config import UF_COD, PASTA_RENDIMENTO, PASTA_DATA
import io

Path(PASTA_RENDIMENTO).mkdir(parents=True, exist_ok=True)  # cria a pasta se não existir
# ─── CONFIGURAÇÃO ─────────────────────────────────────────────────────────────
ESTADOS = {
    11: "RO", 12: "AC", 13: "AM", 14: "RR", 15: "PA", 16: "AP", 17: "TO",
    21: "MA", 22: "PI", 23: "CE", 24: "RN", 25: "PB", 26: "PE", 27: "AL",
    28: "SE", 29: "BA",
    31: "MG", 32: "ES", 33: "RJ", 35: "SP",
    41: "PR", 42: "SC", 43: "RS",
    50: "MS", 51: "MT", 52: "GO", 53: "DF",
}
SIGLA = ESTADOS.get(UF_COD, str(UF_COD))

PASTA_ZIPS    = Path(PASTA_DATA) / "Rendimento"
ARQUIVO_FINAL = Path(PASTA_RENDIMENTO) / f"taxa_rendimento_{SIGLA.lower()}.csv"
# ─────────────────────────────────────────────────────────────────────────────


def extrair_xlsx_do_zip(zip_path):
    """Abre o ZIP e retorna o conteúdo do XLSX em bytes."""
    with zipfile.ZipFile(zip_path, "r") as z:
        for info in z.infolist():
            nome = info.filename
            if nome.lower().endswith(".xlsx") and "rend_municipios" in nome.lower():
                print(f"  → Encontrado: {Path(nome).name}")
                return z.read(info)
    return None


def carregar_xlsx(conteudo_bytes, ano):
    df = pd.read_excel(
        io.BytesIO(conteudo_bytes),
        header=None,
        skiprows=8,
        dtype=str,
        engine="openpyxl"
    )

    df = df.dropna(how="all")

    # filtra estado dinamicamente pela sigla
    df = df[df[2].str.strip() == SIGLA].copy()

    if df.empty:
        print(f"  ✗  Nenhum dado de {SIGLA} encontrado.")
        return pd.DataFrame()

    # seleciona e renomeia colunas por posição
    mapa = {
        0:  "ANO",
        3:  "CO_MUNICIPIO",
        4:  "NO_MUNICIPIO",
        5:  "LOCALIZACAO",
        6:  "DEPENDENCIA",
        7:  "APROVACAO_FUND_TOTAL",
        19: "APROVACAO_MED_TOTAL",
        25: "REPROVACAO_FUND_TOTAL",
        37: "REPROVACAO_MED_TOTAL",
        43: "ABANDONO_FUND_TOTAL",
        44: "ABANDONO_FUND_ANOS_INICIAIS",
        45: "ABANDONO_FUND_ANOS_FINAIS",
        55: "ABANDONO_MED_TOTAL",
        56: "ABANDONO_MED_1SERIE",
        57: "ABANDONO_MED_2SERIE",
        58: "ABANDONO_MED_3SERIE",
    }

    colunas_existentes = {k: v for k, v in mapa.items() if k < len(df.columns)}
    df = df[list(colunas_existentes.keys())].rename(columns=colunas_existentes)

    colunas_numericas = [v for v in colunas_existentes.values()
                         if v not in ("ANO", "CO_MUNICIPIO", "NO_MUNICIPIO",
                                      "LOCALIZACAO", "DEPENDENCIA")]
    for col in colunas_numericas:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(",", ".").str.strip(),
            errors="coerce"
        )

    df["ANO"] = int(ano)
    return df


def processar_todos_os_anos(pasta_zips):
    pasta_zips = Path(pasta_zips)
    dfs = []

    zips = sorted(pasta_zips.glob("tx_rend_municipios_*.zip"))

    if not zips:
        print(f"Nenhum ZIP de rendimento encontrado em: {pasta_zips}")
        return pd.DataFrame()

    print(f"Encontrados {len(zips)} arquivos ZIP.\n")

    for zip_path in zips:
        ano = zip_path.stem.replace("tx_rend_municipios_", "")
        print(f"[{ano}] Processando {zip_path.name}...")

        conteudo = extrair_xlsx_do_zip(zip_path)
        if conteudo is None:
            print(f"  ✗  XLSX não encontrado dentro do ZIP.")
            continue

        df = carregar_xlsx(conteudo, ano)
        if df.empty:
            print(f"  ✗  Nenhum dado carregado para {ano}.")
            continue

        print(f"  ✓  {len(df):,} registros de {SIGLA} carregados.")
        dfs.append(df)

    if not dfs:
        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True, sort=False)


# ─── EXECUÇÃO ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":

    print("=" * 60)
    print(f"TAXAS DE RENDIMENTO — Estado: {SIGLA} (código {UF_COD})")
    print("=" * 60)

    df = processar_todos_os_anos(PASTA_ZIPS)

    if df.empty:
        print("Nenhum dado processado.")
    else:
        print()
        print("=" * 60)
        print("RESUMO")
        print("=" * 60)
        print(f"Total de registros: {len(df):,}")
        print(f"Anos disponíveis:   {sorted(df['ANO'].unique())}")
        print(f"Municípios únicos:  {df['CO_MUNICIPIO'].nunique()}")
        print(f"Colunas:            {list(df.columns)}")
        print()
        print("Prévia:")
        print(df.head(10).to_string())

        # guarda versão completa antes de filtrar
        df_raw = df.copy()

        # filtra só Total x Total — uma linha por município por ano
        df = df[
            (df["LOCALIZACAO"].str.strip() == "Total") &
            (df["DEPENDENCIA"].str.strip() == "Total")
        ].copy()

        print(f"Após filtro Total x Total: {len(df):,} registros")
        df.to_csv(ARQUIVO_FINAL, index=False, sep=";", encoding="utf-8-sig")
        print(f"✓ Salvo: {ARQUIVO_FINAL}")

        # salva versão por dependência (estadual + municipal separados)
        df_redes = df_raw[
            (df_raw["LOCALIZACAO"].str.strip() == "Total") &
            (df_raw["DEPENDENCIA"].str.strip().isin(["Estadual", "Municipal"]))
        ].copy()

        ARQUIVO_REDES = Path(PASTA_RENDIMENTO) / f"taxa_rendimento_redes_{SIGLA.lower()}.csv"
        df_redes.to_csv(ARQUIVO_REDES, index=False, sep=";", encoding="utf-8-sig")
        print(f"✓ Versão por rede salva: {ARQUIVO_REDES}")