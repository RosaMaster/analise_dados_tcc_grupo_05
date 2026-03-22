import pandas as pd
from pathlib import Path
from config import UF_COD, PASTA_SAIDA, PASTA_SIOPE

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

ENTRADA = Path(PASTA_SIOPE) / f"siope_bruto_{SIGLA.lower()}.csv"
SAIDA   = Path(PASTA_SIOPE) / f"siope_dados_gerais_{SIGLA.lower()}.csv"
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print(f"SIOPE PREPARAÇÃO — Estado: {SIGLA} (código {UF_COD})")
print("=" * 60)

if not ENTRADA.exists():
    print(f"✗ Arquivo bruto não encontrado: {ENTRADA}")
    print("  Execute primeiro o script 003a_SIOPE_Extrair.py")
    exit()

df = pd.read_csv(ENTRADA, sep=";", low_memory=False)
print(f"Carregado: {len(df)} registros | {len(df.columns)} colunas")

# normaliza coluna de despesa (nome muda entre anos)
if "VL_DESP_PAGA_EDU" in df.columns and "VAL_DESP_PAGA_EDU" not in df.columns:
    df = df.rename(columns={"VL_DESP_PAGA_EDU": "VAL_DESP_PAGA_EDU"})
if "VL_DESP_LIQU_EDU" in df.columns and "VAL_DESP_LIQU_EDU" not in df.columns:
    df = df.rename(columns={"VL_DESP_LIQU_EDU": "VAL_DESP_LIQU_EDU"})

# converte valores
for col in ["VAL_DESP_PAGA_EDU", "VAL_DESP_LIQU_EDU", "NUM_POPU"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# seleciona colunas relevantes
cols_finais = [c for c in ["NUM_ANO", "COD_MUNI", "NOM_MUNI", "NUM_POPU",
                            "VAL_DESP_PAGA_EDU", "VAL_DESP_LIQU_EDU"] if c in df.columns]
df = df[cols_finais]

# renomeia para padronizar com o resto do projeto
df = df.rename(columns={
    "NUM_ANO":           "ANO",
    "COD_MUNI":          "CO_MUNICIPIO",
    "NOM_MUNI":          "NO_MUNICIPIO",
    "NUM_POPU":          "POPULACAO",
    "VAL_DESP_PAGA_EDU": "DESP_EDU_PAGA",
    "VAL_DESP_LIQU_EDU": "DESP_EDU_LIQU",
})

df["CO_MUNICIPIO"] = df["CO_MUNICIPIO"].astype(str)

print(f"\n{'='*50}")
print(f"Total: {len(df)} registros | {df['CO_MUNICIPIO'].nunique()} municípios")
print(f"Anos: {sorted(df['ANO'].unique())}")
print(df.head(5).to_string())

df.to_csv(SAIDA, sep=";", index=False, encoding="utf-8-sig")
print(f"\n✓ Salvo em: {SAIDA}")
