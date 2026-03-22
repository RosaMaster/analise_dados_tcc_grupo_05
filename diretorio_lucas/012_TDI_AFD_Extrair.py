import zipfile
import pandas as pd
import io
from pathlib import Path
from config import UF_COD, PASTA_TDI_AFD, PASTA_DATA

Path(PASTA_TDI_AFD).mkdir(parents=True, exist_ok=True)  # cria a pasta se não existir
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

ANOS = list(range(2019, 2026))

SAIDA_TDI = Path(PASTA_TDI_AFD) / f"tdi_municipios_{SIGLA.lower()}.csv"
SAIDA_AFD = Path(PASTA_TDI_AFD) / f"afd_municipios_{SIGLA.lower()}.csv"
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print(f"TDI + AFD EXTRAÇÃO — Estado: {SIGLA} (código {UF_COD})")
print("=" * 60)


def abrir_xlsx_do_zip(zip_path, header_row):
    """Abre o XLSX dentro do ZIP e retorna DataFrame."""
    with zipfile.ZipFile(zip_path, "r") as z:
        nome_interno = next(n for n in z.namelist() if n.lower().endswith(".xlsx"))
        with z.open(nome_interno) as f:
            return pd.read_excel(
                io.BytesIO(f.read()),
                header=header_row,
                dtype=str,
                engine="openpyxl"
            )


# ══════════════════════════════════════════════════════════════════════════════
# TDI — Taxa de Distorção Idade-série
# ══════════════════════════════════════════════════════════════════════════════
print("\n── TDI — Taxa de Distorção Idade-série ──")

# colunas de interesse TDI
COLUNAS_TDI = {
    "NU_ANO_CENSO": "ANO",
    "CO_MUNICIPIO":  "CO_MUNICIPIO",
    "NO_MUNICIPIO":  "NO_MUNICIPIO",
    "SG_UF":         "SG_UF",
    "FUN_CAT_0":     "TDI_FUND_TOTAL",      # distorção fundamental total
    "FUN_AI_CAT_0":  "TDI_FUND_AI",         # anos iniciais
    "FUN_AF_CAT_0":  "TDI_FUND_AF",         # anos finais
    "MED_CAT_0":     "TDI_MED_TOTAL",       # distorção médio total
    "MED_01_CAT_0":  "TDI_MED_1SERIE",      # 1ª série
    "MED_02_CAT_0":  "TDI_MED_2SERIE",      # 2ª série
    "MED_03_CAT_0":  "TDI_MED_3SERIE",      # 3ª série
}

todos_tdi = []

for ano in ANOS:
    # tenta nome com e sem sufixo " (1)"
    for sufixo in [" (1)", ""]:
        zip_path = Path(PASTA_DATA) / "TDI_AFD" / f"TDI_{ano}_MUNICIPIOS{sufixo}.zip"
        if zip_path.exists():
            break
    else:
        print(f"  [{ano}] ✗ Arquivo não encontrado")
        continue

    print(f"  [{ano}] Carregando...", end=" ", flush=True)
    try:
        df = abrir_xlsx_do_zip(zip_path, header_row=8)

        # filtra estado
        df = df[df["SG_UF"] == SIGLA].copy()

        # filtra Total x Total
        df = df[
            (df["NO_CATEGORIA"].str.strip() == "Total") &
            (df["NO_DEPENDENCIA"].str.strip() == "Total")
        ].copy()

        # seleciona colunas disponíveis
        cols = {k: v for k, v in COLUNAS_TDI.items() if k in df.columns}
        df = df[list(cols.keys())].rename(columns=cols)

        # converte para numérico
        for col in df.columns:
            if col not in ("ANO", "CO_MUNICIPIO", "NO_MUNICIPIO", "SG_UF"):
                df[col] = pd.to_numeric(
                    df[col].astype(str).str.replace(",", ".").str.strip(),
                    errors="coerce"
                )

        df["ANO"] = int(ano)
        todos_tdi.append(df)
        print(f"✓ {len(df)} municípios")

    except Exception as e:
        print(f"✗ Erro: {e}")

if todos_tdi:
    df_tdi = pd.concat(todos_tdi, ignore_index=True)
    df_tdi["CO_MUNICIPIO"] = df_tdi["CO_MUNICIPIO"].astype(str)
    df_tdi.to_csv(SAIDA_TDI, sep=";", index=False, encoding="utf-8-sig")
    print(f"\n✓ TDI salvo: {SAIDA_TDI}")
    print(f"  {len(df_tdi)} registros | Anos: {sorted(df_tdi['ANO'].unique())}")
    print(df_tdi.head(3).to_string())
else:
    print("  ✗ Nenhum dado TDI coletado.")


# ══════════════════════════════════════════════════════════════════════════════
# AFD — Adequação da Formação Docente
# ══════════════════════════════════════════════════════════════════════════════
print("\n── AFD — Adequação da Formação Docente ──")

# grupos do AFD:
# Grupo 1: formação superior na mesma área (adequação plena)
# Grupo 2: formação superior em área diferente
# Grupo 3: formação superior em licenciatura de outras disciplinas
# Grupo 4: formação superior sem licenciatura
# Grupo 5: sem formação superior

COLUNAS_AFD = {
    "NU_ANO_CENSO": "ANO",
    "CO_MUNICIPIO":  "CO_MUNICIPIO",
    "NO_MUNICIPIO":  "NO_MUNICIPIO",
    "SG_UF":         "SG_UF",
    # Ensino Fundamental
    "FUN_CAT_1":     "AFD_FUND_G1",   # formação adequada Fund.
    "FUN_CAT_2":     "AFD_FUND_G2",
    "FUN_CAT_3":     "AFD_FUND_G3",
    "FUN_CAT_4":     "AFD_FUND_G4",
    "FUN_CAT_5":     "AFD_FUND_G5",   # sem superior Fund.
    # Ensino Médio
    "MED_CAT_1":     "AFD_MED_G1",    # formação adequada Médio
    "MED_CAT_2":     "AFD_MED_G2",
    "MED_CAT_3":     "AFD_MED_G3",
    "MED_CAT_4":     "AFD_MED_G4",
    "MED_CAT_5":     "AFD_MED_G5",    # sem superior Médio
}

todos_afd = []

for ano in ANOS:
    zip_path = Path(PASTA_DATA) / "TDI_AFD" / f"AFD_{ano}_MUNICIPIOS.zip"
    if not zip_path.exists():
        print(f"  [{ano}] ✗ Arquivo não encontrado")
        continue

    print(f"  [{ano}] Carregando...", end=" ", flush=True)
    try:
        df = abrir_xlsx_do_zip(zip_path, header_row=10)

        # filtra estado
        df = df[df["SG_UF"] == SIGLA].copy()

        # filtra Total x Total
        df = df[
            (df["NO_CATEGORIA"].str.strip() == "Total") &
            (df["NO_DEPENDENCIA"].str.strip() == "Total")
        ].copy()

        # seleciona colunas disponíveis
        cols = {k: v for k, v in COLUNAS_AFD.items() if k in df.columns}
        df = df[list(cols.keys())].rename(columns=cols)

        # converte para numérico
        for col in df.columns:
            if col not in ("ANO", "CO_MUNICIPIO", "NO_MUNICIPIO", "SG_UF"):
                df[col] = pd.to_numeric(
                    df[col].astype(str).str.replace(",", ".").str.strip(),
                    errors="coerce"
                )

        # variável derivada: proporção com formação adequada (Grupo 1)
        if "AFD_MED_G1" in df.columns:
            df["AFD_MED_ADEQUADO"] = df["AFD_MED_G1"]  # % docentes com formação plena no EM
        if "AFD_FUND_G1" in df.columns:
            df["AFD_FUND_ADEQUADO"] = df["AFD_FUND_G1"]

        df["ANO"] = int(ano)
        todos_afd.append(df)
        print(f"✓ {len(df)} municípios")

    except Exception as e:
        print(f"✗ Erro: {e}")

if todos_afd:
    df_afd = pd.concat(todos_afd, ignore_index=True)
    df_afd["CO_MUNICIPIO"] = df_afd["CO_MUNICIPIO"].astype(str)
    df_afd.to_csv(SAIDA_AFD, sep=";", index=False, encoding="utf-8-sig")
    print(f"\n✓ AFD salvo: {SAIDA_AFD}")
    print(f"  {len(df_afd)} registros | Anos: {sorted(df_afd['ANO'].unique())}")
    print(df_afd.head(3).to_string())
else:
    print("  ✗ Nenhum dado AFD coletado.")