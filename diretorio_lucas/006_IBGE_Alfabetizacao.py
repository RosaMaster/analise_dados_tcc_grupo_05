import pandas as pd
from pathlib import Path
from config import UF_COD, PASTA_IBGE_ALFABETIZACAO, PASTA_DATA

Path(PASTA_IBGE_ALFABETIZACAO).mkdir(parents=True, exist_ok=True)  # cria a pasta se não existir
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

ARQUIVO = Path(PASTA_DATA) / "IBGE_Alfabetizacao" / "Agregados_por_municipios_alfabetizacao_BR.xlsx"
SAIDA   = Path(PASTA_IBGE_ALFABETIZACAO) / f"ibge_socioeconomico_{SIGLA.lower()}.csv"
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print(f"IBGE ALFABETIZAÇÃO — Estado: {SIGLA} (código {UF_COD})")
print("=" * 60)

if not ARQUIVO.exists():
    print(f"✗ Arquivo não encontrado: {ARQUIVO}")
    exit()

print("Carregando arquivo de alfabetização...")
df = pd.read_excel(ARQUIVO, dtype=str)

# filtra estado pelo prefixo do código IBGE
df = df[df["CD_MUN"].astype(str).str.startswith(PREFIXO_UF)].copy()
print(f"Municípios {SIGLA}: {len(df)}")

# seleciona colunas de interesse
COLUNAS = {
    "CD_MUN":  "CO_MUNICIPIO",
    "NM_MUN":  "NO_MUNICIPIO_IBGE",
    "V00900":  "ALFABETIZADOS_15MAIS",   # sabe ler e escrever, 15+
    "V00901":  "ANALFABETOS_15MAIS",     # não sabe ler e escrever, 15+
    "V01006":  "TOTAL_MORADORES",        # total de moradores
    "V01194":  "DOM_MONOPARENTAL",       # domicílios responsável sem cônjuge com filhos
    "V01063":  "RESP_FEMININO",          # responsável feminino
    "V01042":  "TOTAL_RESPONSAVEIS",     # total de responsáveis (= total domicílios)
}

cols_presentes = {k: v for k, v in COLUNAS.items() if k in df.columns}
cols_faltando  = [k for k in COLUNAS if k not in df.columns]
if cols_faltando:
    print(f"Colunas ausentes: {cols_faltando}")

df = df[list(cols_presentes.keys())].rename(columns=cols_presentes)

# converte para numérico
for col in df.columns:
    if col not in ("CO_MUNICIPIO", "NO_MUNICIPIO_IBGE"):
        df[col] = pd.to_numeric(df[col], errors="coerce")

# calcula indicadores derivados
df["TAXA_ANALFABETISMO"] = (
    df["ANALFABETOS_15MAIS"] / (df["ALFABETIZADOS_15MAIS"] + df["ANALFABETOS_15MAIS"])
).round(4)

if "DOM_MONOPARENTAL" in df.columns and "TOTAL_RESPONSAVEIS" in df.columns:
    df["PROP_MONOPARENTAL"] = (df["DOM_MONOPARENTAL"] / df["TOTAL_RESPONSAVEIS"]).round(4)

if "RESP_FEMININO" in df.columns and "TOTAL_RESPONSAVEIS" in df.columns:
    df["PROP_RESP_FEMININO"] = (df["RESP_FEMININO"] / df["TOTAL_RESPONSAVEIS"]).round(4)

df["CO_MUNICIPIO"] = df["CO_MUNICIPIO"].astype(str)

# estatísticas
print(f"\nShape: {df.shape}")
cols_stat = ["TAXA_ANALFABETISMO"] + \
            [c for c in ["PROP_MONOPARENTAL", "PROP_RESP_FEMININO"] if c in df.columns]
print(f"\nEstatísticas:")
print(df[cols_stat].describe().round(4))

cols_view = ["CO_MUNICIPIO", "NO_MUNICIPIO_IBGE", "TAXA_ANALFABETISMO"] + \
            [c for c in ["PROP_MONOPARENTAL", "PROP_RESP_FEMININO"] if c in df.columns]
print(f"\nPrimeiras linhas:")
print(df[cols_view].head(10).to_string())

df.to_csv(SAIDA, sep=";", index=False, encoding="utf-8-sig")
print(f"\n✓ Salvo em: {SAIDA}")