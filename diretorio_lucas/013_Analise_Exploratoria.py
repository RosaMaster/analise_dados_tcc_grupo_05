import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
import os
warnings.filterwarnings("ignore")

from pathlib import Path
from config import UF_COD, PASTA_SAIDA

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

MASTER     = Path(PASTA_SAIDA) / f"df_master_{SIGLA.lower()}.csv"
PASTA_GRAF = Path(PASTA_SAIDA).parent / "graficos"
os.makedirs(PASTA_GRAF, exist_ok=True)
# ─────────────────────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════════
# ESTILO GRÁFICO — PUBLICAÇÃO CIENTÍFICA
# ══════════════════════════════════════════════════════════════════════════════
plt.rcParams.update({
    "font.family":        "DejaVu Sans",
    "font.size":          11,
    "axes.titlesize":     13,
    "axes.titleweight":   "bold",
    "axes.labelsize":     11,
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "axes.grid":          True,
    "grid.alpha":         0.3,
    "grid.linestyle":     "--",
    "xtick.labelsize":    10,
    "ytick.labelsize":    10,
    "legend.fontsize":    10,
    "legend.framealpha":  0.8,
    "figure.dpi":         150,
    "savefig.dpi":        300,
    "savefig.bbox":       "tight",
    "savefig.facecolor":  "white",
})

PALETTE     = ["#2166ac", "#d6604d", "#4dac26", "#f4a582", "#762a83", "#1b7837"]
CMAP_DIV    = "RdBu_r"
CMAP_SEQ    = "Blues"

def salvar(nome):
    path = PASTA_GRAF / f"{nome}_{SIGLA.lower()}.png"
    plt.savefig(path)
    plt.close()
    print(f"  ✓ Salvo: {path.name}")

def subtitulo(texto):
    plt.figtext(0.5, -0.02, texto, ha="center", fontsize=9,
                color="gray", style="italic")

# ══════════════════════════════════════════════════════════════════════════════
# CARREGA E PREPARA
# ══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print(f"ANÁLISE EXPLORATÓRIA COMPLETA — {SIGLA}")
print("=" * 60)

if not MASTER.exists():
    print(f"✗ Master não encontrado: {MASTER}")
    exit()

df = pd.read_csv(MASTER, sep=";")

# limpa colunas duplicadas de população
for col in ["POPULACAO_x", "POPULACAO_y"]:
    if "POPULACAO_x" in df.columns and "POPULACAO_y" in df.columns:
        df["POPULACAO"] = df["POPULACAO_x"].fillna(df["POPULACAO_y"])
        df = df.drop(columns=["POPULACAO_x", "POPULACAO_y"])
        break
    elif col in df.columns:
        df = df.rename(columns={col: "POPULACAO"})
        break

print(f"Shape: {df.shape} | Municípios: {df['CO_MUNICIPIO'].nunique()} | Anos: {sorted(df['ANO'].unique())}")
print(f"Colunas: {list(df.columns)}\n")

# remove outliers de gasto por aluno (percentil 99)
if "GASTO_ALUNO" in df.columns:
    p99 = df["GASTO_ALUNO"].quantile(0.99)
    df_limpo = df[df["GASTO_ALUNO"] <= p99].copy()
else:
    df_limpo = df.copy()

INFRA = [c for c in [
    "IN_BIBLIOTECA", "IN_LABORATORIO_INFORMATICA", "IN_INTERNET",
    "IN_QUADRA_ESPORTES", "IN_REFEITORIO", "IN_AGUA_POTAVEL",
    "IN_ESGOTO_REDE_PUBLICA"
] if c in df.columns]

INFRA_LABELS = {
    "IN_BIBLIOTECA":              "Biblioteca",
    "IN_LABORATORIO_INFORMATICA": "Lab. informática",
    "IN_INTERNET":                "Internet",
    "IN_QUADRA_ESPORTES":         "Quadra esportiva",
    "IN_REFEITORIO":              "Refeitório",
    "IN_AGUA_POTAVEL":            "Água potável",
    "IN_ESGOTO_REDE_PUBLICA":     "Esgoto rede pública",
}

VARS_SOCIO = [c for c in [
    "GASTO_ALUNO", "PIB_PERCAPITA", "RENDA_PERCAPITA",
    "INSE", "TAXA_ANALFABETISMO", "BF_MEDIA_MENSAL", "BF_POR_ALUNO",
    "ALUNO_DOC_MED", "ALUNO_DOC_FUND",
    "TDI_MED_TOTAL", "TDI_FUND_TOTAL",
    "AFD_MED_ADEQUADO", "AFD_FUND_ADEQUADO"
] if c in df.columns]

VARS_DESEMPENHO = [c for c in [
    "IDEB_FUND_AI", "IDEB_FUND_AF", "IDEB_MEDIO",
    "SAEB_5_LP", "SAEB_5_MT", "SAEB_9_LP", "SAEB_9_MT",
    "SAEB_12_LP", "SAEB_12_MT",
    "ENEM_MEDIA_GERAL", "ENEM_MEDIA_MT", "ENEM_MEDIA_CN",
    "ENEM_MEDIA_CH", "ENEM_MEDIA_LC", "ENEM_MEDIA_REDACAO",
] if c in df.columns]

VARS_ABANDONO = [c for c in [
    "ABANDONO_FUND_TOTAL", "ABANDONO_FUND_ANOS_INICIAIS",
    "ABANDONO_FUND_ANOS_FINAIS", "ABANDONO_MED_TOTAL",
    "ABANDONO_MED_1SERIE", "ABANDONO_MED_2SERIE", "ABANDONO_MED_3SERIE",
] if c in df.columns]

LABELS = {
    "ABANDONO_FUND_TOTAL":         "Abandono Fund. Total",
    "ABANDONO_FUND_ANOS_INICIAIS": "Abandono Fund. AI",
    "ABANDONO_FUND_ANOS_FINAIS":   "Abandono Fund. AF",
    "ABANDONO_MED_TOTAL":          "Abandono Médio Total",
    "ABANDONO_MED_1SERIE":         "Abandono Médio 1ª série",
    "ABANDONO_MED_2SERIE":         "Abandono Médio 2ª série",
    "ABANDONO_MED_3SERIE":         "Abandono Médio 3ª série",
    "IDEB_FUND_AI":                "IDEB Fund. AI",
    "IDEB_FUND_AF":                "IDEB Fund. AF",
    "IDEB_MEDIO":                  "IDEB Médio",
    "SAEB_5_LP":                   "SAEB 5º LP",
    "SAEB_5_MT":                   "SAEB 5º MT",
    "SAEB_9_LP":                   "SAEB 9º LP",
    "SAEB_9_MT":                   "SAEB 9º MT",
    "SAEB_12_LP":                  "SAEB EM LP",
    "SAEB_12_MT":                  "SAEB EM MT",
    "ENEM_MEDIA_GERAL":            "ENEM Média Geral",
    "ENEM_MEDIA_MT":               "ENEM Matemática",
    "ENEM_MEDIA_CN":               "ENEM Ciências Nat.",
    "ENEM_MEDIA_CH":               "ENEM Ciências Hum.",
    "ENEM_MEDIA_LC":               "ENEM Linguagens",
    "ENEM_MEDIA_REDACAO":          "ENEM Redação",
    "GASTO_ALUNO":                 "Gasto por aluno (R$)",
    "PIB_PERCAPITA":               "PIB per capita (R$)",
    "RENDA_PERCAPITA":             "Renda per capita (R$)",
    "INSE":                        "INSE",
    "TAXA_ANALFABETISMO":          "Taxa analfabetismo",
    "BF_MEDIA_MENSAL":             "BF — média mensal",
    "BF_POR_ALUNO":                "BF por aluno",
    "ALUNO_DOC_MED":               "Alunos/docente (Médio)",
    "ALUNO_DOC_FUND":              "Alunos/docente (Fund.)",
}

def label(col):
    return LABELS.get(col, col)


# ══════════════════════════════════════════════════════════════════════════════
# BLOCO A — ABANDONO ESCOLAR
# ══════════════════════════════════════════════════════════════════════════════

# ── A1. Evolução temporal do abandono ────────────────────────────────────────
print("\n── A1. Evolução temporal do abandono ──")
cols_ab = [c for c in ["ABANDONO_FUND_TOTAL", "ABANDONO_MED_TOTAL"] if c in df.columns]
if cols_ab:
    ab_ano = df.groupby("ANO")[cols_ab].mean()
    print(ab_ano.round(3))

    fig, ax = plt.subplots(figsize=(9, 5))
    for i, col in enumerate(cols_ab):
        ax.plot(ab_ano.index, ab_ano[col], marker="o", color=PALETTE[i],
                linewidth=2, markersize=6, label=label(col))
    ax.set_title(f"Evolução da taxa média de abandono escolar — {SIGLA}")
    ax.set_ylabel("Taxa média de abandono (%)")
    ax.set_xlabel("Ano")
    ax.legend()
    subtitulo("Fonte: INEP — Taxas de Rendimento Escolar. Escolas estaduais e municipais, zona urbana.")
    salvar("A1_abandono_evolucao")

# ── A2. Abandono por série do Ensino Médio ───────────────────────────────────
print("\n── A2. Abandono por série do Ensino Médio ──")
cols_series = [c for c in ["ABANDONO_MED_1SERIE", "ABANDONO_MED_2SERIE",
                            "ABANDONO_MED_3SERIE"] if c in df.columns]
if cols_series:
    ab_serie = df.groupby("ANO")[cols_series].mean()
    print(ab_serie.round(3))

    fig, ax = plt.subplots(figsize=(9, 5))
    for i, col in enumerate(cols_series):
        ax.plot(ab_serie.index, ab_serie[col], marker="o", color=PALETTE[i],
                linewidth=2, markersize=6, label=label(col))
    ax.set_title(f"Abandono no Ensino Médio por série — {SIGLA}")
    ax.set_ylabel("Taxa média de abandono (%)")
    ax.set_xlabel("Ano")
    ax.legend()
    subtitulo("Fonte: INEP — Taxas de Rendimento Escolar.")
    salvar("A2_abandono_por_serie")

# ── A3. Top 10 municípios — maior abandono médio ─────────────────────────────
print("\n── A3. Top 10 municípios — maior abandono médio ──")
if "ABANDONO_MED_TOTAL" in df.columns:
    top10 = (df.groupby("NO_MUNICIPIO")["ABANDONO_MED_TOTAL"]
               .mean().sort_values(ascending=False).head(10))
    print(top10.round(2))

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(range(len(top10)), top10.sort_values().values,
                   color=PALETTE[1], edgecolor="white", linewidth=0.5)
    ax.set_yticks(range(len(top10)))
    ax.set_yticklabels(top10.sort_values().index, fontsize=10)
    ax.set_xlabel("Taxa média de abandono (%)")
    ax.set_title(f"Top 10 — maior abandono no Ensino Médio — {SIGLA}")
    for bar in bars:
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                f"{bar.get_width():.2f}%", va="center", fontsize=9)
    subtitulo("Média do período disponível. Fonte: INEP — Taxas de Rendimento Escolar.")
    salvar("A3_top10_abandono_medio")

# ── A4. Abandono por porte do município ──────────────────────────────────────
print("\n── A4. Abandono por porte ──")
if "QT_MAT_BAS" in df.columns and "ABANDONO_MED_TOTAL" in df.columns:
    df["PORTE"] = pd.cut(
        df["QT_MAT_BAS"],
        bins=[0, 500, 2000, 10000, float("inf")],
        labels=["Pequeno\n<500", "Médio\n500–2k", "Grande\n2k–10k", "Muito Grande\n>10k"]
    )
    porte = df.groupby("PORTE", observed=True)[
        [c for c in ["ABANDONO_FUND_TOTAL", "ABANDONO_MED_TOTAL"] if c in df.columns]
    ].mean()
    print(porte.round(3))

    x = np.arange(len(porte))
    width = 0.35
    fig, ax = plt.subplots(figsize=(9, 5))
    cols_p = porte.columns.tolist()
    for i, col in enumerate(cols_p):
        ax.bar(x + i*width, porte[col], width, label=label(col),
               color=PALETTE[i], edgecolor="white")
    ax.set_xticks(x + width/2)
    ax.set_xticklabels(porte.index, fontsize=10)
    ax.set_ylabel("Taxa média de abandono (%)")
    ax.set_title(f"Taxa de abandono por porte do município — {SIGLA}")
    ax.legend()
    subtitulo("Porte definido pelo número de matrículas na educação básica.")
    salvar("A4_abandono_por_porte")


# ══════════════════════════════════════════════════════════════════════════════
# BLOCO B — DESEMPENHO (IDEB, SAEB, ENEM)
# ══════════════════════════════════════════════════════════════════════════════

# ── B1. Evolução do IDEB ─────────────────────────────────────────────────────
print("\n── B1. Evolução do IDEB ──")
cols_ideb = [c for c in ["IDEB_FUND_AI", "IDEB_FUND_AF", "IDEB_MEDIO"] if c in df.columns]
if cols_ideb:
    ideb_ano = df.dropna(subset=cols_ideb[:1]).groupby("ANO")[cols_ideb].mean()
    print(ideb_ano.round(3))

    fig, ax = plt.subplots(figsize=(9, 5))
    for i, col in enumerate(cols_ideb):
        ax.plot(ideb_ano.index, ideb_ano[col], marker="o", color=PALETTE[i],
                linewidth=2, markersize=6, label=label(col))
    ax.set_title(f"Evolução média do IDEB — municípios do {SIGLA}")
    ax.set_ylabel("IDEB médio")
    ax.set_xlabel("Ano")
    ax.legend()
    subtitulo("Fonte: INEP — IDEB. Rede pública. Disponível para 2019, 2021 e 2023.")
    salvar("B1_ideb_evolucao")

# ── B2. Top 10 municípios que mais melhoraram no IDEB Médio ──────────────────
print("\n── B2. Municípios com maior melhora no IDEB Médio ──")
if "IDEB_MEDIO" in df.columns:
    df19 = df[df["ANO"] == 2019][["CO_MUNICIPIO", "NO_MUNICIPIO", "IDEB_MEDIO"]]
    df23 = df[df["ANO"] == 2023][["CO_MUNICIPIO", "IDEB_MEDIO"]]
    evolucao = df19.merge(df23, on="CO_MUNICIPIO", suffixes=("_2019", "_2023"))
    evolucao["VARIACAO"] = evolucao["IDEB_MEDIO_2023"] - evolucao["IDEB_MEDIO_2019"]
    evolucao = evolucao.dropna(subset=["VARIACAO"])
    top10m = evolucao.nlargest(10, "VARIACAO")
    print(top10m[["NO_MUNICIPIO", "IDEB_MEDIO_2019", "IDEB_MEDIO_2023", "VARIACAO"]].round(2).to_string(index=False))

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(range(len(top10m)), top10m.sort_values("VARIACAO")["VARIACAO"].values,
            color=PALETTE[2], edgecolor="white")
    ax.set_yticks(range(len(top10m)))
    ax.set_yticklabels(top10m.sort_values("VARIACAO")["NO_MUNICIPIO"].values, fontsize=10)
    ax.set_xlabel("Variação do IDEB (2019 → 2023)")
    ax.set_title(f"Top 10 — maior melhora no IDEB do Ensino Médio — {SIGLA}")
    subtitulo("Variação = IDEB 2023 − IDEB 2019. Fonte: INEP.")
    salvar("B2_top10_melhora_ideb")

# ── B3. Evolução das médias SAEB ─────────────────────────────────────────────
print("\n── B3. Evolução SAEB ──")
cols_saeb = [c for c in ["SAEB_9_LP", "SAEB_9_MT", "SAEB_12_LP", "SAEB_12_MT"] if c in df.columns]
if cols_saeb:
    saeb_ano = df.dropna(subset=[cols_saeb[0]]).groupby("ANO")[cols_saeb].mean()
    print(saeb_ano.round(2))

    fig, ax = plt.subplots(figsize=(9, 5))
    for i, col in enumerate(cols_saeb):
        ax.plot(saeb_ano.index, saeb_ano[col], marker="o", color=PALETTE[i],
                linewidth=2, markersize=6, label=label(col))
    ax.set_title(f"Evolução das médias de proficiência SAEB — {SIGLA}")
    ax.set_ylabel("Proficiência média (TRI)")
    ax.set_xlabel("Ano")
    ax.legend(ncol=2)
    subtitulo("Fonte: INEP — SAEB. Rede pública, localização total. Anos 2019, 2021, 2023.")
    salvar("B3_saeb_evolucao")

# ── B4. Evolução das médias ENEM ─────────────────────────────────────────────
print("\n── B4. Evolução ENEM ──")
cols_enem = [c for c in [
    "ENEM_MEDIA_MT", "ENEM_MEDIA_CN", "ENEM_MEDIA_CH",
    "ENEM_MEDIA_LC", "ENEM_MEDIA_REDACAO", "ENEM_MEDIA_GERAL"
] if c in df.columns]
if cols_enem:
    enem_ano = df.dropna(subset=["ENEM_MEDIA_GERAL"]).groupby("ANO")[cols_enem].mean()
    print(enem_ano.round(2))

    fig, ax = plt.subplots(figsize=(10, 5))
    for i, col in enumerate(cols_enem):
        ls = "-" if col == "ENEM_MEDIA_GERAL" else "--"
        lw = 2.5 if col == "ENEM_MEDIA_GERAL" else 1.5
        ax.plot(enem_ano.index, enem_ano[col], marker="o", color=PALETTE[i % len(PALETTE)],
                linewidth=lw, linestyle=ls, markersize=5, label=label(col))
    ax.set_title(f"Evolução das médias municipais do ENEM — {SIGLA}")
    ax.set_ylabel("Nota média (TRI)")
    ax.set_xlabel("Ano")
    ax.legend(ncol=2)
    subtitulo("Médias calculadas sobre participantes de escolas estaduais e municipais, zona urbana.")
    salvar("B4_enem_evolucao")

# ── B5. IDEB x Abandono ──────────────────────────────────────────────────────
print("\n── B5. IDEB x Abandono ──")
if "IDEB_MEDIO" in df.columns and "ABANDONO_MED_TOTAL" in df.columns:
    d = df.dropna(subset=["IDEB_MEDIO", "ABANDONO_MED_TOTAL"])
    r = d[["IDEB_MEDIO", "ABANDONO_MED_TOTAL"]].corr().iloc[0, 1]
    print(f"r = {r:.3f}")

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(d["IDEB_MEDIO"], d["ABANDONO_MED_TOTAL"],
               alpha=0.25, s=8, color=PALETTE[4], rasterized=True)
    m, b = np.polyfit(d["IDEB_MEDIO"].dropna(), d["ABANDONO_MED_TOTAL"].dropna(), 1)
    x_line = np.linspace(d["IDEB_MEDIO"].min(), d["IDEB_MEDIO"].max(), 100)
    ax.plot(x_line, m*x_line + b, color="black", linewidth=1.5, label=f"r = {r:.3f}")
    ax.set_xlabel("IDEB — Ensino Médio")
    ax.set_ylabel("Taxa de abandono (%)")
    ax.set_title(f"IDEB x Abandono no Ensino Médio — {SIGLA}")
    ax.legend()
    subtitulo("Cada ponto representa um município-ano.")
    salvar("B5_ideb_vs_abandono")

# ── B6. ENEM x Abandono ──────────────────────────────────────────────────────
print("\n── B6. ENEM x Abandono ──")
if "ENEM_MEDIA_GERAL" in df.columns and "ABANDONO_MED_TOTAL" in df.columns:
    d = df.dropna(subset=["ENEM_MEDIA_GERAL", "ABANDONO_MED_TOTAL"])
    r = d[["ENEM_MEDIA_GERAL", "ABANDONO_MED_TOTAL"]].corr().iloc[0, 1]
    print(f"r = {r:.3f}")

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(d["ENEM_MEDIA_GERAL"], d["ABANDONO_MED_TOTAL"],
               alpha=0.25, s=8, color=PALETTE[3], rasterized=True)
    m, b = np.polyfit(d["ENEM_MEDIA_GERAL"], d["ABANDONO_MED_TOTAL"], 1)
    x_line = np.linspace(d["ENEM_MEDIA_GERAL"].min(), d["ENEM_MEDIA_GERAL"].max(), 100)
    ax.plot(x_line, m*x_line + b, color="black", linewidth=1.5, label=f"r = {r:.3f}")
    ax.set_xlabel("ENEM — Média geral")
    ax.set_ylabel("Taxa de abandono (%)")
    ax.set_title(f"ENEM x Abandono no Ensino Médio — {SIGLA}")
    ax.legend()
    subtitulo("Cada ponto representa um município-ano.")
    salvar("B6_enem_vs_abandono")


# ══════════════════════════════════════════════════════════════════════════════
# BLOCO C — INVESTIMENTO E FATORES SOCIOECONÔMICOS
# ══════════════════════════════════════════════════════════════════════════════

# ── C1. Evolução do gasto por aluno ──────────────────────────────────────────
print("\n── C1. Evolução do gasto por aluno ──")
if "GASTO_ALUNO" in df_limpo.columns:
    gasto_ano = df_limpo.groupby("ANO")["GASTO_ALUNO"].mean()
    print(gasto_ano.round(0))

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(gasto_ano.index, gasto_ano.values, color=PALETTE[2], edgecolor="white", width=0.6)
    for x, y in zip(gasto_ano.index, gasto_ano.values):
        ax.text(x, y + 50, f"R${y:,.0f}", ha="center", fontsize=9)
    ax.set_title(f"Evolução do gasto público médio por aluno — {SIGLA}")
    ax.set_ylabel("Gasto médio por aluno (R$)")
    ax.set_xlabel("Ano")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R${x:,.0f}"))
    subtitulo("Fonte: SIOPE/FNDE. Gasto = despesa paga / matrículas na educação básica.")
    salvar("C1_gasto_aluno_evolucao")

# ── C2. Gasto por aluno x Abandono ───────────────────────────────────────────
print("\n── C2. Gasto x Abandono ──")
if "GASTO_ALUNO" in df_limpo.columns and "ABANDONO_MED_TOTAL" in df_limpo.columns:
    d = df_limpo.dropna(subset=["GASTO_ALUNO", "ABANDONO_MED_TOTAL"])
    r_fund = d[["GASTO_ALUNO", "ABANDONO_FUND_TOTAL"]].corr().iloc[0, 1] if "ABANDONO_FUND_TOTAL" in d.columns else None
    r_med  = d[["GASTO_ALUNO", "ABANDONO_MED_TOTAL"]].corr().iloc[0, 1]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    if "ABANDONO_FUND_TOTAL" in d.columns:
        axes[0].scatter(d["GASTO_ALUNO"], d["ABANDONO_FUND_TOTAL"],
                        alpha=0.2, s=8, color=PALETTE[0], rasterized=True)
        m, b = np.polyfit(d["GASTO_ALUNO"], d["ABANDONO_FUND_TOTAL"], 1)
        x_line = np.linspace(d["GASTO_ALUNO"].min(), d["GASTO_ALUNO"].max(), 100)
        axes[0].plot(x_line, m*x_line+b, color="black", lw=1.5, label=f"r = {r_fund:.3f}")
        axes[0].set_xlabel("Gasto por aluno (R$)")
        axes[0].set_ylabel("Taxa de abandono (%)")
        axes[0].set_title("Ensino Fundamental")
        axes[0].legend()

    axes[1].scatter(d["GASTO_ALUNO"], d["ABANDONO_MED_TOTAL"],
                    alpha=0.2, s=8, color=PALETTE[1], rasterized=True)
    m, b = np.polyfit(d["GASTO_ALUNO"], d["ABANDONO_MED_TOTAL"], 1)
    x_line = np.linspace(d["GASTO_ALUNO"].min(), d["GASTO_ALUNO"].max(), 100)
    axes[1].plot(x_line, m*x_line+b, color="black", lw=1.5, label=f"r = {r_med:.3f}")
    axes[1].set_xlabel("Gasto por aluno (R$)")
    axes[1].set_ylabel("Taxa de abandono (%)")
    axes[1].set_title("Ensino Médio")
    axes[1].legend()

    plt.suptitle(f"Gasto público por aluno × Taxa de abandono — {SIGLA}", fontsize=13, fontweight="bold")
    subtitulo("Fonte: SIOPE/FNDE e INEP — Taxas de Rendimento Escolar.")
    salvar("C2_gasto_vs_abandono")

# ── C3. Gasto por aluno x IDEB e ENEM ────────────────────────────────────────
print("\n── C3. Gasto x Desempenho ──")
if "GASTO_ALUNO" in df_limpo.columns:
    targets = [(c, label(c), PALETTE[i]) for i, c in enumerate(
        [c for c in ["IDEB_MEDIO", "ENEM_MEDIA_GERAL", "SAEB_12_MT"] if c in df_limpo.columns]
    )]
    if targets:
        fig, axes = plt.subplots(1, len(targets), figsize=(5*len(targets), 5))
        if len(targets) == 1:
            axes = [axes]
        for ax, (col, lbl, cor) in zip(axes, targets):
            d = df_limpo.dropna(subset=["GASTO_ALUNO", col])
            r = d[["GASTO_ALUNO", col]].corr().iloc[0, 1]
            ax.scatter(d["GASTO_ALUNO"], d[col], alpha=0.2, s=8, color=cor, rasterized=True)
            m, b = np.polyfit(d["GASTO_ALUNO"], d[col], 1)
            x_line = np.linspace(d["GASTO_ALUNO"].min(), d["GASTO_ALUNO"].max(), 100)
            ax.plot(x_line, m*x_line+b, color="black", lw=1.5, label=f"r = {r:.3f}")
            ax.set_xlabel("Gasto por aluno (R$)")
            ax.set_ylabel(lbl)
            ax.set_title(lbl)
            ax.legend()
        plt.suptitle(f"Gasto por aluno × Indicadores de desempenho — {SIGLA}", fontsize=13, fontweight="bold")
        subtitulo("Fonte: SIOPE/FNDE, INEP — IDEB, SAEB e microdados ENEM.")
        salvar("C3_gasto_vs_desempenho")

# ── C4. Top 10 maior e menor gasto por aluno ─────────────────────────────────
print("\n── C4. Top 10 maior/menor gasto ──")
if "GASTO_ALUNO" in df_limpo.columns:
    gasto_muni = df_limpo.groupby("NO_MUNICIPIO")["GASTO_ALUNO"].mean()
    top_maior = gasto_muni.sort_values(ascending=False).head(10)
    top_menor = gasto_muni.sort_values().head(10)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].barh(range(len(top_maior)), top_maior.sort_values().values,
                 color=PALETTE[2], edgecolor="white")
    axes[0].set_yticks(range(len(top_maior)))
    axes[0].set_yticklabels(top_maior.sort_values().index, fontsize=9)
    axes[0].set_xlabel("Gasto médio por aluno (R$)")
    axes[0].set_title("Top 10 — maior gasto")
    axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R${x:,.0f}"))

    axes[1].barh(range(len(top_menor)), top_menor.sort_values(ascending=False).values,
                 color=PALETTE[1], edgecolor="white")
    axes[1].set_yticks(range(len(top_menor)))
    axes[1].set_yticklabels(top_menor.sort_values(ascending=False).index, fontsize=9)
    axes[1].set_xlabel("Gasto médio por aluno (R$)")
    axes[1].set_title("Top 10 — menor gasto")
    axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R${x:,.0f}"))

    plt.suptitle(f"Extremos de gasto público por aluno — {SIGLA} (média do período)", fontsize=13, fontweight="bold")
    subtitulo("Fonte: SIOPE/FNDE.")
    salvar("C4_top10_gasto_aluno")

# ── C5. INSE x Abandono e Desempenho ─────────────────────────────────────────
print("\n── C5. INSE x Abandono e Desempenho ──")
if "INSE" in df.columns:
    targets = [(c, label(c), PALETTE[i]) for i, c in enumerate(
        [c for c in ["ABANDONO_MED_TOTAL", "IDEB_MEDIO", "ENEM_MEDIA_GERAL"] if c in df.columns]
    )]
    if targets:
        fig, axes = plt.subplots(1, len(targets), figsize=(5*len(targets), 5))
        if len(targets) == 1:
            axes = [axes]
        for ax, (col, lbl, cor) in zip(axes, targets):
            d = df.dropna(subset=["INSE", col])
            r = d[["INSE", col]].corr().iloc[0, 1]
            ax.scatter(d["INSE"], d[col], alpha=0.2, s=8, color=cor, rasterized=True)
            m, b = np.polyfit(d["INSE"], d[col], 1)
            x_line = np.linspace(d["INSE"].min(), d["INSE"].max(), 100)
            ax.plot(x_line, m*x_line+b, color="black", lw=1.5, label=f"r = {r:.3f}")
            ax.set_xlabel("INSE (nível socioeconômico)")
            ax.set_ylabel(lbl)
            ax.set_title(lbl)
            ax.legend()
        plt.suptitle(f"INSE × Abandono e Desempenho — {SIGLA}", fontsize=13, fontweight="bold")
        subtitulo("Fonte: INEP — INSE 2019, 2021, 2023.")
        salvar("C5_inse_vs_outcomes")

# ── C6. PIB per capita x Abandono e Desempenho ───────────────────────────────
print("\n── C6. PIB x Abandono e Desempenho ──")
if "PIB_PERCAPITA" in df.columns:
    targets = [(c, label(c), PALETTE[i]) for i, c in enumerate(
        [c for c in ["ABANDONO_MED_TOTAL", "IDEB_MEDIO", "ENEM_MEDIA_GERAL"] if c in df.columns]
    )]
    if targets:
        fig, axes = plt.subplots(1, len(targets), figsize=(5*len(targets), 5))
        if len(targets) == 1:
            axes = [axes]
        for ax, (col, lbl, cor) in zip(axes, targets):
            d = df.dropna(subset=["PIB_PERCAPITA", col])
            r = d[["PIB_PERCAPITA", col]].corr().iloc[0, 1]
            ax.scatter(d["PIB_PERCAPITA"], d[col], alpha=0.2, s=8, color=cor, rasterized=True)
            m, b = np.polyfit(d["PIB_PERCAPITA"], d[col], 1)
            x_line = np.linspace(d["PIB_PERCAPITA"].min(), d["PIB_PERCAPITA"].max(), 100)
            ax.plot(x_line, m*x_line+b, color="black", lw=1.5, label=f"r = {r:.3f}")
            ax.set_xlabel("PIB per capita (R$)")
            ax.set_ylabel(lbl)
            ax.set_title(lbl)
            ax.legend()
        plt.suptitle(f"PIB per capita × Abandono e Desempenho — {SIGLA}", fontsize=13, fontweight="bold")
        subtitulo("Fonte: IBGE — tabela 5938 SIDRA. PIB per capita calculado com população do Censo 2022.")
        salvar("C6_pib_vs_outcomes")

# ── C7. Renda per capita x Abandono e Desempenho ─────────────────────────────
print("\n── C7. Renda x Abandono e Desempenho ──")
if "RENDA_PERCAPITA" in df.columns:
    targets = [(c, label(c), PALETTE[i]) for i, c in enumerate(
        [c for c in ["ABANDONO_MED_TOTAL", "IDEB_MEDIO", "ENEM_MEDIA_GERAL"] if c in df.columns]
    )]
    if targets:
        fig, axes = plt.subplots(1, len(targets), figsize=(5*len(targets), 5))
        if len(targets) == 1:
            axes = [axes]
        for ax, (col, lbl, cor) in zip(axes, targets):
            d = df.dropna(subset=["RENDA_PERCAPITA", col])
            r = d[["RENDA_PERCAPITA", col]].corr().iloc[0, 1]
            ax.scatter(d["RENDA_PERCAPITA"], d[col], alpha=0.2, s=8, color=cor, rasterized=True)
            m, b = np.polyfit(d["RENDA_PERCAPITA"], d[col], 1)
            x_line = np.linspace(d["RENDA_PERCAPITA"].min(), d["RENDA_PERCAPITA"].max(), 100)
            ax.plot(x_line, m*x_line+b, color="black", lw=1.5, label=f"r = {r:.3f}")
            ax.set_xlabel("Renda per capita (R$)")
            ax.set_ylabel(lbl)
            ax.set_title(lbl)
            ax.legend()
        plt.suptitle(f"Renda per capita × Abandono e Desempenho — {SIGLA}", fontsize=13, fontweight="bold")
        subtitulo("Fonte: IBGE — tabela 10295 SIDRA (Censo 2022, resultados preliminares da amostra).")
        salvar("C7_renda_vs_outcomes")

# ── C8. Taxa de analfabetismo x Abandono e Desempenho ────────────────────────
print("\n── C8. Analfabetismo x Abandono e Desempenho ──")
if "TAXA_ANALFABETISMO" in df.columns:
    targets = [(c, label(c), PALETTE[i]) for i, c in enumerate(
        [c for c in ["ABANDONO_MED_TOTAL", "IDEB_MEDIO"] if c in df.columns]
    )]
    if targets:
        fig, axes = plt.subplots(1, len(targets), figsize=(5*len(targets), 5))
        if len(targets) == 1:
            axes = [axes]
        for ax, (col, lbl, cor) in zip(axes, targets):
            d = df.dropna(subset=["TAXA_ANALFABETISMO", col])
            r = d[["TAXA_ANALFABETISMO", col]].corr().iloc[0, 1]
            ax.scatter(d["TAXA_ANALFABETISMO"]*100, d[col], alpha=0.2, s=8, color=cor, rasterized=True)
            m, b = np.polyfit(d["TAXA_ANALFABETISMO"]*100, d[col], 1)
            x_line = np.linspace((d["TAXA_ANALFABETISMO"]*100).min(), (d["TAXA_ANALFABETISMO"]*100).max(), 100)
            ax.plot(x_line, m*x_line+b, color="black", lw=1.5, label=f"r = {r:.3f}")
            ax.set_xlabel("Taxa de analfabetismo (%)")
            ax.set_ylabel(lbl)
            ax.set_title(lbl)
            ax.legend()
        plt.suptitle(f"Taxa de analfabetismo × Abandono e IDEB — {SIGLA}", fontsize=13, fontweight="bold")
        subtitulo("Fonte: IBGE — Censo Demográfico 2022. Pessoas de 15 anos ou mais.")
        salvar("C8_analfabetismo_vs_outcomes")

# ── C9. Bolsa Família x Abandono e Desempenho ────────────────────────────────
print("\n── C9. Bolsa Família x Abandono e Desempenho ──")
if "BF_MEDIA_MENSAL" in df.columns:
    df["BF_POR_ALUNO"] = df["BF_MEDIA_MENSAL"] / df["QT_MAT_BAS"]
    targets = [(c, label(c), PALETTE[i]) for i, c in enumerate(
        [c for c in ["ABANDONO_MED_TOTAL", "IDEB_MEDIO"] if c in df.columns]
    )]
    if targets:
        fig, axes = plt.subplots(1, len(targets), figsize=(5*len(targets), 5))
        if len(targets) == 1:
            axes = [axes]
        for ax, (col, lbl, cor) in zip(axes, targets):
            d = df.dropna(subset=["BF_POR_ALUNO", col])
            d = d[d["BF_POR_ALUNO"] > 0]
            r = d[["BF_POR_ALUNO", col]].corr().iloc[0, 1]
            ax.scatter(d["BF_POR_ALUNO"], d[col], alpha=0.2, s=8, color=cor, rasterized=True)
            m, b = np.polyfit(d["BF_POR_ALUNO"], d[col], 1)
            x_line = np.linspace(d["BF_POR_ALUNO"].min(), d["BF_POR_ALUNO"].max(), 100)
            ax.plot(x_line, m*x_line+b, color="black", lw=1.5, label=f"r = {r:.3f}")
            ax.set_xlabel("Beneficiários BF por matrícula")
            ax.set_ylabel(lbl)
            ax.set_title(lbl)
            ax.legend()
        plt.suptitle(f"Bolsa Família por matrícula × Abandono e IDEB — {SIGLA}", fontsize=13, fontweight="bold")
        subtitulo("Fonte: MDS — dados.gov.br. Disponível para 2021, 2023 e 2024.")
        salvar("C9_bf_vs_outcomes")

# ── C10. Relação aluno/docente x Abandono e Desempenho ───────────────────────
print("\n── C10. Aluno/docente x Abandono e Desempenho ──")
if "ALUNO_DOC_MED" in df.columns:
    df_v = df[df["ALUNO_DOC_MED"].between(1, 80)].copy()
    targets = [(c, label(c), PALETTE[i]) for i, c in enumerate(
        [c for c in ["ABANDONO_MED_TOTAL", "IDEB_MEDIO", "ENEM_MEDIA_GERAL"] if c in df_v.columns]
    )]
    if targets:
        fig, axes = plt.subplots(1, len(targets), figsize=(5*len(targets), 5))
        if len(targets) == 1:
            axes = [axes]
        for ax, (col, lbl, cor) in zip(axes, targets):
            d = df_v.dropna(subset=["ALUNO_DOC_MED", col])
            r = d[["ALUNO_DOC_MED", col]].corr().iloc[0, 1]
            ax.scatter(d["ALUNO_DOC_MED"], d[col], alpha=0.2, s=8, color=cor, rasterized=True)
            m, b = np.polyfit(d["ALUNO_DOC_MED"], d[col], 1)
            x_line = np.linspace(d["ALUNO_DOC_MED"].min(), d["ALUNO_DOC_MED"].max(), 100)
            ax.plot(x_line, m*x_line+b, color="black", lw=1.5, label=f"r = {r:.3f}")
            ax.set_xlabel("Alunos por docente (Ensino Médio)")
            ax.set_ylabel(lbl)
            ax.set_title(lbl)
            ax.legend()
        plt.suptitle(f"Relação aluno/docente × Abandono e Desempenho — {SIGLA}", fontsize=13, fontweight="bold")
        subtitulo("Fonte: Censo Escolar INEP. Valores entre 1 e 80 alunos/docente.")
        salvar("C10_aluno_doc_vs_outcomes")


# ══════════════════════════════════════════════════════════════════════════════
# BLOCO D — INFRAESTRUTURA
# ══════════════════════════════════════════════════════════════════════════════

# ── D1. Heatmap infraestrutura x abandono ────────────────────────────────────
print("\n── D1. Infraestrutura x Abandono ──")
cols_ab2 = [c for c in ["ABANDONO_FUND_TOTAL", "ABANDONO_MED_TOTAL"] if c in df.columns]
if INFRA and cols_ab2:
    corr = df[INFRA + cols_ab2].corr()[cols_ab2].loc[INFRA]
    corr.index = [INFRA_LABELS.get(c, c) for c in corr.index]
    corr.columns = [label(c) for c in corr.columns]
    print(corr.round(3))

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap=CMAP_DIV, center=0,
                linewidths=0.5, ax=ax, annot_kws={"size": 10})
    ax.set_title(f"Correlação: Infraestrutura × Taxa de abandono — {SIGLA}")
    subtitulo("Coeficiente de Pearson. Fonte: Censo Escolar INEP e Taxas de Rendimento INEP.")
    salvar("D1_infra_vs_abandono")

# ── D2. Heatmap infraestrutura x IDEB e SAEB ─────────────────────────────────
print("\n── D2. Infraestrutura x Desempenho ──")
cols_desemp = [c for c in ["IDEB_MEDIO", "SAEB_12_MT", "ENEM_MEDIA_GERAL"] if c in df.columns]
if INFRA and cols_desemp:
    corr = df[INFRA + cols_desemp].corr()[cols_desemp].loc[INFRA]
    corr.index = [INFRA_LABELS.get(c, c) for c in corr.index]
    corr.columns = [label(c) for c in corr.columns]
    print(corr.round(3))

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap=CMAP_DIV, center=0,
                linewidths=0.5, ax=ax, annot_kws={"size": 10})
    ax.set_title(f"Correlação: Infraestrutura × Desempenho — {SIGLA}")
    subtitulo("Coeficiente de Pearson. Fonte: Censo Escolar INEP, IDEB, SAEB e ENEM.")
    salvar("D2_infra_vs_desempenho")


# ══════════════════════════════════════════════════════════════════════════════
# BLOCO E — MATRIZES DE CORRELAÇÃO GERAL
# ══════════════════════════════════════════════════════════════════════════════

# ── E1. Correlação de todas as variáveis com abandono e IDEB ─────────────────
print("\n── E1. Resumo de correlações ──")
todas = INFRA + [c for c in [
    "ALUNO_DOC_MED", "GASTO_ALUNO", "PIB_PERCAPITA", "RENDA_PERCAPITA",
    "INSE", "TAXA_ANALFABETISMO", "BF_POR_ALUNO",
    "SAEB_12_MT", "ENEM_MEDIA_GERAL"
] if c in df.columns]
alvo = [c for c in ["ABANDONO_FUND_TOTAL", "ABANDONO_MED_TOTAL",
                    "IDEB_MEDIO", "ENEM_MEDIA_GERAL"] if c in df.columns]

if todas and alvo:
    resumo = df[todas + alvo].corr()[alvo].loc[todas]
    resumo.index = [INFRA_LABELS.get(c, label(c)) for c in resumo.index]
    resumo.columns = [label(c) for c in resumo.columns]
    print(resumo.round(3).to_string())

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(resumo, annot=True, fmt=".2f", cmap=CMAP_DIV, center=0,
                linewidths=0.5, ax=ax, annot_kws={"size": 9})
    ax.set_title(f"Correlações com abandono e desempenho — {SIGLA}", pad=15)
    subtitulo("Coeficiente de Pearson. Todas as fontes integradas no dataframe master.")
    salvar("E1_resumo_correlacoes")

# ── E2. Matriz de correlação completa entre todas as variáveis ───────────────
print("\n── E2. Matriz de correlação completa ──")
todas_vars = [c for c in (
    INFRA + VARS_SOCIO + ["ABANDONO_FUND_TOTAL", "ABANDONO_MED_TOTAL",
                           "IDEB_MEDIO", "SAEB_12_MT", "ENEM_MEDIA_GERAL"]
) if c in df.columns]

if len(todas_vars) > 3:
    matrix = df[todas_vars].corr()
    labels_matrix = [INFRA_LABELS.get(c, label(c)) for c in matrix.columns]

    fig, ax = plt.subplots(figsize=(14, 11))
    mask = np.triu(np.ones_like(matrix, dtype=bool))
    sns.heatmap(matrix, mask=mask, annot=True, fmt=".2f", cmap=CMAP_DIV,
                center=0, linewidths=0.3, ax=ax, annot_kws={"size": 7},
                xticklabels=labels_matrix, yticklabels=labels_matrix)
    ax.set_title(f"Matriz de correlação completa — {SIGLA}", pad=15)
    ax.tick_params(axis="x", rotation=45)
    ax.tick_params(axis="y", rotation=0)
    subtitulo("Triângulo inferior. Coeficiente de Pearson. Todas as variáveis do dataframe master.")
    salvar("E2_matriz_correlacao_completa")




# ══════════════════════════════════════════════════════════════════════════════
# BLOCO F — DISTORÇÃO IDADE-SÉRIE (TDI) E ADEQUAÇÃO DOCENTE (AFD)
# ══════════════════════════════════════════════════════════════════════════════

# ── F1. Evolução da distorção idade-série ─────────────────────────────────────
print("\n── F1. Evolução da distorção idade-série ──")
cols_tdi = [c for c in ["TDI_FUND_TOTAL", "TDI_MED_TOTAL"] if c in df.columns]
if cols_tdi:
    tdi_ano = df.groupby("ANO")[cols_tdi].mean()
    print(tdi_ano.round(2))

    fig, ax = plt.subplots(figsize=(9, 5))
    tdi_labels = {"TDI_FUND_TOTAL": "Ens. Fundamental", "TDI_MED_TOTAL": "Ens. Médio"}
    for i, col in enumerate(cols_tdi):
        ax.plot(tdi_ano.index, tdi_ano[col], marker="o", color=PALETTE[i],
                linewidth=2, markersize=6, label=tdi_labels.get(col, col))
    ax.set_title(f"Evolução da taxa de distorção idade-série — {SIGLA}")
    ax.set_ylabel("Taxa média de distorção (%)")
    ax.set_xlabel("Ano")
    ax.legend()
    subtitulo("Fonte: INEP — Taxas de Distorção Idade-série. Escolas estaduais e municipais, Total.")
    salvar("F1_tdi_evolucao")

# ── F2. TDI por série do Ensino Médio ─────────────────────────────────────────
print("\n── F2. TDI por série do Ensino Médio ──")
cols_tdi_serie = [c for c in ["TDI_MED_1SERIE", "TDI_MED_2SERIE", "TDI_MED_3SERIE"] if c in df.columns]
if cols_tdi_serie:
    tdi_serie = df.groupby("ANO")[cols_tdi_serie].mean()
    print(tdi_serie.round(2))

    fig, ax = plt.subplots(figsize=(9, 5))
    serie_labels = {
        "TDI_MED_1SERIE": "1ª série",
        "TDI_MED_2SERIE": "2ª série",
        "TDI_MED_3SERIE": "3ª série",
    }
    for i, col in enumerate(cols_tdi_serie):
        ax.plot(tdi_serie.index, tdi_serie[col], marker="o", color=PALETTE[i],
                linewidth=2, markersize=6, label=serie_labels.get(col, col))
    ax.set_title(f"Distorção idade-série no Ensino Médio por série — {SIGLA}")
    ax.set_ylabel("Taxa média de distorção (%)")
    ax.set_xlabel("Ano")
    ax.legend()
    subtitulo("Fonte: INEP — Taxas de Distorção Idade-série.")
    salvar("F2_tdi_por_serie")

# ── F3. TDI x Abandono ────────────────────────────────────────────────────────
print("\n── F3. TDI x Abandono ──")
if "TDI_MED_TOTAL" in df.columns and "ABANDONO_MED_TOTAL" in df.columns:
    d = df.dropna(subset=["TDI_MED_TOTAL", "ABANDONO_MED_TOTAL"])
    r = d[["TDI_MED_TOTAL", "ABANDONO_MED_TOTAL"]].corr().iloc[0, 1]
    print(f"  r(TDI_MED x ABANDONO_MED) = {r:.3f}")

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(d["TDI_MED_TOTAL"], d["ABANDONO_MED_TOTAL"],
               alpha=0.25, s=8, color=PALETTE[1], rasterized=True)
    m, b = np.polyfit(d["TDI_MED_TOTAL"], d["ABANDONO_MED_TOTAL"], 1)
    x_line = np.linspace(d["TDI_MED_TOTAL"].min(), d["TDI_MED_TOTAL"].max(), 100)
    ax.plot(x_line, m*x_line + b, color="black", linewidth=1.5, label=f"r = {r:.3f}")
    ax.set_xlabel("Taxa de distorção idade-série — Ensino Médio (%)")
    ax.set_ylabel("Taxa de abandono — Ensino Médio (%)")
    ax.set_title(f"Distorção idade-série × Abandono no Ensino Médio — {SIGLA}")
    ax.legend()
    subtitulo("Cada ponto representa um município-ano. Fonte: INEP.")
    salvar("F3_tdi_vs_abandono")

# ── F4. TDI x IDEB e Desempenho ───────────────────────────────────────────────
print("\n── F4. TDI x Desempenho ──")
if "TDI_MED_TOTAL" in df.columns:
    targets = [(c, label(c), PALETTE[i]) for i, c in enumerate(
        [c for c in ["IDEB_MEDIO", "SAEB_12_MT", "ENEM_MEDIA_GERAL"] if c in df.columns]
    )]
    if targets:
        fig, axes = plt.subplots(1, len(targets), figsize=(5*len(targets), 5))
        if len(targets) == 1:
            axes = [axes]
        for ax, (col, lbl, cor) in zip(axes, targets):
            d = df.dropna(subset=["TDI_MED_TOTAL", col])
            r = d[["TDI_MED_TOTAL", col]].corr().iloc[0, 1]
            ax.scatter(d["TDI_MED_TOTAL"], d[col], alpha=0.2, s=8, color=cor, rasterized=True)
            m, b = np.polyfit(d["TDI_MED_TOTAL"], d[col], 1)
            x_line = np.linspace(d["TDI_MED_TOTAL"].min(), d["TDI_MED_TOTAL"].max(), 100)
            ax.plot(x_line, m*x_line+b, color="black", lw=1.5, label=f"r = {r:.3f}")
            ax.set_xlabel("TDI — Ensino Médio (%)")
            ax.set_ylabel(lbl)
            ax.set_title(lbl)
            ax.legend()
        plt.suptitle(f"Distorção idade-série × Indicadores de desempenho — {SIGLA}",
                     fontsize=13, fontweight="bold")
        subtitulo("Fonte: INEP — TDI, IDEB, SAEB e microdados ENEM.")
        salvar("F4_tdi_vs_desempenho")

# ── F5. Evolução da adequação da formação docente ─────────────────────────────
print("\n── F5. Evolução da adequação docente (AFD) ──")
cols_afd_evo = [c for c in ["AFD_MED_ADEQUADO", "AFD_FUND_ADEQUADO"] if c in df.columns]
if cols_afd_evo:
    afd_ano = df.groupby("ANO")[cols_afd_evo].mean()
    print(afd_ano.round(2))

    fig, ax = plt.subplots(figsize=(9, 5))
    afd_labels = {
        "AFD_MED_ADEQUADO":  "Ens. Médio — formação adequada (Grupo 1)",
        "AFD_FUND_ADEQUADO": "Ens. Fund. — formação adequada (Grupo 1)",
    }
    for i, col in enumerate(cols_afd_evo):
        ax.plot(afd_ano.index, afd_ano[col], marker="o", color=PALETTE[i],
                linewidth=2, markersize=6, label=afd_labels.get(col, col))
    ax.set_title(f"Evolução do percentual de docentes com formação adequada — {SIGLA}")
    ax.set_ylabel("% docentes com formação plena (Grupo 1)")
    ax.set_xlabel("Ano")
    ax.legend()
    subtitulo("Grupo 1 = licenciatura na mesma área da disciplina. Fonte: INEP — AFD.")
    salvar("F5_afd_evolucao")

# ── F6. AFD x Abandono e Desempenho ───────────────────────────────────────────
print("\n── F6. AFD x Abandono e Desempenho ──")
if "AFD_MED_ADEQUADO" in df.columns:
    targets = [(c, label(c), PALETTE[i]) for i, c in enumerate(
        [c for c in ["ABANDONO_MED_TOTAL", "IDEB_MEDIO", "SAEB_12_MT"] if c in df.columns]
    )]
    if targets:
        fig, axes = plt.subplots(1, len(targets), figsize=(5*len(targets), 5))
        if len(targets) == 1:
            axes = [axes]
        for ax, (col, lbl, cor) in zip(axes, targets):
            d = df.dropna(subset=["AFD_MED_ADEQUADO", col])
            r = d[["AFD_MED_ADEQUADO", col]].corr().iloc[0, 1]
            ax.scatter(d["AFD_MED_ADEQUADO"], d[col], alpha=0.2, s=8, color=cor, rasterized=True)
            m, b = np.polyfit(d["AFD_MED_ADEQUADO"], d[col], 1)
            x_line = np.linspace(d["AFD_MED_ADEQUADO"].min(), d["AFD_MED_ADEQUADO"].max(), 100)
            ax.plot(x_line, m*x_line+b, color="black", lw=1.5, label=f"r = {r:.3f}")
            ax.set_xlabel("% docentes com formação adequada — EM (%)")
            ax.set_ylabel(lbl)
            ax.set_title(lbl)
            ax.legend()
        plt.suptitle(f"Adequação da formação docente × Abandono e Desempenho — {SIGLA}",
                     fontsize=13, fontweight="bold")
        subtitulo("Grupo 1 = licenciatura na mesma área. Fonte: INEP — AFD.")
        salvar("F6_afd_vs_outcomes")

# ── F7. Heatmap TDI e AFD x todos os outcomes ─────────────────────────────────
print("\n── F7. Heatmap TDI + AFD x outcomes ──")
vars_tdi_afd = [c for c in [
    "TDI_FUND_TOTAL", "TDI_MED_TOTAL",
    "AFD_MED_ADEQUADO", "AFD_FUND_ADEQUADO",
] if c in df.columns]
alvo_f7 = [c for c in [
    "ABANDONO_FUND_TOTAL", "ABANDONO_MED_TOTAL", "IDEB_MEDIO",
    "SAEB_12_MT", "ENEM_MEDIA_GERAL"
] if c in df.columns]

if vars_tdi_afd and alvo_f7:
    corr_f7 = df[vars_tdi_afd + alvo_f7].corr()[alvo_f7].loc[vars_tdi_afd]
    labels_f7 = {
        "TDI_FUND_TOTAL":    "TDI Fund. Total (%)",
        "TDI_MED_TOTAL":     "TDI Médio Total (%)",
        "AFD_MED_ADEQUADO":  "AFD Médio — Grupo 1 (%)",
        "AFD_FUND_ADEQUADO": "AFD Fund. — Grupo 1 (%)",
    }
    corr_f7.index   = [labels_f7.get(c, c) for c in corr_f7.index]
    corr_f7.columns = [label(c) for c in corr_f7.columns]
    print(corr_f7.round(3))

    fig, ax = plt.subplots(figsize=(9, 4))
    sns.heatmap(corr_f7, annot=True, fmt=".2f", cmap=CMAP_DIV, center=0,
                linewidths=0.5, ax=ax, annot_kws={"size": 10})
    ax.set_title(f"Correlação: TDI e AFD × Abandono e Desempenho — {SIGLA}", pad=12)
    subtitulo("Coeficiente de Pearson. Fonte: INEP — TDI, AFD, Taxas de Rendimento, IDEB, SAEB, ENEM.")
    salvar("F7_tdi_afd_heatmap")














# ── A5. Evolução do abandono por rede (estadual vs municipal) ─────────────────
print("\n── A5. Abandono por rede ──")
ARQ_REDES = Path(PASTA_SAIDA) / "Rendimento" / f"taxa_rendimento_redes_{SIGLA.lower()}.csv"
if ARQ_REDES.exists():
    df_redes = pd.read_csv(ARQ_REDES, sep=";")
    df_redes["DEPENDENCIA"] = df_redes["DEPENDENCIA"].str.strip()

    for nivel, col in [("Ensino Médio", "ABANDONO_MED_TOTAL"),
                        ("Ensino Fundamental", "ABANDONO_FUND_TOTAL")]:
        if col not in df_redes.columns:
            continue
        d = df_redes.groupby(["ANO", "DEPENDENCIA"])[col].mean().unstack()
        fig, ax = plt.subplots(figsize=(9, 5))
        for i, rede in enumerate([c for c in ["Estadual", "Municipal"] if c in d.columns]):
            ax.plot(d.index, d[rede], marker="o", color=PALETTE[i],
                    linewidth=2, markersize=6, label=rede)
        ax.set_title(f"Abandono no {nivel} por rede administrativa — {SIGLA}")
        ax.set_ylabel("Taxa média de abandono (%)")
        ax.set_xlabel("Ano")
        ax.legend()
        subtitulo(f"Fonte: INEP — Taxas de Rendimento Escolar. Localização Total.")
        salvar(f"A5_abandono_{nivel.replace(' ','_').lower()}_por_rede")

# ── A6. Abandono por série do EM e rede ──────────────────────────────────────
    print("\n── A6. Abandono por série do EM e rede ──")
    cols_series = [c for c in ["ABANDONO_MED_1SERIE", "ABANDONO_MED_2SERIE",
                                "ABANDONO_MED_3SERIE"] if c in df_redes.columns]
    serie_nomes = {"ABANDONO_MED_1SERIE": "1ª série",
                   "ABANDONO_MED_2SERIE": "2ª série",
                   "ABANDONO_MED_3SERIE": "3ª série"}
    if cols_series:
        for rede in ["Estadual", "Municipal"]:
            d = df_redes[df_redes["DEPENDENCIA"] == rede].groupby("ANO")[cols_series].mean()
            fig, ax = plt.subplots(figsize=(9, 5))
            for i, col in enumerate(cols_series):
                ax.plot(d.index, d[col], marker="o", color=PALETTE[i],
                        linewidth=2, markersize=6, label=serie_nomes.get(col, col))
            ax.set_title(f"Abandono por série do Ensino Médio — Rede {rede} — {SIGLA}")
            ax.set_ylabel("Taxa média de abandono (%)")
            ax.set_xlabel("Ano")
            ax.legend()
            subtitulo("Fonte: INEP — Taxas de Rendimento Escolar.")
            salvar(f"A6_abandono_series_rede_{rede.lower()}")

# ── A7. Comparativo estadual vs municipal por nível ──────────────────────────
    print("\n── A7. Comparativo estadual vs municipal ──")
    cols_niveis = [c for c in ["ABANDONO_FUND_TOTAL", "ABANDONO_MED_TOTAL"]
                   if c in df_redes.columns]
    if cols_niveis:
        medias = df_redes.groupby("DEPENDENCIA")[cols_niveis].mean()
        x = np.arange(len(cols_niveis))
        width = 0.35
        fig, ax = plt.subplots(figsize=(8, 5))
        for i, rede in enumerate([r for r in ["Estadual", "Municipal"] if r in medias.index]):
            ax.bar(x + i*width, medias.loc[rede, cols_niveis].values,
                   width, label=rede, color=PALETTE[i], edgecolor="white")
        ax.set_xticks(x + width/2)
        ax.set_xticklabels([label(c) for c in cols_niveis])
        ax.set_ylabel("Taxa média de abandono (%)")
        ax.set_title(f"Abandono médio por nível e rede administrativa — {SIGLA}")
        ax.legend()
        subtitulo("Média de todo o período disponível. Fonte: INEP — Taxas de Rendimento Escolar.")
        salvar("A7_abandono_comparativo_redes")
else:
    print(f"  ⚠️  Arquivo por rede não encontrado. Execute 007_Rendimento_Extrair.py primeiro.")
# ══════════════════════════════════════════════════════════════════════════════
# RESUMO FINAL
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{'='*60}")
print(f"ANÁLISE CONCLUÍDA — {SIGLA}")
print(f"Gráficos salvos em: {PASTA_GRAF}")
print(f"{'='*60}")