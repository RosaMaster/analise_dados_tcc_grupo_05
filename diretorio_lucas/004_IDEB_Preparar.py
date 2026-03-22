import pandas as pd
from pathlib import Path
from config import UF_COD, PASTA_SAIDA, PASTA_IDEB

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
ANOS  = [2019, 2021, 2023]

ENTRADA = Path(PASTA_IDEB) / f"ideb_bruto_{SIGLA.lower()}.csv"
SAIDA   = Path(PASTA_IDEB) / f"ideb_municipios_{SIGLA.lower()}.csv"
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print(f"IDEB PREPARAÇÃO — Estado: {SIGLA} (código {UF_COD})")
print("=" * 60)

if not ENTRADA.exists():
    print(f"✗ Arquivo bruto não encontrado: {ENTRADA}")
    print("  Execute primeiro o script 004a_IDEB_Extrair.py")
    exit()

df_bruto = pd.read_csv(ENTRADA, sep=";", dtype=str)
print(f"Carregado: {len(df_bruto)} registros | níveis: {df_bruto['NIVEL'].unique().tolist()}")

dfs = []

for nivel in df_bruto["NIVEL"].unique():
    df = df_bruto[df_bruto["NIVEL"] == nivel].copy()

    cols_id   = ["CO_MUNICIPIO", "NO_MUNICIPIO"]
    cols_ideb = [f"VL_OBSERVADO_{ano}" for ano in ANOS if f"VL_OBSERVADO_{ano}" in df.columns]

    df = df[cols_id + cols_ideb].copy()

    # wide → long
    df_long = df.melt(
        id_vars=cols_id,
        value_vars=cols_ideb,
        var_name="VAR",
        value_name=f"IDEB_{nivel}"
    )
    df_long["ANO"] = df_long["VAR"].str.extract(r"(\d{4})").astype(int)
    df_long = df_long.drop(columns=["VAR"])
    df_long[f"IDEB_{nivel}"] = pd.to_numeric(df_long[f"IDEB_{nivel}"], errors="coerce")
    df_long["CO_MUNICIPIO"]  = df_long["CO_MUNICIPIO"].astype(str)

    print(f"  {nivel}: {df_long['CO_MUNICIPIO'].nunique()} municípios | {sorted(df_long['ANO'].unique())}")
    dfs.append(df_long)

# junta os três níveis em wide — igual ao formato original
df = dfs[0]
for df_nivel in dfs[1:]:
    df = df.merge(df_nivel, on=["CO_MUNICIPIO", "NO_MUNICIPIO", "ANO"], how="outer")

df = df.sort_values(["CO_MUNICIPIO", "ANO"]).reset_index(drop=True)

print(f"\nShape: {df.shape}")
print(f"Anos: {sorted(df['ANO'].unique())}")
print(f"Municípios: {df['CO_MUNICIPIO'].nunique()}")
print(df.head(6).to_string())

df.to_csv(SAIDA, sep=";", index=False, encoding="utf-8-sig")
print(f"\n✓ Salvo em: {SAIDA}")