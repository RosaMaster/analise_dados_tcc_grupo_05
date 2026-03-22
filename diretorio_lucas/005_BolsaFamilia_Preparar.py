import pandas as pd
from pathlib import Path
from config import UF_COD, PASTA_BOLSA_FAMILIA

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

ENTRADA = Path(PASTA_BOLSA_FAMILIA) / f"bolsa_familia_bruto_{SIGLA.lower()}.csv"
SAIDA   = Path(PASTA_BOLSA_FAMILIA) / f"bolsa_familia_{SIGLA.lower()}.csv"
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print(f"BOLSA FAMÍLIA PREPARAÇÃO — Estado: {SIGLA} (código {UF_COD})")
print("=" * 60)

if not ENTRADA.exists():
    print(f"✗ Arquivo bruto não encontrado: {ENTRADA}")
    print("  Execute primeiro o script 005a_BolsaFamilia_Extrair.py")
    exit()

df = pd.read_csv(ENTRADA, sep=";", dtype=str)
df["QTD_BENEFICIARIOS"] = pd.to_numeric(df["QTD_BENEFICIARIOS"], errors="coerce")
df["ANO"] = pd.to_numeric(df["ANO"], errors="coerce")

print(f"Carregado: {len(df)} registros | Anos: {sorted(df['ANO'].unique())}")

# agrega por município e ano — média e máximo mensal de beneficiários
df_agg = df.groupby(["CO_MUNICIPIO", "ANO"], as_index=False).agg(
    BF_MEDIA_MENSAL=("QTD_BENEFICIARIOS", "mean"),
    BF_MAX_MENSAL  =("QTD_BENEFICIARIOS", "max"),
)
df_agg["BF_MEDIA_MENSAL"] = df_agg["BF_MEDIA_MENSAL"].round(0)
df_agg["BF_MAX_MENSAL"]   = df_agg["BF_MAX_MENSAL"].round(0)

print(f"\nShape final: {df_agg.shape}")
print(f"Anos: {sorted(df_agg['ANO'].unique())}")
print(f"Municípios: {df_agg['CO_MUNICIPIO'].nunique()}")
print(df_agg.head(10).to_string())

df_agg.to_csv(SAIDA, sep=";", index=False, encoding="utf-8-sig")
print(f"\n✓ Salvo em: {SAIDA}")