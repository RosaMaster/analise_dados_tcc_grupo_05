import pandas as pd
import os
from pathlib import Path
from config import UF_COD, PASTA_SAIDA, PASTA_DATA, PASTA_BOLSA_FAMILIA

Path(PASTA_BOLSA_FAMILIA).mkdir(parents=True, exist_ok=True)  # cria a pasta se não existir
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
PREFIXO_UF = str(UF_COD).zfill(2)  # ex: "35" para SP, "23" para CE

ANOS        = [2019, 2020, 2021, 2023, 2024, 2025]
SAIDA_BRUTO = Path(PASTA_BOLSA_FAMILIA) / f"bolsa_familia_bruto_{SIGLA.lower()}.csv"
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print(f"BOLSA FAMÍLIA EXTRAÇÃO — Estado: {SIGLA} (código {UF_COD})")
print("=" * 60)

todos = []

for ano in ANOS:
    arquivo = Path(PASTA_DATA) / "Bolsa_Familia" / f"BolsaFamilia{ano}.csv"

    if not arquivo.exists():
        print(f"[{ano}] Arquivo não encontrado: {arquivo}")
        continue

    print(f"[{ano}] Carregando...", end=" ", flush=True)

    try:
        # detecta separador
        with open(arquivo, "r", encoding="utf-8") as f:
            primeira = f.readline()
        sep = ";" if ";" in primeira else ","

        df_ano = pd.read_csv(arquivo, sep=sep, dtype=str, encoding="utf-8")
        df_ano.columns = df_ano.columns.str.strip().str.lower()

        # padroniza coluna de código do município
        col_ibge = next((c for c in df_ano.columns if "ibge" in c or "codigo" in c), None)
        if col_ibge is None:
            print(f"✗ Coluna de código não encontrada")
            continue

        df_ano = df_ano.rename(columns={col_ibge: "CO_MUNICIPIO"})
        df_ano["CO_MUNICIPIO"] = df_ano["CO_MUNICIPIO"].astype(str).str.strip().str.zfill(6)

        # filtra estado pelo prefixo do código IBGE
        df_uf = df_ano[df_ano["CO_MUNICIPIO"].str.startswith(PREFIXO_UF)].copy()

        # padroniza coluna de beneficiários
        col_bf = next((c for c in df_uf.columns
                       if c in ("qtd_ben_bf", "qtd_ben_bas", "beneficiarios", "qtd_ben_brc")), None)
        if col_bf is None:
            col_bf = next((c for c in df_uf.columns if "ben" in c), None)
        if col_bf is None:
            print(f"✗ Coluna de beneficiários não encontrada. Colunas: {list(df_uf.columns)}")
            continue

        df_uf = df_uf.rename(columns={col_bf: "QTD_BENEFICIARIOS"})

        # padroniza coluna de período
        col_periodo = next((c for c in df_uf.columns if "anomes" in c or "periodo" in c), None)
        if col_periodo:
            df_uf = df_uf.rename(columns={col_periodo: "ANOMES"})

        df_uf["ANO"] = ano
        df_uf["QTD_BENEFICIARIOS"] = pd.to_numeric(df_uf["QTD_BENEFICIARIOS"], errors="coerce")

        cols = [c for c in ["CO_MUNICIPIO", "ANOMES", "ANO", "QTD_BENEFICIARIOS"] if c in df_uf.columns]
        todos.append(df_uf[cols])
        print(f"✓ {len(df_uf)} registros {SIGLA}")

    except Exception as e:
        print(f"✗ Erro: {e}")

if not todos:
    print("Nenhum dado coletado.")
else:
    df_bruto = pd.concat(todos, ignore_index=True)
    df_bruto.to_csv(SAIDA_BRUTO, sep=";", index=False, encoding="utf-8-sig")
    print(f"\n✓ Dados brutos salvos em: {SAIDA_BRUTO}")
    print(f"  {len(df_bruto)} registros | Anos: {sorted(df_bruto['ANO'].unique())}")
    print("\nExecute o script de preparação para gerar o arquivo final agregado.")