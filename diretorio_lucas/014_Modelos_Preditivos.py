import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import (accuracy_score, roc_auc_score, classification_report,
                              confusion_matrix, RocCurveDisplay)
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import permutation_importance
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
    "axes.titlesize":     12,
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
    "legend.framealpha":  0.85,
    "figure.dpi":         150,
    "savefig.dpi":        300,
    "savefig.bbox":       "tight",
    "savefig.facecolor":  "white",
})

BLUE   = "#2166ac"
RED    = "#d6604d"
ORANGE = "#f4a582"
GREEN  = "#4dac26"
GRAY   = "#636363"

def salvar(nome):
    path = PASTA_GRAF / f"{nome}_{SIGLA.lower()}.png"
    plt.savefig(path)
    plt.close()
    print(f"  ✓ {path.name}")

def fonte(texto):
    plt.figtext(0.5, -0.03, texto, ha="center", fontsize=8.5,
                color=GRAY, style="italic")

# ══════════════════════════════════════════════════════════════════════════════
# CARREGA DADOS
# ══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print(f"MODELOS PREDITIVOS — {SIGLA} (código {UF_COD})")
print("=" * 60)

if not MASTER.exists():
    print(f"✗ Master não encontrado: {MASTER}")
    exit()

df = pd.read_csv(MASTER, sep=";")
print(f"Shape: {df.shape} | Municípios: {df['CO_MUNICIPIO'].nunique()} | Anos: {sorted(df['ANO'].unique())}")

NOMES = {
    "INSE":                        "Nível socioeconômico (INSE)",
    "RENDA_PERCAPITA":             "Renda per capita",
    "GASTO_ALUNO":                 "Gasto por aluno",
    "PIB_PERCAPITA":               "PIB per capita",
    "ALUNO_DOC_MED":               "Alunos/docente (Médio)",
    "IN_REFEITORIO":               "Refeitório",
    "IN_ESGOTO_REDE_PUBLICA":      "Esgoto rede pública",
    "IN_BIBLIOTECA":               "Biblioteca",
    "IN_AGUA_POTAVEL":             "Água potável",
    "IN_QUADRA_ESPORTES":          "Quadra esportiva",
    "IN_LABORATORIO_INFORMATICA":  "Lab. informática",
    "IN_INTERNET":                 "Internet",
    "TDI_MED_TOTAL":               "Distorção idade-série (Médio)",
    "TDI_FUND_TOTAL":              "Distorção idade-série (Fund.)",
    "AFD_MED_ADEQUADO":            "Formação docente adequada (Médio)",
    "AFD_FUND_ADEQUADO":           "Formação docente adequada (Fund.)",
}

FEATURES_BASE = [
    "IN_BIBLIOTECA", "IN_LABORATORIO_INFORMATICA", "IN_INTERNET",
    "IN_QUADRA_ESPORTES", "IN_REFEITORIO", "IN_AGUA_POTAVEL",
    "IN_ESGOTO_REDE_PUBLICA",
    "ALUNO_DOC_MED", "GASTO_ALUNO", "PIB_PERCAPITA", "INSE",
]

# Features estendidas — inclui TDI e AFD quando disponíveis
FEATURES_EXTENDED = FEATURES_BASE + [
    "TDI_MED_TOTAL",      # distorção idade-série ensino médio
    "TDI_FUND_TOTAL",     # distorção idade-série fundamental
    "AFD_MED_ADEQUADO",   # % docentes com formação adequada ensino médio
    "AFD_FUND_ADEQUADO",  # % docentes com formação adequada fundamental
]


# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÃO GENÉRICA DE MODELAGEM
# ══════════════════════════════════════════════════════════════════════════════
def rodar_modelo(df, features, alvo, label_alvo, prefixo, classes):
    features = [f for f in features if f in df.columns]
    if alvo not in df.columns:
        print(f"  ⚠️  Coluna {alvo} não encontrada. Pulando.")
        return None

    df_m = df[features + [alvo]].dropna().copy()
    mediana = df_m[alvo].median()
    df_m["TARGET"] = (df_m[alvo] > mediana).astype(int)

    n_total = len(df_m)
    n_pos   = df_m["TARGET"].sum()
    n_neg   = n_total - n_pos

    print(f"\n  Registros: {n_total} | Mediana {label_alvo}: {mediana:.2f}")
    print(f"  Classe 1 ({classes[1]}): {n_pos} | Classe 0 ({classes[0]}): {n_neg}")

    X = df_m[features]
    y = df_m["TARGET"]

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # ── Regressão Logística (baseline) ───────────────────────────────────────
    scaler = StandardScaler()
    log = LogisticRegression(max_iter=1000, random_state=42)
    log.fit(scaler.fit_transform(X_tr), y_tr)
    yp_log  = log.predict(scaler.transform(X_te))
    ypr_log = log.predict_proba(scaler.transform(X_te))[:, 1]
    acc_log = accuracy_score(y_te, yp_log)
    auc_log = roc_auc_score(y_te, ypr_log)
    cv_log  = cross_val_score(log, scaler.fit_transform(X), y,
                               cv=cv, scoring="roc_auc").mean()

    # ── Random Forest ─────────────────────────────────────────────────────────
    rf = RandomForestClassifier(n_estimators=300, max_depth=8,
                                 min_samples_leaf=5, random_state=42, n_jobs=-1)
    rf.fit(X_tr, y_tr)
    yp_rf  = rf.predict(X_te)
    ypr_rf = rf.predict_proba(X_te)[:, 1]
    acc_rf = accuracy_score(y_te, yp_rf)
    auc_rf = roc_auc_score(y_te, ypr_rf)
    cv_rf  = cross_val_score(rf, X, y, cv=cv, scoring="roc_auc").mean()

    print(f"\n  Reg. Logística — Acurácia: {acc_log:.3f} | AUC: {auc_log:.3f} | AUC CV: {cv_log:.3f}")
    print(f"  Random Forest  — Acurácia: {acc_rf:.3f} | AUC: {auc_rf:.3f} | AUC CV: {cv_rf:.3f}")
    print(f"\n  Relatório Random Forest:\n{classification_report(y_te, yp_rf, target_names=classes)}")

    # importância MDI
    imp = pd.Series(rf.feature_importances_, index=features).sort_values(ascending=False)
    print(f"  Importância:\n{imp.round(3)}")

    # ── FIGURA 1: Painel completo (importância + ROC + matrizes) ─────────────
    fig = plt.figure(figsize=(16, 10))
    gs  = gridspec.GridSpec(2, 3, figure=fig,
                             hspace=0.45, wspace=0.35)

    # importância das variáveis
    ax_imp = fig.add_subplot(gs[:, 0])
    imp_plot = imp.copy()
    imp_plot.index = [NOMES.get(i, i) for i in imp_plot.index]
    cores = [RED if v == imp_plot.max() else BLUE for v in imp_plot.sort_values().values]
    imp_plot.sort_values().plot(kind="barh", ax=ax_imp, color=cores, edgecolor="white")
    ax_imp.axvline(x=1/len(features), color=GRAY, linestyle="--",
                    alpha=0.7, linewidth=1, label="Importância uniforme")
    ax_imp.set_xlabel("Importância (MDI)", fontsize=10)
    ax_imp.set_title("Importância das variáveis\n(Random Forest — MDI)", fontsize=11)
    ax_imp.legend(fontsize=9)
    for spine in ["top", "right"]:
        ax_imp.spines[spine].set_visible(False)

    # curva ROC
    ax_roc = fig.add_subplot(gs[0, 1])
    RocCurveDisplay.from_predictions(
        y_te, ypr_log, ax=ax_roc,
        name=f"Reg. Logística (AUC={auc_log:.3f}, CV={cv_log:.3f})",
        color=BLUE, linewidth=1.8
    )
    RocCurveDisplay.from_predictions(
        y_te, ypr_rf, ax=ax_roc,
        name=f"Random Forest (AUC={auc_rf:.3f}, CV={cv_rf:.3f})",
        color=RED, linewidth=1.8
    )
    ax_roc.plot([0, 1], [0, 1], "k--", alpha=0.4, linewidth=1, label="Aleatório")
    ax_roc.set_title("Curva ROC", fontsize=11)
    ax_roc.legend(fontsize=8.5)
    for spine in ["top", "right"]:
        ax_roc.spines[spine].set_visible(False)

    # matrizes de confusão
    for col_idx, (modelo_pred, modelo_nome, cor_cmap) in enumerate([
        (yp_log, f"Reg. Logística\nAcurácia={acc_log:.3f}", "Blues"),
        (yp_rf,  f"Random Forest\nAcurácia={acc_rf:.3f}",   "Reds"),
    ], start=1):
        ax_cm = fig.add_subplot(gs[1, col_idx])
        cm = confusion_matrix(y_te, modelo_pred)
        cm_pct = cm.astype(float) / cm.sum(axis=1, keepdims=True) * 100
        sns.heatmap(cm, annot=False, fmt="d", cmap=cor_cmap,
                    ax=ax_cm, linewidths=0.5, cbar=False)
        for i in range(2):
            for j in range(2):
                ax_cm.text(j + 0.5, i + 0.35, str(cm[i, j]),
                           ha="center", va="center", fontsize=13, fontweight="bold",
                           color="white" if cm[i, j] > cm.max()*0.6 else "black")
                ax_cm.text(j + 0.5, i + 0.65, f"({cm_pct[i, j]:.1f}%)",
                           ha="center", va="center", fontsize=9, color="gray")
        ax_cm.set_xticklabels(classes, fontsize=9)
        ax_cm.set_yticklabels(classes, fontsize=9, rotation=0)
        ax_cm.set_xlabel("Predito", fontsize=10)
        ax_cm.set_ylabel("Real", fontsize=10)
        ax_cm.set_title(modelo_nome, fontsize=10)

    # tabela de métricas
    ax_tab = fig.add_subplot(gs[0, 2])
    ax_tab.axis("off")
    tabela_dados = [
        ["Modelo",         "Acurácia", "AUC\n(teste)", "AUC\n(CV k=5)"],
        ["Reg. Logística", f"{acc_log:.3f}", f"{auc_log:.3f}", f"{cv_log:.3f}"],
        ["Random Forest",  f"{acc_rf:.3f}",  f"{auc_rf:.3f}",  f"{cv_rf:.3f}"],
    ]
    tb = ax_tab.table(
        cellText=tabela_dados[1:],
        colLabels=tabela_dados[0],
        cellLoc="center",
        loc="center",
        bbox=[0, 0.3, 1, 0.5]
    )
    tb.auto_set_font_size(False)
    tb.set_fontsize(10)
    for (row, col), cell in tb.get_celld().items():
        cell.set_edgecolor("#cccccc")
        if row == 0:
            cell.set_facecolor("#2166ac")
            cell.set_text_props(color="white", fontweight="bold")
        elif row == 2:  # Random Forest
            cell.set_facecolor("#fef0d9")
        else:
            cell.set_facecolor("#f7f7f7")
    ax_tab.set_title("Métricas comparativas", fontsize=11, fontweight="bold", pad=10)

    fig.suptitle(
        f"Classificação de {label_alvo} — {SIGLA}\n"
        f"n = {n_total} observações | {len(features)} variáveis preditoras",
        fontsize=13, fontweight="bold", y=1.01
    )
    fonte("Fonte: INEP (Censo Escolar, IDEB, SAEB, INSE), SIOPE/FNDE, IBGE. "
          "Divisão treino/teste: 80/20, estratificada. Random Forest: 300 árvores, profundidade máxima 8.")
    salvar(f"{prefixo}_painel_completo")

    # ── FIGURA 2: Importância com intervalo de confiança (permutation) ────────
    print("  Calculando importância por permutação...")
    perm = permutation_importance(rf, X_te, y_te, n_repeats=20,
                                   random_state=42, scoring="roc_auc")
    perm_mean = pd.Series(perm.importances_mean, index=features)
    perm_std  = pd.Series(perm.importances_std,  index=features)
    ordem = perm_mean.sort_values()

    fig, ax = plt.subplots(figsize=(9, 6))
    y_pos = range(len(ordem))
    ax.barh(y_pos, ordem.values, xerr=perm_std[ordem.index].values,
            color=[RED if v == ordem.max() else BLUE for v in ordem.values],
            edgecolor="white", capsize=3, error_kw={"elinewidth": 1.2, "ecolor": GRAY})
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels([NOMES.get(c, c) for c in ordem.index], fontsize=10)
    ax.axvline(x=0, color=GRAY, linewidth=1)
    ax.set_xlabel("Redução de AUC-ROC por permutação (média ± DP, n=20)", fontsize=10)
    ax.set_title(f"Importância por permutação — {label_alvo} — {SIGLA}", fontsize=12)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    fonte("Importância por permutação: redução de AUC-ROC ao embaralhar aleatoriamente cada variável no conjunto de teste.")
    salvar(f"{prefixo}_importancia_permutacao")

    return {
        "acc_log": acc_log, "auc_log": auc_log, "cv_log": cv_log,
        "acc_rf":  acc_rf,  "auc_rf":  auc_rf,  "cv_rf":  cv_rf,
        "imp_mdi": imp, "perm_mean": perm_mean,
        "n": n_total, "mediana": mediana,
        "features": features,
    }


# ══════════════════════════════════════════════════════════════════════════════
# MODELO 1 — ABANDONO ESCOLAR NO ENSINO MÉDIO
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print(f"MODELO 1 — Classificação de abandono escolar ({SIGLA})")
print("="*60)

res1 = rodar_modelo(
    df=df,
    features=FEATURES_BASE,
    alvo="ABANDONO_MED_TOTAL",
    label_alvo="Abandono no Ensino Médio",
    prefixo="M1_abandono",
    classes=["Baixo abandono", "Alto abandono"],
)


# ══════════════════════════════════════════════════════════════════════════════
# MODELO 2 — DESEMPENHO SAEB EM MATEMÁTICA
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print(f"MODELO 2 — Classificação de desempenho SAEB EM MT ({SIGLA})")
print("="*60)

res2 = rodar_modelo(
    df=df,
    features=FEATURES_BASE,
    alvo="SAEB_12_MT",
    label_alvo="Desempenho SAEB EM Matemática",
    prefixo="M2_saeb_mt",
    classes=["Baixo desempenho", "Alto desempenho"],
)


# ══════════════════════════════════════════════════════════════════════════════
# MODELO 3 — DESEMPENHO ENEM (se disponível)
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print(f"MODELO 3 — Classificação de desempenho ENEM ({SIGLA})")
print("="*60)

res3 = rodar_modelo(
    df=df,
    features=FEATURES_BASE,
    alvo="ENEM_MEDIA_GERAL",
    label_alvo="Desempenho ENEM (média geral)",
    prefixo="M3_enem",
    classes=["Baixo desempenho", "Alto desempenho"],
)


# ══════════════════════════════════════════════════════════════════════════════
# MODELO 4 — ABANDONO COM FEATURES ESTENDIDAS (TDI + AFD)
# Mesmo objetivo do Modelo 1, mas com distorção e adequação docente como preditores
# Permite avaliar se TDI e AFD aumentam o poder preditivo sobre abandono
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print(f"MODELO 4 — Abandono com TDI + AFD ({SIGLA})")
print("="*60)

features_ext_disp = [f for f in FEATURES_EXTENDED if f in df.columns]
n_novas = len(features_ext_disp) - len([f for f in FEATURES_BASE if f in df.columns])
if n_novas > 0:
    print(f"  Features adicionais disponíveis: {n_novas} (TDI/AFD)")
    res4 = rodar_modelo(
        df=df,
        features=FEATURES_EXTENDED,
        alvo="ABANDONO_MED_TOTAL",
        label_alvo="Abandono EM — features estendidas",
        prefixo="M4_abandono_ext",
        classes=["Baixo abandono", "Alto abandono"],
    )
else:
    print("  ⚠️  TDI/AFD não disponíveis no master. Execute extrair_tdi_afd.py e integrar_tdi_afd.py primeiro.")
    res4 = None


# ══════════════════════════════════════════════════════════════════════════════
# FIGURA COMPARATIVA — IMPORTÂNCIA NOS TRÊS MODELOS
# ══════════════════════════════════════════════════════════════════════════════
resultados = {k: v for k, v in {
    "Abandono\nEnsino Médio": res1,
    "Desempenho\nSAEB MT":    res2,
    "Desempenho\nENEM":       res3,
    "Abandono EM\n+ TDI/AFD": res4,
}.items() if v is not None}

if len(resultados) >= 2:
    print("\n── Figura comparativa de importância ──")
    features_comuns = FEATURES_BASE.copy()

    n_cols = len(resultados)
    fig, axes = plt.subplots(1, n_cols, figsize=(6*n_cols, 7),
                              sharey=False)
    if n_cols == 1:
        axes = [axes]

    cores_modelos = [BLUE, RED, GREEN, ORANGE]
    for ax, (titulo, res), cor in zip(axes, resultados.items(), cores_modelos):
        imp = res["imp_mdi"]
        feat_disp = [f for f in features_comuns if f in imp.index]
        imp_disp = imp[feat_disp].sort_values()
        labels = [NOMES.get(c, c) for c in imp_disp.index]

        ax.barh(range(len(imp_disp)), imp_disp.values,
                color=[RED if v == imp_disp.max() else cor for v in imp_disp.values],
                edgecolor="white")
        ax.set_yticks(range(len(imp_disp)))
        ax.set_yticklabels(labels, fontsize=9)
        ax.axvline(x=1/len(feat_disp), color=GRAY, linestyle="--",
                    alpha=0.6, linewidth=1)
        ax.set_xlabel("Importância (MDI)", fontsize=10)
        ax.set_title(
            f"{titulo}\nAUC={res['auc_rf']:.3f} (CV={res['cv_rf']:.3f})",
            fontsize=11, fontweight="bold"
        )
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)

    fig.suptitle(
        f"Comparação da importância das variáveis entre modelos — {SIGLA}",
        fontsize=13, fontweight="bold", y=1.02
    )
    fonte("MDI = Mean Decrease in Impurity (Random Forest, 300 árvores). "
          "Linha tracejada = importância uniforme (1/n variáveis).")
    salvar("MX_comparacao_importancia_modelos")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURA COMPARATIVA — MÉTRICAS LADO A LADO
# ══════════════════════════════════════════════════════════════════════════════
if len(resultados) >= 2:
    print("\n── Figura comparativa de métricas ──")

    modelos_nomes = list(resultados.keys())
    metricas = {
        "AUC-ROC\n(teste)":  [r["auc_rf"]  for r in resultados.values()],
        "AUC-ROC\n(CV k=5)": [r["cv_rf"]   for r in resultados.values()],
        "Acurácia\n(teste)":  [r["acc_rf"]  for r in resultados.values()],
    }
    metricas_log = {
        "AUC-ROC\n(teste)":  [r["auc_log"] for r in resultados.values()],
        "AUC-ROC\n(CV k=5)": [r["cv_log"]  for r in resultados.values()],
        "Acurácia\n(teste)":  [r["acc_log"] for r in resultados.values()],
    }

    x = np.arange(len(modelos_nomes))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 5))
    for i, (met, vals) in enumerate(metricas.items()):
        bars = ax.bar(x + i*width, vals, width, label=f"RF — {met}",
                      color=cores_modelos[i], alpha=0.85, edgecolor="white")
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                    f"{bar.get_height():.3f}", ha="center", va="bottom", fontsize=8.5)

    ax.axhline(y=0.5, color=GRAY, linestyle="--", alpha=0.5, linewidth=1,
                label="AUC = 0.5 (aleatório)")
    ax.set_xticks(x + width)
    ax.set_xticklabels(modelos_nomes, fontsize=10)
    ax.set_ylim(0.4, 1.0)
    ax.set_ylabel("Valor da métrica", fontsize=11)
    ax.set_title(f"Desempenho comparativo dos modelos Random Forest — {SIGLA}",
                  fontsize=12, fontweight="bold")
    ax.legend(fontsize=9, ncol=2)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    fonte("Random Forest: 300 árvores, profundidade máxima 8, mínimo de 5 observações por folha. "
          "Divisão treino/teste 80/20, estratificada. Validação cruzada: StratifiedKFold k=5.")
    salvar("MX_metricas_comparativas")

# ══════════════════════════════════════════════════════════════════════════════
# RESUMO FINAL NO TERMINAL
# ══════════════════════════════════════════════════════════════════════════════
# ── Nota comparativa M1 vs M4 ──────────────────────────────────────────────
if res1 is not None and res4 is not None:
    delta_auc  = res4["auc_rf"]  - res1["auc_rf"]
    delta_cv   = res4["cv_rf"]   - res1["cv_rf"]
    delta_acc  = res4["acc_rf"]  - res1["acc_rf"]
    print(f"\n── Ganho do Modelo 4 vs Modelo 1 (TDI + AFD) ──")
    print(f"  ΔAUC-ROC (teste):  {delta_auc:+.3f}")
    print(f"  ΔAUC-ROC (CV):     {delta_cv:+.3f}")
    print(f"  ΔAcurácia:         {delta_acc:+.3f}")
    if delta_auc > 0.01:
        print(f"  → TDI/AFD melhoram o modelo de abandono.")
    elif delta_auc < -0.01:
        print(f"  → TDI/AFD reduzem o poder preditivo.")
    else:
        print(f"  → TDI/AFD não alteram significativamente o modelo.")

print(f"\n{'='*60}")
print(f"RESUMO COMPARATIVO — {SIGLA}")
print(f"{'='*60}")

nomes_modelos = {
    "Abandono\nEnsino Médio": "Modelo 1 — Abandono EM (base)",
    "Desempenho\nSAEB MT":    "Modelo 2 — Desempenho SAEB MT",
    "Desempenho\nENEM":       "Modelo 3 — Desempenho ENEM",
    "Abandono EM\n+ TDI/AFD": "Modelo 4 — Abandono EM + TDI/AFD",
}
for titulo, res in resultados.items():
    nome = nomes_modelos.get(titulo, titulo)
    print(f"\n{nome} (n={res['n']}):")
    print(f"  Reg. Logística — Acurácia={res['acc_log']:.3f} | AUC={res['auc_log']:.3f} | AUC CV={res['cv_log']:.3f}")
    print(f"  Random Forest  — Acurácia={res['acc_rf']:.3f}  | AUC={res['auc_rf']:.3f}  | AUC CV={res['cv_rf']:.3f}")
    print(f"  Top 3 variáveis: {', '.join([NOMES.get(c, c) for c in res['imp_mdi'].head(3).index])}")

print(f"\n✓ Gráficos salvos em: {PASTA_GRAF}")