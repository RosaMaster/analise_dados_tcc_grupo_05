import os
import zipfile
import shutil
import pandas as pd
from pathlib import Path

# ─── CONFIGURAÇÃO ────────────────────────────────────────────────────────────
PASTA_ZIPS  = r"/mnt/c/Users/User/Documents/TCC_UNIVESP/Data/Censo_escolar/"
PASTA_SAIDA = r"/mnt/c/Users/User/Documents/TCC_UNIVESP/Output/Censo_Escolar"
# ─────────────────────────────────────────────────────────────────────────────


def extrair_todos_os_zips(pasta_zips, pasta_saida):
    pasta_zips  = Path(pasta_zips)
    pasta_saida = Path(pasta_saida)
    pasta_saida.mkdir(parents=True, exist_ok=True)

    zips = sorted(pasta_zips.glob("microdados_censo_escolar_*.zip"))

    if not zips:
        print(f"Nenhum ZIP encontrado em: {pasta_zips}")
        return

    print(f"Encontrados {len(zips)} arquivos ZIP.\n")

    for zip_path in zips:
        ano = zip_path.stem.replace("microdados_censo_escolar_", "").strip("_")
        pasta_ano = pasta_saida / ano
        pasta_ano.mkdir(parents=True, exist_ok=True)

        print(f"[{ano}] Abrindo {zip_path.name}...")

        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                for info in zip_ref.infolist():

                    # corrige encoding corrompido (problema do ZIP 2022)
                    try:
                        nome = info.filename.encode("cp437").decode("latin-1")
                    except Exception:
                        nome = info.filename

                    nome_arquivo = Path(nome).name.lower()

                    if not nome_arquivo.endswith(".csv"):
                        continue
                    if "md5" in nome_arquivo or "suplemento" in nome_arquivo:
                        continue

                    partes = nome.replace("\\", "/").split("/")
                    partes_lower = [p.lower().strip() for p in partes]
                    if "dados" not in partes_lower:
                        continue

                    # força nome do arquivo em minúsculo
                    destino = pasta_ano / nome_arquivo

                    if destino.exists():
                        print(f"  ✓  {nome_arquivo} já existe, pulando.")
                        continue

                    print(f"  → Extraindo {nome_arquivo}...")

                    # tentativa 1: abre pelo info original
                    sucesso = False
                    try:
                        with zip_ref.open(info) as src, open(destino, "wb") as dst:
                            dst.write(src.read())
                        sucesso = True
                    except Exception:
                        pass

                    # tentativa 2: abre pelo nome decodificado
                    if not sucesso:
                        try:
                            with zip_ref.open(nome) as src, open(destino, "wb") as dst:
                                dst.write(src.read())
                            sucesso = True
                        except Exception:
                            pass

                    # tentativa 3: extrai para pasta temporária e move
                    if not sucesso:
                        try:
                            pasta_tmp = pasta_ano / "_tmp_extract"
                            pasta_tmp.mkdir(exist_ok=True)
                            zip_ref.extract(info, pasta_tmp)
                            # procura o csv extraído
                            extraidos = list(pasta_tmp.rglob("*.csv")) + list(pasta_tmp.rglob("*.CSV"))
                            if extraidos:
                                shutil.move(str(extraidos[0]), str(destino))
                                sucesso = True
                            # limpa pasta temporária
                            shutil.rmtree(pasta_tmp, ignore_errors=True)
                        except Exception as e3:
                            print(f"  ✗  Todas as tentativas falharam: {e3}")

                    if sucesso:
                        print(f"  ✓  Salvo em {destino}")

        except Exception as e:
            print(f"  ✗  Erro ao processar {zip_path.name}: {e}")

    print("\nExtração concluída!\n")


def montar_dataframe(pasta_saida, filtro_nome):
    """
    Percorre todas as subpastas de ano, carrega os CSVs que contenham
    filtro_nome no nome, adiciona coluna ANO_CENSO e concatena tudo.
    """
    pasta_saida = Path(pasta_saida)
    dfs = []

    pastas_ano = sorted([p for p in pasta_saida.iterdir() if p.is_dir()])

    for pasta_ano in pastas_ano:
        ano = pasta_ano.name
        csvs = [f for f in pasta_ano.glob("*.csv") if filtro_nome.lower() in f.name.lower()]

        if not csvs:
            print(f"  [{ano}] nenhum arquivo com '{filtro_nome}' encontrado, pulando.")
            continue

        for csv_path in csvs:
            print(f"  [{ano}] Carregando {csv_path.name}...")
            try:
                df = pd.read_csv(
                    csv_path,
                    sep=";",
                    encoding="latin-1",
                    low_memory=False
                )
                df["ANO_CENSO"] = int(ano[:4])
                dfs.append(df)
                print(f"         {len(df):,} linhas carregadas.")
            except Exception as e:
                print(f"         ✗ Erro: {e}")

    if not dfs:
        print(f"Nenhum dado carregado para '{filtro_nome}'.\n")
        return pd.DataFrame()

    print(f"\nConcatenando {len(dfs)} arquivos...")
    df_final = pd.concat(dfs, ignore_index=True, sort=False)
    print(f"Total de linhas: {len(df_final):,}")
    print(f"Total de colunas: {len(df_final.columns)}\n")
    return df_final


# ─── EXECUÇÃO ────────────────────────────────────────────────────────────────
if __name__ == "__main__":

    # PASSO 1: extrai todos os ZIPs
    extrair_todos_os_zips(PASTA_ZIPS, PASTA_SAIDA)