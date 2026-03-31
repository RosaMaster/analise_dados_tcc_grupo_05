# TRABALHO DE CONCLUSÃO DE CURSO EM CIÊNCIA DE DADOS
### Grupo: BCD - TCC530 - A2026S1N3 - GRUPO 5
#### Tema: Determinantes do Abandono Escolar e do Desempenho Acadêmico nos Municípios do Estado de São Paulo: uma Análise Exploratória e Preditiva com Dados Públicos (2019 - 2024)

---

Repositório para armazenamento de dados e analise de dados do TCC Científico do __BCD - TCC530 - A2026S1N3 - GRUPO 5__.

### FICHA TÉCNICA

> LINGUAGEM: [**`python v3.14.3`**](https://www.python.org/downloads/release/python-3143/)
>> FOMARTO: **`csv`** -> **`parquet`** -> **`view`**
>
>> BIBLIOTECAS (LIB's)
>>> LEITURA (EXTRACT) | TRANFORMAÇÃO (TRANSFORM) | CARREGAMENTO (LOAD): [**`Polars`**](https://pola.rs/)
>>> OUTRO: [pathlib](https://docs.python.org/3/library/pathlib.html)

<br><br>

### LIB's Python

#### ETL

| __Bibliotecas__                                                       | __Descrição__                                                                                                                                                                                                                                |
| --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Dask](https://docs.dask.org/en/stable/)                              | Dask é uma biblioteca Python para computação paralela e distribuída                                                                                                                                                                          |
| [DuckDB](https://duckdb.org/docs/stable/)                             | É um banco de dados analítico que roda "dentro" do seu script Python. Ele é fenomenal para ler CSVs gigantes e já salvar em Parquet usando SQL ou comandos simples. Ele não carrega tudo na RAM de uma vez (streaming)                       |
| [Modin](https://modin.readthedocs.io/en/stable/)                      | Uma biblioteca que atua como um "acelerador" do Pandas. Você muda apenas uma linha de código (import modin.pandas as pd) e ele distribui o processamento em todos os núcleos do seu processador automaticamente usando Ray ou Dask por baixo |
| [Pandas](https://pandas.pydata.org/docs/)                             | Pandas é uma biblioteca de código aberto, licenciada sob a licença BSD, que fornece estruturas de dados de alto desempenho e ferramentas de análise de dados fáceis de usar para a linguagem de programação Python                           |
| [Polars](https://pola.rs/)                                            | Polars é uma biblioteca DataFrame extremamente rápida para manipulação de dados estruturados. O núcleo é escrito em Rust e está disponível para Python, R e NodeJS                                                                           |
| [PySpark](https://spark.apache.org/docs/latest/api/python/index.html) | PySpark é a API Python para Apache Spark. Ela permite realizar processamento de dados em larga escala e em tempo real em um ambiente distribuído usando Python. Também fornece um shell PySpark para análise interativa de dados             |
| [Vaex](https://vaex.io/docs/index.html)                               | Focada em "Lazy Out-of-core DataFrames". Ela é excelente se você precisar visualizar esses dados depois sem ocupar quase nada de memória, pois ela mapeia o arquivo no disco em vez de lê-lo                                                 |

#### Vantagens e Desvantagens Libs

| __Biblioteca__ | __Leitura(2 GB)__            | __Limpeza(Drop/Filter)__       | __Exportação Parquet__ | __Vantagem Principal__                             | __Desvantagem Principal__                             |
| -------------- | ---------------------------- | ------------------------------ | ---------------------- | -------------------------------------------------- | ----------------------------------------------------- |
| Dask           | Rápido (Paralelizado)        | Eficiente (Lazy)               | Bom                    | Escala para múltiplos computadores                 | Overhead de configuração para dados "pequenos"        |
| DuckDB         | Instantâneo (Streaming)      | Muito Rápido (via SQL)         | Rápido                 | Pode processar dados maiores que a sua RAM         | Foco maior em SQL do que em manipulação funcional     |
| Modin          | Rápida (Paralelizada)        | Boa (Igual ao Pandas)          | Boa                    | Acelera o Pandas sem mudar nenhuma linha de código | Depende de engines externas (Ray/Dask) para rodar     |
| Pandas         | Muito Lento / Risco de Crash | Simples, mas consome muita RAM | Lento                  | Sintaxe universal e familiar                       | Péssimo gerenciamento de memória                      |
| Polars         | Ultra Rápido                 | Extremamente Eficiente         | Excelente              | Escrito em Rust, usa 100% da CPU nativamente       | Sintaxe levemente diferente do Pandas                 |
| PySpark        | Rápido                       | Robusto                        | Excelente              | Padrão ouro para Big Data (Petabytes)              | Exige Java e tem muito "peso" inicial                 |
| Vaex           | Instantânea (Memory Mapping) | Muito Rápida                   | Boa                    | Permite visualizar bilhões de linhas sem latência  | Menos flexível para manipulações de strings complexas |

#### Qual é a mais viável para o seu projeto?

Para o seu cenário específico (2 GB, foco em limpeza e posterior criação de dashboards), a opção mais viável é o Polars.

#### Por que o Polars?

- Velocidade: Ele vai ler seus 2 GB em segundos, enquanto o Pandas pode levar minutos ou travar.

- Simplicidade Local: Diferente do PySpark (que precisa de JVM/Java) ou Dask (que precisa gerenciar workers), o Polars é apenas um pip install polars.

- Parquet Nativo: Ele foi construído sobre a tecnologia Apache Arrow, que é o "idioma nativo" do formato Parquet. A conversão é quase instantânea.

#### OUTRAS LIBs

| __Bibliotecas__                                           | __Descrição__                                                                                                                                                                                    |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [pathlib](https://docs.python.org/3/library/pathlib.html) | Caminhos do sistema de arquivos orientados a objetos, este módulo oferece classes que representam caminhos de sistema de arquivos com semântica apropriada para diferentes sistemas operacionais |

<br>

### FORMATO ARQUIVO PARA LEITURA APÓS TRANFORMAÇÃO ?

Comparativo de Formatos para Armazenamento (Pós-Tratamento)

- CSV: é o formato mais comum, onde cada linha do arquivo representa um registro e as colunas são separadas por vírgulas.
- JSON: muito usado em APIs web, guarda os dados em pares de chave-valor (como um dicionário Python).
- PARQUET: é o formato mais comum, onde cada linha do arquivo representa um registro e as colunas são separadas por vírgulas.
 
| __FORMATO__ | __TIPO__         | __COMPRESSÃO__          | __VELOCIDADE DE LEITURA__ | __PRESERVA TIPOS DE DADOS?__               | __VANTAGENS__                                                                                                                                                                                                                                                                                                                                                                                                                | __DESVANTAGENS__                                                                                                                                                                                                                                                                                                                                  |
| ----------- | ---------------- | ----------------------- | ------------------------- | ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CSV         | Texto (Linha)    | Baixa (ou nenhuma)      | Lenta                     | Não (Tudo vira string ao salvar)           | - Universal: Praticamente qualquer software do mundo (Excel, Google Sheets, Bancos de Dados) abre um CSV<br>- Simplicidade: Fácil de gerar e fácil de ler manualmente para conferir se os dados estão corretos                                                                                                                                                                                                               | - Pesado: Não possui compressão nativa, ocupando muito espaço em disco<br>- Lento: Para ler a última coluna da última linha, o computador precisa percorrer o arquivo inteiro desde o começo<br>- Perda de Tipos: Tudo é salvo como texto. Ao reabrir, o Python precisa "adivinhar" o que é número, data ou booleano, o que gera erros frequentes |
| JSON        | Texto (Objeto)   | Muito Baixa             | Muito Lenta               | Parcialmente                               | - Flexibilidade: Ótimo para dados que não são perfeitamente tabulares (onde uma linha tem mais informações que outra)<br>- Hierárquico: Permite listas e objetos dentro de objetos                                                                                                                                                                                                                                           | - Extremamente Ineficiente para arquivos muito grande: Como o nome de cada coluna se repete em cada linha, um arquivo de 2 GB de CSV pode virar 6 GB em JSON<br>- Consumo de RAM: Bibliotecas de Data Science sofrem para transformar JSON em tabelas (DataFrames), consumindo muita memória no processo                                          |
| Parquet     | Binário (Coluna) | Altíssima (Snappy/Zstd) | Ultra Rápida              | Sim (Data continua Data, Int continua Int) | - Compressão Eficiente: Reduz drasticamente o tamanho do arquivo<br>- Leitura Seletiva: Se seu gráfico só usa 2 colunas, o código lê apenas os bytes dessas 2 colunas, ignorando o resto do arquivo<br>- Preservação de Tipos: Ele guarda o "Schema". Se você definiu uma coluna como datetime ou int32, ela voltará exatamente assim ao ser lida<br>- Velocidade: É otimizado para as bibliotecas como Polars, Dask e Spark | - Não é Legível por humanos: Você não consegue abrir um arquivo .parquet no Bloco de Notas para dar uma espiada rápida como nos outros formatos<br>- Escrita mais Lenta: O processo de salvar (escrever) demora um pouco mais que o CSV porque ele precisa comprimir e organizar os dados                                                         |

OBS: O CSV e o JSON são formatos de texto "brutos", enquanto o Parquet é um formato binário colunar projetado especificamente para alta performance em Ciência de Dados. Salvar em Parquet transformará seu arquivo de 2 GB em algo muito menor (provavelmente cerca de 300 MB a 600 MB) e muito mais rápido de ler.


### FONTES DE DADOS (DATA SOURCES)
Os dados utilizados neste projeto são provenientes de bases oficiais e governamentais, garantindo a fidedignidade para a construção do modelo preditivo.

INSTITUIÇÃO: INEP (Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira)

DATASET: Taxas de Rendimento Escolar (Aprovação, Reprovação e Abandono)

ABRANGÊNCIA: Estado de São Paulo

LINK PARA ACESSO: [Taxas de Rendimento Escolar - INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/taxas-de-rendimento-escolar)

