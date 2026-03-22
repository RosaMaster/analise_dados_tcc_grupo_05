import pandas as pd
from pathlib import Path
from config import UF_COD, PASTA_SAIDA, PASTA_CENSO

# ─── CONFIGURAÇÃO ────────────────────────────────────────────────────────────
ESTADOS = {
    11: "RO", 12: "AC", 13: "AM", 14: "RR", 15: "PA", 16: "AP", 17: "TO",
    21: "MA", 22: "PI", 23: "CE", 24: "RN", 25: "PB", 26: "PE", 27: "AL",
    28: "SE", 29: "BA",
    31: "MG", 32: "ES", 33: "RJ", 35: "SP",
    41: "PR", 42: "SC", 43: "RS",
    50: "MS", 51: "MT", 52: "GO", 53: "DF",
}
SIGLA = ESTADOS.get(UF_COD, str(UF_COD))

ARQUIVO_FINAL = Path(PASTA_CENSO) / f"censo_escolar_{SIGLA.lower()}.csv"
# ─────────────────────────────────────────────────────────────────────────────

# Colunas que existem nos anos antigos (2019-2024) — arquivo único por escola
COLUNAS_ANTIGO = [
    "NU_ANO_CENSO",
    "CO_UF",
    "CO_MUNICIPIO",
    "NO_MUNICIPIO",
    "TP_DEPENDENCIA",            # 1=federal, 2=estadual, 3=municipal, 4=privada
    "TP_LOCALIZACAO",            # 1=urbana, 2=rural
    "TP_SITUACAO_FUNCIONAMENTO", # 1=em atividade
    # matrículas
    "QT_MAT_BAS",
    "QT_MAT_FUND",
    "QT_MAT_MED",
    "QT_MAT_EJA",
    # infraestrutura
    "IN_AGUA_POTAVEL",
    "IN_ENERGIA_REDE_PUBLICA",
    "IN_ESGOTO_REDE_PUBLICA",
    "IN_BIBLIOTECA",
    "IN_LABORATORIO_INFORMATICA",
    "IN_INTERNET",
    "IN_INTERNET_ALUNOS",
    "IN_QUADRA_ESPORTES",
    "IN_REFEITORIO",
    # docentes
    "QT_DOC_BAS",
    "QT_DOC_MED",
    "QT_DOC_FUND",
]

COLUNAS_ESCOLA_2025 = [
    "NU_ANO_CENSO", "CO_UF", "CO_MUNICIPIO", "NO_MUNICIPIO", "CO_ENTIDADE",
    "TP_DEPENDENCIA", "TP_LOCALIZACAO", "TP_SITUACAO_FUNCIONAMENTO",
    "IN_AGUA_POTAVEL", "IN_ENERGIA_REDE_PUBLICA", "IN_ESGOTO_REDE_PUBLICA",
    "IN_BIBLIOTECA", "IN_LABORATORIO_INFORMATICA", "IN_INTERNET",
    "IN_INTERNET_ALUNOS", "IN_QUADRA_ESPORTES", "IN_REFEITORIO",
]

COLUNAS_MAT_2025 = [
    "CO_ENTIDADE", "QT_MAT_BAS", "QT_MAT_FUND", "QT_MAT_MED", "QT_MAT_EJA",
]

COLUNAS_SOMA = [
    "QT_MAT_BAS", "QT_MAT_FUND", "QT_MAT_MED", "QT_MAT_EJA",
    "QT_DOC_BAS", "QT_DOC_MED", "QT_DOC_FUND",
]
COLUNAS_MEDIA = [
    "IN_AGUA_POTAVEL", "IN_ENERGIA_REDE_PUBLICA", "IN_ESGOTO_REDE_PUBLICA",
    "IN_BIBLIOTECA", "IN_LABORATORIO_INFORMATICA", "IN_INTERNET",
    "IN_INTERNET_ALUNOS", "IN_QUADRA_ESPORTES", "IN_REFEITORIO",
]


def carregar_anos_antigos(pasta_saida):
    pasta_saida = Path(pasta_saida)
    dfs = []

    for ano in [str(a) for a in range(2019, 2025)]:
        pasta_ano = pasta_saida / ano
        csvs = list(pasta_ano.glob("microdados_ed_basica_*.csv"))

        if not csvs:
            print(f"  [{ano}] arquivo não encontrado, pulando.")
            continue

        csv_path = csvs[0]
        print(f"  [{ano}] Carregando {csv_path.name}...")

        try:
            df_cols = pd.read_csv(csv_path, sep=";", encoding="latin-1", nrows=0)
            cols_disponiveis = [c for c in COLUNAS_ANTIGO if c in df_cols.columns]
            cols_faltando    = [c for c in COLUNAS_ANTIGO if c not in df_cols.columns]

            if cols_faltando:
                print(f"         ⚠️  Colunas ausentes em {ano}: {cols_faltando}")

            df = pd.read_csv(
                csv_path, sep=";", encoding="latin-1",
                low_memory=False, usecols=cols_disponiveis
            )

            df = df[df["CO_UF"] == UF_COD].copy()

            if "TP_SITUACAO_FUNCIONAMENTO" in df.columns:
                df = df[df["TP_SITUACAO_FUNCIONAMENTO"] == 1]

            df["ANO"] = int(ano)
            dfs.append(df)
            print(f"         {len(df):,} escolas em {SIGLA}.")

        except Exception as e:
            print(f"         ✗ Erro: {e}")

    if not dfs:
        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True, sort=False)


def carregar_2025(pasta_saida):
    pasta_saida = Path(pasta_saida)
    pasta_ano   = pasta_saida / "2025"

    print("  [2025] Carregando Tabela_Escola...")
    try:
        # tenta nome em minúsculo primeiro, depois maiúsculo
        for nome in ["tabela_escola_2025.csv", "Tabela_Escola_2025.csv"]:
            if (pasta_ano / nome).exists():
                df_escola = pd.read_csv(
                    pasta_ano / nome, sep=";", encoding="latin-1",
                    low_memory=False, usecols=COLUNAS_ESCOLA_2025
                )
                break
        df_escola = df_escola[df_escola["CO_UF"] == UF_COD].copy()
        if "TP_SITUACAO_FUNCIONAMENTO" in df_escola.columns:
            df_escola = df_escola[df_escola["TP_SITUACAO_FUNCIONAMENTO"] == 1]
        print(f"         {len(df_escola):,} escolas em {SIGLA}.")
    except Exception as e:
        print(f"         ✗ Erro escola: {e}")
        return pd.DataFrame()

    print("  [2025] Carregando Tabela_Matricula...")
    try:
        for nome in ["tabela_matricula_2025.csv", "Tabela_Matricula_2025.csv"]:
            if (pasta_ano / nome).exists():
                df_mat = pd.read_csv(
                    pasta_ano / nome, sep=";", encoding="latin-1",
                    low_memory=False, usecols=COLUNAS_MAT_2025
                )
                break
        print(f"         {len(df_mat):,} registros de matrícula.")
    except Exception as e:
        print(f"         ✗ Erro matrícula: {e}")
        return pd.DataFrame()

    df = df_escola.merge(df_mat, on="CO_ENTIDADE", how="left")
    df["ANO"] = 2025
    return df


def agregar_por_municipio(df):
    agg_dict = {}
    for col in COLUNAS_SOMA:
        if col in df.columns:
            agg_dict[col] = "sum"
    for col in COLUNAS_MEDIA:
        if col in df.columns:
            agg_dict[col] = "mean"
    if "CO_ENTIDADE" in df.columns:
        agg_dict["CO_ENTIDADE"] = "count"

    agg_dict = {k: v for k, v in agg_dict.items() if v is not None}

    df_mun = df.groupby(
        ["ANO", "CO_MUNICIPIO", "NO_MUNICIPIO", "TP_DEPENDENCIA", "TP_LOCALIZACAO"],
        as_index=False
    ).agg(agg_dict)

    if "CO_ENTIDADE" in df_mun.columns:
        df_mun = df_mun.rename(columns={"CO_ENTIDADE": "QT_ESCOLAS"})

    # filtra só rede pública (estadual + municipal) e urbana — BUG CORRIGIDO: era isin([2,2])
    df_mun = df_mun[
        (df_mun["TP_DEPENDENCIA"].isin([2, 3])) &
        (df_mun["TP_LOCALIZACAO"] == 1)
    ].copy()

    return df_mun


# ─── EXECUÇÃO ────────────────────────────────────────────────────────────────
if __name__ == "__main__":

    print("=" * 60)
    print(f"CENSO ESCOLAR — Estado: {SIGLA} (código {UF_COD})")
    print("=" * 60)

    print("\nCarregando anos antigos (2019-2024)...")
    df_antigo = carregar_anos_antigos(PASTA_CENSO)

    print("\nCarregando 2025...")
    df_2025 = carregar_2025(PASTA_CENSO)

    print("\nConcatenando todos os anos...")
    df_total = pd.concat([df_antigo, df_2025], ignore_index=True, sort=False)
    print(f"Total de registros (nível escola): {len(df_total):,}")
    print(f"Anos disponíveis: {sorted(df_total['ANO'].unique())}")
    print(f"Municípios únicos: {df_total['CO_MUNICIPIO'].nunique()}")

    print("\nAgregando por município e ano...")
    df_final = agregar_por_municipio(df_total)
    print(f"Total de registros (nível município): {len(df_final):,}")
    print(f"Municípios únicos após filtro: {df_final['CO_MUNICIPIO'].nunique()}")

    print(f"\nSalvando em {ARQUIVO_FINAL}...")
    df_final.to_csv(ARQUIVO_FINAL, index=False, sep=";", encoding="utf-8-sig")
    print("✓ Salvo!")

    print("\n" + "=" * 60)
    print("PRÉVIA DO DATAFRAME FINAL")
    print("=" * 60)
    print(df_final.head(10).to_string())

