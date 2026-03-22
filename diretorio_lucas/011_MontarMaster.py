
# ETAPA 12 — JOIN + SAEB (proficiência em LP e MT por município)
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Etapa 12: Join + SAEB ──")

if ARQUIVO_SAEB.exists():
    df_saeb = pd.read_csv(ARQUIVO_SAEB, sep=";")
    df_saeb["CO_MUNICIPIO"] = df_saeb["CO_MUNICIPIO"].astype(str)

    cols_saeb = ["SAEB_5_LP", "SAEB_5_MT", "SAEB_9_LP", "SAEB_9_MT", "SAEB_12_LP", "SAEB_12_MT"]
    df = df.drop(columns=cols_saeb, errors="ignore")

    df["CO_MUN_6"]        = df["CO_MUNICIPIO"].str[:6]
    df_saeb["CO_MUN_6"]   = df_saeb["CO_MUNICIPIO"].str[:6]

    df = df.merge(
        df_saeb[["CO_MUN_6", "ANO"] + [c for c in cols_saeb if c in df_saeb.columns]],
        on=["CO_MUN_6", "ANO"],
        how="left"
    )
    df = df.drop(columns=["CO_MUN_6"], errors="ignore")
    print(f"  ✓ {df['SAEB_12_MT'].notna().sum()} registros com SAEB EM Matemática")
else:
    print(f"  ⚠️  Arquivo não encontrado, pulando: {ARQUIVO_SAEB}")
    print(f"     Execute 016a_SAEB_Extrair.py para gerar o arquivo.")

# ══════════════════════════════════════════════════════════════════════════════
# ETAPA 13 — VARIÁVEIS DERIVADAS
# ══════════════════════════════════════════════════════════════════════════════
print("\n── Etapa 13: Calculando variáveis derivadas ──")

df["ALUNO_DOC_FUND"] = (df["QT_MAT_FUND"] / df["QT_DOC_FUND"]).replace([float("inf")], None)
df["ALUNO_DOC_MED"]  = (df["QT_MAT_MED"]  / df["QT_DOC_MED"]).replace([float("inf")], None)
print("  ✓ ALUNO_DOC_FUND e ALUNO_DOC_MED calculados")


# ══════════════════════════════════════════════════════════════════════════════
# RESUMO FINAL
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{'='*60}")
print(f"MASTER FINAL — {SIGLA}")
print(f"{'='*60}")
print(f"Shape:      {df.shape}")
print(f"Anos:       {sorted(df['ANO'].unique())}")
print(f"Municípios: {df['CO_MUNICIPIO'].nunique()}")
print(f"Colunas:    {list(df.columns)}")

print(f"\nCobertura das variáveis principais:")
for col in ["GASTO_ALUNO", "PIB_PERCAPITA", "INSE", "TAXA_ANALFABETISMO",
            "BF_MEDIA_MENSAL", "ABANDONO_MED_TOTAL", "IDEB_MEDIO"]:
    if col in df.columns:
        pct = df[col].notna().sum() / len(df) * 100
        print(f"  {col:<25} {df[col].notna().sum():>4} registros ({pct:.0f}%)")

print(f"\nPrimeiras linhas:")
cols_preview = ["ANO", "NO_MUNICIPIO", "GASTO_ALUNO", "PIB_PERCAPITA",
                "INSE", "ABANDONO_MED_TOTAL", "IDEB_MEDIO"]
cols_preview = [c for c in cols_preview if c in df.columns]
print(df[cols_preview].head(10).to_string())


# ══════════════════════════════════════════════════════════════════════════════
# SALVA
# ══════════════════════════════════════════════════════════════════════════════
df.to_csv(ARQUIVO_MASTER, sep=";", index=False, encoding="utf-8-sig")
print(f"\n✓ Master salvo em: {ARQUIVO_MASTER}")