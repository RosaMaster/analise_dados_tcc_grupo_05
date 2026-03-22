import requests
import pandas as pd
import time
from pathlib import Path
from config import UF_COD, PASTA_SAIDA, PASTA_SIOPE

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

ANOS  = [2019, 2020, 2021, 2022, 2023, 2024]

# arquivo intermediário com dados brutos
SAIDA_BRUTO = Path(PASTA_SIOPE) / f"siope_bruto_{SIGLA.lower()}.csv"
Path(PASTA_SIOPE).mkdir(parents=True, exist_ok=True)  # cria a pasta se não existir

BASE_URL = (
    "https://www.fnde.gov.br/olinda-ide/servico/DADOS_ABERTOS_SIOPE/versao/v1/odata/"
    "Dados_Gerais_Siope(Ano_Consulta=@Ano_Consulta,Num_Peri=@Num_Peri,Sig_UF=@Sig_UF)"
    "?@Ano_Consulta={ano}&@Num_Peri=6&@Sig_UF='{uf}'"
    "&$top=10000&$format=json"
)
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print(f"SIOPE EXTRAÇÃO — Estado: {SIGLA} (código {UF_COD})")
print("=" * 60)

todos = []

for ano in ANOS:
    url = BASE_URL.format(ano=ano, uf=SIGLA)
    print(f"[{ano}] Buscando... ", end="", flush=True)

    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        dados = r.json().get("value", [])

        if not dados:
            url2 = BASE_URL.replace("Num_Peri=6", "Num_Peri=5").format(ano=ano, uf=SIGLA)
            r2 = requests.get(url2, timeout=60)
            dados = r2.json().get("value", [])

        if dados:
            df_ano = pd.DataFrame(dados)
            if "TIPO" in df_ano.columns:
                df_ano = df_ano[df_ano["TIPO"] == "Municipal"]
            todos.append(df_ano)
            print(f"✓ {len(df_ano)} municípios")
        else:
            print("✗ Nenhum dado retornado")

    except Exception as e:
        print(f"✗ Erro: {e}")

    time.sleep(1)

if not todos:
    print("Nenhum dado coletado.")
else:
    df_bruto = pd.concat(todos, ignore_index=True)
    df_bruto.to_csv(SAIDA_BRUTO, sep=";", index=False, encoding="utf-8-sig")
    print(f"\n✓ Dados brutos salvos em: {SAIDA_BRUTO}")
    print(f"  {len(df_bruto)} registros | colunas: {list(df_bruto.columns)}")