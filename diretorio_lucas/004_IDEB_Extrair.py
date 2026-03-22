import pandas as pd
from pathlib import Path
from config import UF_COD, PASTA_SAIDA, PASTA_DATA, PASTA_IDEB

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

SAIDA_BRUTO = Path(PASTA_IDEB) / f"ideb_bruto_{SIGLA.lower()}.csv"
Path(PASTA_IDEB).mkdir(parents=True, exist_ok=True)  # cria a pasta se não existir

# os três arquivos XLSX do INEP — um por nível de ensino
ARQUIVOS = {
    "FUND_AI": Path(PASTA_DATA) / "IDEB" / "divulgacao_anos_iniciais_municipios_2023.xlsx",
    "FUND_AF": Path(PASTA_DATA) / "IDEB" / "divulgacao_anos_finais_municipios_2023.xlsx",
    "MEDIO":   Path(PASTA_DATA) / "IDEB" / "divulgacao_ensino_medio_municipios_2023.xlsx",
}
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print(f"IDEB EXTRAÇÃO — Estado: {SIGLA} (código {UF_COD})")
print("=" * 60)

todos = []

for nivel, arquivo in ARQUIVOS.items():
    if not arquivo.exists():
        print(f"\n  ✗ Arquivo não encontrado: {arquivo}")
        continue

    print(f"\n  Carregando {arquivo.name} ({nivel})...")
    df = pd.read_excel(arquivo, header=9, dtype=str)

    # filtra estado e rede pública
    df = df[df["SG_UF"] == SIGLA].copy()
    df = df[df["REDE"].str.strip() == "Pública"].copy()

    cols_id   = ["CO_MUNICIPIO", "NO_MUNICIPIO"]
    cols_ideb = [f"VL_OBSERVADO_{ano}" for ano in ANOS if f"VL_OBSERVADO_{ano}" in df.columns]

    anos_faltando = [ano for ano in ANOS if f"VL_OBSERVADO_{ano}" not in df.columns]
    if anos_faltando:
        print(f"    ⚠️  Anos ausentes: {anos_faltando}")

    df = df[cols_id + cols_ideb].copy()
    df["NIVEL"] = nivel

    todos.append(df)
    print(f"    ✓ {df['CO_MUNICIPIO'].nunique()} municípios")

if todos:
    df_bruto = pd.concat(todos, ignore_index=True)
    df_bruto.to_csv(SAIDA_BRUTO, sep=";", index=False, encoding="utf-8-sig")
    print(f"\n✓ Dados brutos salvos em: {SAIDA_BRUTO}")
    print(f"  {len(df_bruto)} registros | níveis: {df_bruto['NIVEL'].unique().tolist()}")
    print("\nExecute o script de preparação para gerar o arquivo final.")
else:
    print("\n✗ Nenhum dado extraído.")