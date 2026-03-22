import pandas as pd
from pathlib import Path
from config import UF_COD, PASTA_SAEB, PASTA_DATA

Path(PASTA_SAEB).mkdir(parents=True, exist_ok=True)  # cria a pasta se não existir
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

SAIDA_SAEB = Path(PASTA_SAEB) / f"saeb_municipios_{SIGLA.lower()}.csv"

ARQUIVOS = {
    2019: {
        "arquivo": "Resultados_Saeb_2019_Brasil_Estados_Municipios.xlsx",
        "engine":  "openpyxl",
        "sheet":   "Municípios",
    },
    2021: {
        "arquivo": "saeb_2021_brasil_estados_municipios.xlsx",
        "engine":  "openpyxl",
        "sheet":   "Municípios",
    },
    2023: {
        "arquivo": "Resultados_Saeb_2023_Brasil_Estados_Municipios.xlsb",
        "engine":  "pyxlsb",
        "sheet":   "Municípios",
    },
}

COLUNAS = [
    "CO_MUNICIPIO",
    "MEDIA_5_LP",   # 5º ano LP
    "MEDIA_5_MT",   # 5º ano MT
    "MEDIA_9_LP",   # 9º ano LP
    "MEDIA_9_MT",   # 9º ano MT
    "MEDIA_12_LP",  # 3ª série EM LP
    "MEDIA_12_MT",  # 3ª série EM MT
]
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print(f"SAEB EXTRAÇÃO — Estado: {SIGLA} (código {UF_COD})")
print("=" * 60)

todos = []

for ano, cfg in ARQUIVOS.items():
    arquivo = Path(PASTA_DATA) / "Saeb" / cfg["arquivo"]

    if not arquivo.exists():
        print(f"[{ano}] ✗ Arquivo não encontrado: {arquivo}")
        continue

    print(f"[{ano}] Carregando...")

    try:
        df = pd.read_excel(
            arquivo,
            sheet_name=cfg["sheet"],
            engine=cfg["engine"],
            dtype=str
        )

        if "ANO_SAEB" not in df.columns:
            df["ANO_SAEB"] = str(ano)

        df["CO_MUNICIPIO"] = df["CO_MUNICIPIO"].astype(str).str.strip().str.split(".").str[0]
        df["CO_UF"]        = pd.to_numeric(df["CO_UF"], errors="coerce")

        # filtra estado dinamicamente
        df = df[df["CO_UF"] == UF_COD].copy()

        # filtra Total de localização
        df = df[df["LOCALIZACAO"].str.strip() == "Total"].copy()

        # filtra dependência — prioriza Total, aceita Estadual
        dep = df["DEPENDENCIA_ADM"].str.strip()
        df = df[
            dep.str.contains("Total", case=False, na=False) |
            dep.str.contains("Estadual", case=False, na=False)
        ].copy()

        # se sobrar mais de uma linha por município, pega a "Total"
        df["_dep_rank"] = df["DEPENDENCIA_ADM"].apply(
            lambda x: 0 if "Total" in str(x) else 1
        )
        df = df.sort_values("_dep_rank").drop_duplicates("CO_MUNICIPIO").drop(columns="_dep_rank")

        cols = ["CO_MUNICIPIO"] + [c for c in COLUNAS[1:] if c in df.columns]
        df = df[cols].copy()

        for c in cols[1:]:
            df[c] = pd.to_numeric(
                df[c].astype(str).str.replace(",", ".").str.strip(), errors="coerce"
            )

        df["ANO"] = ano
        todos.append(df)
        print(f"  ✓ {len(df)} municípios")

    except Exception as e:
        print(f"  ✗ Erro: {e}")

if not todos:
    print("Nenhum dado carregado.")
    exit()

df_saeb = pd.concat(todos, ignore_index=True)

# renomeia para padronizar no master
df_saeb = df_saeb.rename(columns={
    "MEDIA_5_LP":  "SAEB_5_LP",
    "MEDIA_5_MT":  "SAEB_5_MT",
    "MEDIA_9_LP":  "SAEB_9_LP",
    "MEDIA_9_MT":  "SAEB_9_MT",
    "MEDIA_12_LP": "SAEB_12_LP",
    "MEDIA_12_MT": "SAEB_12_MT",
})

print(f"\nSAEB total: {len(df_saeb)} registros | Anos: {sorted(df_saeb['ANO'].unique())}")
print(df_saeb.head(5).to_string())

df_saeb.to_csv(SAIDA_SAEB, sep=";", index=False, encoding="utf-8-sig")
print(f"\n✓ Salvo em: {SAIDA_SAEB}")
print("Execute o montar_master.py para integrar ao master.")