"""
Orquestrador multi-estado — roda o pipeline completo para cada UF
sem alterar nenhum script existente.

Funcionamento:
  1. Para cada estado, sobrescreve UF_COD no config.py
  2. Executa cada script do pipeline em sequência
  3. Restaura o config.py original ao final
"""

import subprocess
import sys
import shutil
import re
from pathlib import Path

# ─── CONFIGURAÇÃO ─────────────────────────────────────────────────────────────
PASTA_SCRIPTS = Path("/mnt/c/Users/lucas/Documents/TCC_UNIVESP/oficial_scripts")
CONFIG_PATH   = PASTA_SCRIPTS / "config.py"

ESTADOS = {
    35: "SP",
    23: "CE",
    27: "AL",
    43: "RS",
}

SCRIPTS = [
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
    "011_MontarMaster.py",
    "010_ENEM_Extrair.py",
    "010_ENEM_Preparar.py",
    "012_TDI_AFD_Extrair.py",
    "012_TDI_AFD_Preparar.py",
    "013_Analise_Exploratoria.py",
    "014_Modelos_Preditivos.py",
]

# scripts que podem ser pulados se o arquivo de entrada não existir
# (útil para bases que só têm dados de alguns estados)
# OPCIONAIS = {
#     "010_ENEM_Extrair.py",
#     "010_ENEM_Preparar.py",
# }
# ─────────────────────────────────────────────────────────────────────────────


def ler_config():
    """Lê o conteúdo atual do config.py."""
    return CONFIG_PATH.read_text(encoding="utf-8")


def salvar_config(conteudo):
    """Salva conteúdo no config.py."""
    CONFIG_PATH.write_text(conteudo, encoding="utf-8")


def trocar_uf(conteudo, uf_cod):
    """Substitui o UF_COD no config.py."""
    return re.sub(r"^UF_COD\s*=\s*\d+", f"UF_COD = {uf_cod}", conteudo, flags=re.MULTILINE)


def rodar_script(script_path, uf_cod, sigla):
    """Executa um script Python e retorna True se sucesso."""
    print(f"    → {script_path.name}", end=" ", flush=True)
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        cwd=str(PASTA_SCRIPTS),
    )
    if result.returncode == 0:
        print("✓")
        return True
    else:
        print("✗")
        print(f"      ERRO:\n{result.stderr[-500:]}")
        return False


# ─── EXECUÇÃO ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":

    print("=" * 60)
    print("PIPELINE MULTI-ESTADO")
    print(f"Estados: {list(ESTADOS.values())}")
    print(f"Scripts: {len(SCRIPTS)}")
    print("=" * 60)

    # faz backup do config.py original
    config_backup = ler_config()
    uf_original   = re.search(r"^UF_COD\s*=\s*(\d+)", config_backup, re.MULTILINE).group(1)

    resultados = {}

    try:
        for uf_cod, sigla in ESTADOS.items():
            print(f"\n{'─'*60}")
            print(f"  ESTADO: {sigla} (UF_COD={uf_cod})")
            print(f"{'─'*60}")

            # atualiza config.py para este estado
            novo_config = trocar_uf(config_backup, uf_cod)
            salvar_config(novo_config)

            erros = []
            for nome_script in SCRIPTS:
                script_path = PASTA_SCRIPTS / nome_script
                if not script_path.exists():
                    print(f"    → {nome_script} ⚠️  não encontrado, pulando")
                    continue

                ok = rodar_script(script_path, uf_cod, sigla)
                if not ok:
                    erros.append(nome_script)
                    if nome_script not in OPCIONAIS:
                        print(f"      ⚠️  Erro em script obrigatório — continuando mesmo assim")

            resultados[sigla] = erros
            print(f"\n  {sigla} concluído — {len(erros)} erro(s)")

    finally:
        # restaura config.py original sempre, mesmo se der erro
        salvar_config(config_backup)
        print(f"\n✓ config.py restaurado para UF_COD = {uf_original}")

    # ── Resumo final ──────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("RESUMO FINAL")
    print(f"{'='*60}")
    for sigla, erros in resultados.items():
        status = "✓ OK" if not erros else f"✗ {len(erros)} erro(s)"
        print(f"  {sigla:<4} {status}")
        for e in erros:
            print(f"       → {e}")