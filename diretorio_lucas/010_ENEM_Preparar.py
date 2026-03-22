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

ENTRADA = Path(PASTA_ENEM) / f"enem_bruto_{SIGLA.lower()}.csv"
SAIDA   = Path(PASTA_ENEM) / f"enem_municipios_{SIGLA.lower()}.csv"
MASTER  = Path(PASTA_SAIDA) / f"df_master_{SIGLA.lower()}.csv"
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print(f"ENEM PREPARAÇÃO — Estado: {SIGLA} (código {UF_COD})")
print("=" * 60)

if not ENTRADA.exists():
    print(f"✗ Arquivo bruto não encontrado: {ENTRADA}")
    print("  Execute primeiro o script enem_extrair.py")
    exit()

print(f"Carregando {ENTRADA.name}...")
df = pd.read_csv(ENTRADA, sep=";", low_memory=False)
print(f"  {len(df):,} participantes | Anos: {sorted(df['ANO'].unique())}")

# ─── CONVERTE NOTAS PARA NUMÉRICO ─────────────────────────────────────────────
notas = ["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]
for col in notas:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# nota geral = média das 5 áreas (ponderação igual)
df["ENEM_MEDIA_GERAL"] = df[notas].mean(axis=1)

# ─── FILTRA REDE PÚBLICA SE DESEJADO ──────────────────────────────────────────
# mantém estadual (2) e municipal (3) para compatibilidade com o master
# comenta as linhas abaixo se quiser incluir todas as redes
if "TP_DEPENDENCIA_ADM_ESC" in df.columns:
    df_pub = df[df["TP_DEPENDENCIA_ADM_ESC"].isin([2, 3])].copy()
    print(f"  {len(df_pub):,} participantes de escolas públicas (estadual + municipal)")
else:
    df_pub = df.copy()

# ─── AGREGA POR MUNICÍPIO E ANO ───────────────────────────────────────────────
print("\nAgregando por município e ano...")

agg = df_pub.groupby(["CO_MUNICIPIO_ESC", "ANO"], as_index=False).agg(
    NO_MUNICIPIO        =("NO_MUNICIPIO_ESC",   "first"),
    ENEM_PARTICIPANTES  =("ENEM_MEDIA_GERAL",   "count"),
    ENEM_MEDIA_CN       =("NU_NOTA_CN",         "mean"),
    ENEM_MEDIA_CH       =("NU_NOTA_CH",         "mean"),
    ENEM_MEDIA_LC       =("NU_NOTA_LC",         "mean"),
    ENEM_MEDIA_MT       =("NU_NOTA_MT",         "mean"),
    ENEM_MEDIA_REDACAO  =("NU_NOTA_REDACAO",    "mean"),
    ENEM_MEDIA_GERAL    =("ENEM_MEDIA_GERAL",   "mean"),
)

# arredonda notas
cols_notas = ["ENEM_MEDIA_CN", "ENEM_MEDIA_CH", "ENEM_MEDIA_LC",
              "ENEM_MEDIA_MT", "ENEM_MEDIA_REDACAO", "ENEM_MEDIA_GERAL"]
for col in cols_notas:
    agg[col] = agg[col].round(2)

agg = agg.rename(columns={"CO_MUNICIPIO_ESC": "CO_MUNICIPIO"})
agg["CO_MUNICIPIO"] = agg["CO_MUNICIPIO"].astype(str)

print(f"  {len(agg):,} registros | {agg['CO_MUNICIPIO'].nunique()} municípios")
print(f"  Anos: {sorted(agg['ANO'].unique())}")
print(f"\nEstatísticas da média geral:")
print(agg["ENEM_MEDIA_GERAL"].describe().round(2))
print(f"\nPrimeiras linhas:")
print(agg[["CO_MUNICIPIO", "NO_MUNICIPIO", "ANO", "ENEM_PARTICIPANTES",
           "ENEM_MEDIA_GERAL", "ENEM_MEDIA_MT"]].head(10).to_string())

agg.to_csv(SAIDA, sep=";", index=False, encoding="utf-8-sig")
print(f"\n✓ Salvo em: {SAIDA}")

# ─── INTEGRA AO MASTER ────────────────────────────────────────────────────────
if not MASTER.exists():
    print(f"\n⚠️  Master não encontrado: {MASTER}")
    print("   Execute o montar_master.py antes de integrar.")
    exit()

print(f"\nIntegrando ao master...")
df_master = pd.read_csv(MASTER, sep=";")
df_master["CO_MUNICIPIO"] = df_master["CO_MUNICIPIO"].astype(str)

# remove colunas antigas do ENEM se existirem
cols_enem = ["ENEM_PARTICIPANTES", "ENEM_MEDIA_CN", "ENEM_MEDIA_CH",
             "ENEM_MEDIA_LC", "ENEM_MEDIA_MT", "ENEM_MEDIA_REDACAO", "ENEM_MEDIA_GERAL"]
df_master = df_master.drop(columns=cols_enem, errors="ignore")

# chave de 6 dígitos para join
df_master["CO_MUN_6"] = df_master["CO_MUNICIPIO"].str[:6]
agg["CO_MUN_6"]       = agg["CO_MUNICIPIO"].str[:6]

df = df_master.merge(
    agg[["CO_MUN_6", "ANO"] + [c for c in cols_enem if c in agg.columns]],
    on=["CO_MUN_6", "ANO"],
    how="left"
)
df = df.drop(columns=["CO_MUN_6"], errors="ignore")

print(f"Registros com ENEM: {df['ENEM_MEDIA_GERAL'].notna().sum()} de {len(df)}")

# correlação rápida
cols_alvo = [c for c in ["ABANDONO_MED_TOTAL", "IDEB_MEDIO"] if c in df.columns]
if cols_alvo:
    print(f"\n── Correlação ENEM x abandono e IDEB ──")
    cols_enem_disp = [c for c in cols_enem if c in df.columns and c != "ENEM_PARTICIPANTES"]
    print(df[cols_enem_disp + cols_alvo].corr()[cols_alvo].loc[cols_enem_disp].round(3))

df.to_csv(MASTER, sep=";", index=False, encoding="utf-8-sig")
print(f"\n✓ Master atualizado salvo em: {MASTER}")