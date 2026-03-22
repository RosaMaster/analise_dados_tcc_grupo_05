import subprocess
import sys
import os

# ─── VETORES DE SCRIPTS ───────────────────────────────────────────────────────
SCRIPTS_EXTRACAO = [
    "001_CensoEscolar_Extrair.py",
    "003_SIOPE_Extrair.py",
    "004_IDEB_Extrair.py",
    "005_BolsaFamilia_Extrair.py",
    "006_IBGE_Alfabetizacao.py",
    "007_Rendimento_Extrair.py",
    "008_PIB_Percapita.py",
    "009_SAEB_Extrair.py",
    "010_ENEM_Extrair.py",
    "012_TDI_AFD_Extrair.py",
]

SCRIPTS_COMPLETO = [
    "001_CensoEscolar_Extrair.py",
    "002_CensoEscolar_Preparar.py",
    "003_SIOPE_Extrair.py",
    "003_SIOPE_Preparar.py",
    "004_IDEB_Extrair.py",
    "004_IDEB_Preparar.py",
    "005_BolsaFamilia_Extrair.py",
    "005_BolsaFamilia_Preparar.py",
    "006_IBGE_Alfabetizacao.py",
    "007_Rendimento_Extrair.py",
    "008_PIB_Percapita.py",
    "009_SAEB_Extrair.py",
    "010_ENEM_Extrair.py",
    "010_ENEM_Preparar.py",
    "011_MontarMaster.py",
    "012_TDI_AFD_Extrair.py",
    "012_TDI_AFD_Preparar.py",
    "013_Analise_Exploratoria.py",
    "014_Modelos_Preditivos.py",
]
# ─────────────────────────────────────────────────────────────────────────────

# ─── MODO ─────────────────────────────────────────────────────────────────────
MODO    = sys.argv[1] if len(sys.argv) > 1 else "completo"
SCRIPTS = SCRIPTS_EXTRACAO if MODO == "extrair" else SCRIPTS_COMPLETO

PASTA_SCRIPTS = os.path.dirname(os.path.abspath(__file__))
# ─────────────────────────────────────────────────────────────────────────────


def rodar_script(nome):
    caminho = os.path.join(PASTA_SCRIPTS, nome)
    if not os.path.exists(caminho):
        print(f"  ✗  Arquivo não encontrado: {caminho}")
        return False
    print(f"\n{'='*60}")
    print(f"  Executando: {nome}")
    print(f"{'='*60}")
    resultado = subprocess.run(
        [sys.executable, caminho],
        cwd=PASTA_SCRIPTS
    )
    if resultado.returncode == 0:
        print(f"\n  ✓  {nome} concluído com sucesso.")
        return True
    else:
        print(f"\n  ✗  {nome} encerrou com erro (código {resultado.returncode}).")
        return False


if __name__ == "__main__":
    titulo = "APENAS EXTRAÇÕES" if MODO == "extrair" else "EXECUÇÃO COMPLETA"
    print("╔══════════════════════════════════════════════════════════╗")
    print(f"║         PIPELINE TCC — {titulo:<34}║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"  Modo    : {MODO}")
    print(f"  Scripts : {len(SCRIPTS)}")
    print(f"  Uso     : python 000_Pipeline.py           → completo")
    print(f"            python 000_Pipeline.py extrair   → só extração")

    sucesso = 0
    falha   = 0

    for script in SCRIPTS:
        ok = rodar_script(script)
        if ok:
            sucesso += 1
        else:
            falha += 1

    print(f"\n{'='*60}")
    print(f"PIPELINE CONCLUÍDO — {sucesso} scripts OK | {falha} com erro")
    print(f"{'='*60}")
