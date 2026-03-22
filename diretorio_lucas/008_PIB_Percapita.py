import pandas as pd
from pathlib import Path
from config import UF_COD, PASTA_PIB_PER_CAPITA, PASTA_DATA

Path(PASTA_PIB_PER_CAPITA).mkdir(parents=True, exist_ok=True)  # cria a pasta se não existir
# ─── CONFIGURAÇÃO ─────────────────────────────────────────────────────────────
ESTADOS = {
    11: "RO", 12: "AC", 13: "AM", 14: "RR", 15: "PA", 16: "AP", 17: "TO",
    21: "MA", 22: "PI", 23: "CE", 24: "RN", 25: "PB", 26: "PE", 27: "AL",
    28: "SE", 29: "BA",
    31: "MG", 32: "ES", 33: "RJ", 35: "SP",
    41: "PR", 42: "SC", 43: "RS",
    50: "MS", 51: "MT", 52: "GO", 53: "DF",
}
SIGLA      = ESTADOS.get(UF_COD, str(UF_COD))
PREFIXO_UF = str(UF_COD).zfill(2)

ARQUIVO_PIB = Path(PASTA_DATA) / "PIB_per_capita" / "tabela5938.xlsx"
ARQUIVO_POP = Path(PASTA_DATA) / "PIB_per_capita" /  "Agregados_por_municipios_basico_BR.xlsx"
SAIDA       = Path(PASTA_PIB_PER_CAPITA) / f"pib_percapita_{SIGLA.lower()}.csv"

ANOS = [2019, 2020, 2021, 2022, 2023]
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print(f"PIB PER CAPITA — Estado: {SIGLA} (código {UF_COD})")
print("=" * 60)

# ─── CARREGA PIB ──────────────────────────────────────────────────────────────
if not ARQUIVO_PIB.exists():
    print(f"✗ Arquivo não encontrado: {ARQUIVO_PIB}")
    exit()

print("Carregando PIB (tabela 5938)...")
df_pib = pd.read_excel(ARQUIVO_PIB, skiprows=3)
df_pib.columns = ["TIPO", "CO_MUNICIPIO", "NM_MUNICIPIO",
                  "PIB_2014", "PIB_2017", "PIB_2018",
                  "PIB_2019", "PIB_2020", "PIB_2021", "PIB_2022", "PIB_2023"]
df_pib = df_pib.dropna(subset=["CO_MUNICIPIO"])
print(f"  ✓ {len(df_pib)} municípios carregados")

# ─── CARREGA POPULAÇÃO ────────────────────────────────────────────────────────
if not ARQUIVO_POP.exists():
    print(f"✗ Arquivo não encontrado: {ARQUIVO_POP}")
    exit()

print("Carregando população (Censo 2022)...")
df_pop = pd.read_excel(ARQUIVO_POP)
df_pop = df_pop[["CD_MUN", "v0001"]].rename(
    columns={"CD_MUN": "CO_MUNICIPIO", "v0001": "POPULACAO"}
)
print(f"  ✓ {len(df_pop)} municípios carregados")

# ─── JOIN ─────────────────────────────────────────────────────────────────────
df_pib["CO_MUNICIPIO"] = df_pib["CO_MUNICIPIO"].astype(int).astype(str)
df_pop["CO_MUNICIPIO"] = df_pop["CO_MUNICIPIO"].astype(str)

df = df_pib.merge(df_pop, on="CO_MUNICIPIO", how="left")

# ─── PIB PER CAPITA ───────────────────────────────────────────────────────────
for ano in ANOS:
    col_pib = f"PIB_{ano}"
    if col_pib in df.columns:
        df[f"PIB_PERCAPITA_{ano}"] = (df[col_pib] * 1000) / df["POPULACAO"]
    else:
        print(f"  ⚠️  Coluna {col_pib} não encontrada no arquivo")

# filtra estado pelo prefixo do código IBGE
df = df[df["CO_MUNICIPIO"].str.startswith(PREFIXO_UF)].copy()

print(f"\nMunicípios {SIGLA}: {len(df)}")

cols_preview = ["CO_MUNICIPIO", "NM_MUNICIPIO", "POPULACAO"] + \
               [f"PIB_PERCAPITA_{ano}" for ano in ANOS if f"PIB_PERCAPITA_{ano}" in df.columns]
print(df[cols_preview].head(10).to_string())

df.to_csv(SAIDA, sep=";", index=False, encoding="utf-8-sig")
print(f"\n✓ Salvo em: {SAIDA}")