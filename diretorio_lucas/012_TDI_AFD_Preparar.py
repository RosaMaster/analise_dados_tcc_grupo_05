import pandas as pd
from pathlib import Path
from config import *

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

MASTER    = Path(PASTA_SAIDA) / f"df_master_{SIGLA.lower()}.csv"
ARQ_TDI   = Path(PASTA_TDI_AFD) / f"tdi_municipios_{SIGLA.lower()}.csv"
ARQ_AFD   = Path(PASTA_TDI_AFD) / f"afd_municipios_{SIGLA.lower()}.csv"
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print(f"INTEGRAÇÃO TDI + AFD → MASTER — Estado: {SIGLA}")
print("=" * 60)

if not MASTER.exists():
    print(f"✗ Master não encontrado: {MASTER}")
    exit()

df = pd.read_csv(MASTER, sep=";")
df["CO_MUNICIPIO"] = df["CO_MUNICIPIO"].astype(str)
print(f"Master carregado: {df.shape}")

# ── Integra TDI ───────────────────────────────────────────────────────────────
if ARQ_TDI.exists():
    print("\nIntegrando TDI...")
    df_tdi = pd.read_csv(ARQ_TDI, sep=";")
    df_tdi["CO_MUNICIPIO"] = df_tdi["CO_MUNICIPIO"].astype(str)

    cols_tdi = [c for c in df_tdi.columns if c.startswith("TDI_")]
    df = df.drop(columns=cols_tdi, errors="ignore")

    df = df.merge(
        df_tdi[["CO_MUNICIPIO", "ANO"] + cols_tdi],
        on=["CO_MUNICIPIO", "ANO"],
        how="left"
    )
    print(f"  ✓ TDI_MED_TOTAL preenchido: {df['TDI_MED_TOTAL'].notna().sum()} de {len(df)}")
else:
    print(f"  ⚠️  TDI não encontrado: {ARQ_TDI}")

# ── Integra AFD ───────────────────────────────────────────────────────────────
if ARQ_AFD.exists():
    print("\nIntegrando AFD...")
    df_afd = pd.read_csv(ARQ_AFD, sep=";")
    df_afd["CO_MUNICIPIO"] = df_afd["CO_MUNICIPIO"].astype(str)

    cols_afd = [c for c in df_afd.columns if c.startswith("AFD_")]
    df = df.drop(columns=cols_afd, errors="ignore")

    df = df.merge(
        df_afd[["CO_MUNICIPIO", "ANO"] + cols_afd],
        on=["CO_MUNICIPIO", "ANO"],
        how="left"
    )
    print(f"  ✓ AFD_MED_ADEQUADO preenchido: {df['AFD_MED_ADEQUADO'].notna().sum()} de {len(df)}")
else:
    print(f"  ⚠️  AFD não encontrado: {ARQ_AFD}")

# ── Correlações rápidas ───────────────────────────────────────────────────────
alvo = [c for c in ["ABANDONO_MED_TOTAL", "IDEB_MEDIO"] if c in df.columns]
novas = [c for c in [
    "TDI_FUND_TOTAL", "TDI_MED_TOTAL",
    "AFD_MED_ADEQUADO", "AFD_FUND_ADEQUADO"
] if c in df.columns]

if novas and alvo:
    print(f"\n── Correlação TDI/AFD x abandono e IDEB ──")
    print(df[novas + alvo].corr()[alvo].loc[novas].round(3))

# ── Salva ─────────────────────────────────────────────────────────────────────
df.to_csv(MASTER, sep=";", index=False, encoding="utf-8-sig")
print(f"\n✓ Master atualizado: {MASTER}")
print(f"  Shape final: {df.shape}")