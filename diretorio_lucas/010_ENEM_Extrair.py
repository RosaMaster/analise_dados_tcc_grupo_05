import zipfile
import pandas as pd
from pathlib import Path
from config import UF_COD, PASTA_ENEM, PASTA_DATA

Path(PASTA_ENEM).mkdir(parents=True, exist_ok=True)  # cria a pasta se não existir
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

ANOS        = [2019, 2020, 2021, 2022, 2023, 2024]
SAIDA_BRUTO = Path(PASTA_ENEM) / f"enem_bruto_{SIGLA.lower()}.csv"
CHUNK_SIZE  = 100_000  # linhas por chunk — ajuste se der erro de memória

# colunas que queremos extrair (comuns a todos os anos)
COLUNAS_INTERESSE = [
    "NU_ANO",
    "CO_MUNICIPIO_ESC",   # município da escola do participante
    "NO_MUNICIPIO_ESC",
    "CO_UF_ESC",
    "SG_UF_ESC",
    "TP_DEPENDENCIA_ADM_ESC",  # rede: 1=fed, 2=est, 3=mun, 4=priv
    "TP_LOCALIZACAO_ESC",      # 1=urbana, 2=rural
    "TP_ST_CONCLUSAO",         # 1=já concluiu EM, 2=cursando, 3=cursará
    "IN_TREINEIRO",            # 1=treineiro (não incluir nas médias)
    "TP_PRESENCA_CN",
    "TP_PRESENCA_CH",
    "TP_PRESENCA_LC",
    "TP_PRESENCA_MT",
    "NU_NOTA_CN",    # Ciências da Natureza
    "NU_NOTA_CH",    # Ciências Humanas
    "NU_NOTA_LC",    # Linguagens e Códigos
    "NU_NOTA_MT",    # Matemática
    "NU_NOTA_REDACAO",
]
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print(f"ENEM EXTRAÇÃO — Estado: {SIGLA} (código {UF_COD})")
print("=" * 60)


def processar_chunk(chunk, sigla):
    """Filtra e prepara um chunk de dados."""
    # filtra pelo estado da escola
    if "SG_UF_ESC" in chunk.columns:
        chunk = chunk[chunk["SG_UF_ESC"] == sigla].copy()
    elif "CO_UF_ESC" in chunk.columns:
        chunk = chunk[chunk["CO_UF_ESC"] == UF_COD].copy()

    if chunk.empty:
        return chunk

    # remove treineiros (alunos que fazem o ENEM sem ter concluído o EM)
    if "IN_TREINEIRO" in chunk.columns:
        chunk = chunk[chunk["IN_TREINEIRO"] == 0].copy()

    # mantém só quem concluiu ou está concluindo o EM (TP_ST_CONCLUSAO 1 ou 2)
    if "TP_ST_CONCLUSAO" in chunk.columns:
        chunk = chunk[chunk["TP_ST_CONCLUSAO"].isin([1, 2])].copy()

    # filtra só presentes em todas as provas
    for col in ["TP_PRESENCA_CN", "TP_PRESENCA_CH", "TP_PRESENCA_LC", "TP_PRESENCA_MT"]:
        if col in chunk.columns:
            chunk = chunk[chunk[col] == 1].copy()

    return chunk


def extrair_csv_do_zip(zip_path, arquivo_interno, sigla):
    """Lê um CSV grande em chunks direto do ZIP."""
    chunks_filtrados = []
    total_lido = 0
    total_filtrado = 0

    with zipfile.ZipFile(zip_path, "r") as z:
        with z.open(arquivo_interno) as f:
            for chunk in pd.read_csv(
                f,
                sep=";",
                encoding="latin-1",
                low_memory=False,
                chunksize=CHUNK_SIZE,
                usecols=lambda c: c in COLUNAS_INTERESSE,
            ):
                total_lido += len(chunk)
                chunk_filtrado = processar_chunk(chunk, sigla)
                if not chunk_filtrado.empty:
                    chunks_filtrados.append(chunk_filtrado)
                    total_filtrado += len(chunk_filtrado)

                print(f"    lido: {total_lido:,} | filtrado: {total_filtrado:,}", end="\r")

    print()
    if chunks_filtrados:
        return pd.concat(chunks_filtrados, ignore_index=True)
    return pd.DataFrame()


# ─── LOOP POR ANO ─────────────────────────────────────────────────────────────
todos = []

for ano in ANOS:
    zip_path = Path(PASTA_DATA) / "Enem" / f"microdados_enem_{ano}.zip"

    if not zip_path.exists():
        print(f"\n[{ano}] ✗ Arquivo não encontrado: {zip_path}")
        continue

    print(f"\n[{ano}] Processando {zip_path.name}...")

    try:
        if ano == 2024:
            # 2024 tem arquivo de resultados separado
            arquivo = "DADOS/RESULTADOS_2024.csv"
        else:
            arquivo = f"DADOS/MICRODADOS_ENEM_{ano}.csv"

        df_ano = extrair_csv_do_zip(zip_path, arquivo, SIGLA)

        if df_ano.empty:
            print(f"  ✗ Nenhum dado de {SIGLA} encontrado")
            continue

        df_ano["ANO"] = ano
        todos.append(df_ano)
        print(f"  ✓ {len(df_ano):,} participantes de {SIGLA}")

    except Exception as e:
        print(f"  ✗ Erro: {e}")

# ─── CONSOLIDA E SALVA BRUTO ──────────────────────────────────────────────────
if not todos:
    print("\n✗ Nenhum dado coletado.")
    exit()

df_bruto = pd.concat(todos, ignore_index=True)
print(f"\nTotal bruto: {len(df_bruto):,} participantes")
print(f"Anos: {sorted(df_bruto['ANO'].unique())}")

df_bruto.to_csv(SAIDA_BRUTO, sep=";", index=False, encoding="utf-8-sig")
print(f"\n✓ Dados brutos salvos em: {SAIDA_BRUTO}")
print("Execute o script de preparação para agregar por município.")