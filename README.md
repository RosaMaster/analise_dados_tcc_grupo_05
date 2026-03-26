# TRABALHO DE CONCLUSÃO DE CURSO EM CIÊNCIA DE DADOS
### Grupo: BCD - TCC530 - A2026S1N3 - GRUPO 5
#### Tema: MODELO PREDITIVO DE EVASÃO E DESEMPENHO ESCOLAR DO ESTADO DE SÃO PAULO

---

Repositório para armazenamento de dados e analise de dados do TCC Científico do __BCD - TCC530 - A2026S1N3 - GRUPO 5__.

| __Bibliotecas__                                                       | __Descrição__                                                                                                                                                      |
| --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Dask](https://docs.dask.org/en/stable/)                              | Dask é uma biblioteca Python para computação paralela e distribuída                                                                                                |
| [DuckDB](https://duckdb.org/docs/stable/)                             | É um banco de dados analítico que roda "dentro" do seu script Python. Ele é fenomenal para ler CSVs gigantes e já salvar em Parquet usando SQL ou comandos simples. Ele não carrega tudo na RAM de uma vez (streaming) |
| [Modin](https://modin.readthedocs.io/en/stable/)                      | Uma biblioteca que atua como um "acelerador" do Pandas. Você muda apenas uma linha de código (import modin.pandas as pd) e ele distribui o processamento em todos os núcleos do seu processador automaticamente usando Ray ou Dask por baixo |
| [Panda](https://pandas.pydata.org/docs/)                              | Pandas é uma biblioteca de código aberto, licenciada sob a licença BSD, que fornece estruturas de dados de alto desempenho e ferramentas de análise de dados fáceis de usar para a linguagem de programação Python |
| [Polars](https://pola.rs/)                                            | Polars é uma biblioteca DataFrame extremamente rápida para manipulação de dados estruturados. O núcleo é escrito em Rust e está disponível para Python, R e NodeJS |
| [PySpark](https://spark.apache.org/docs/latest/api/python/index.html) | PySpark é a API Python para Apache Spark. Ela permite realizar processamento de dados em larga escala e em tempo real em um ambiente distribuído usando Python. Também fornece um shell PySpark para análise interativa de dados |
| [Vaex](https://vaex.io/docs/index.html)                               | Focada em "Lazy Out-of-core DataFrames". Ela é excelente se você precisar visualizar esses dados depois sem ocupar quase nada de memória, pois ela mapeia o arquivo no disco em vez de lê-lo. |

#### Vantagens e Desvantagens

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

OBS: Utilizando no projeto, use o termo "Lazy Evaluation" e "Memory Efficient Processing". Explicar que você escolheu uma ferramenta que não sobrecarrega a memória RAM (como o Polars ou DuckDB) demonstra uma maturidade técnica de Engenharia de Dados muito maior do que apenas "fazer o código funcionar".

### ÍNDICE

1. [Microdados do ENEM 2023](#microdados-do-enem-2023)
2. [Microdados do ENADE 2023](#microdados-do-enade-2023)
3. [Microdados do Censo Escolar da Educação Básica 2025](#microdados-do-censo-escolar-da-educação-básica-2025)
4. [Microdados](#microdados)

### MICRODADOS DO ENEM 2023

`OBS: (Arquivos atualizados em 24/07/2024 após ajustes no dicionário de dados e na base de itens)`

> **ENEM**<br>
Os microdados do ENEM são o menor nível de desagregação de dados recolhidos por meio do exame. Eles atendem a demanda por informações específicas ao disponibilizar as provas, os gabaritos, as informações sobre os itens, as notas e o questionário respondido pelos inscritos no ENEM.

Link fonte: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem

COLUNAS
['NU_INSCRICAO', 'NU_ANO', 'TP_FAIXA_ETARIA', 'TP_SEXO', 'TP_ESTADO_CIVIL', 'TP_COR_RACA', 'TP_NACIONALIDADE', 'TP_ST_CONCLUSAO', 'TP_ANO_CONCLUIU', 'TP_ESCOLA', 'TP_ENSINO', 'IN_TREINEIRO', 'CO_MUNICIPIO_ESC', 'NO_MUNICIPIO_ESC', 'CO_UF_ESC', 'SG_UF_ESC', 'TP_DEPENDENCIA_ADM_ESC', 'TP_LOCALIZACAO_ESC', 'TP_SIT_FUNC_ESC', 'CO_MUNICIPIO_PROVA', 'NO_MUNICIPIO_PROVA', 'CO_UF_PROVA', 'SG_UF_PROVA', 'TP_PRESENCA_CN', 'TP_PRESENCA_CH', 'TP_PRESENCA_LC', 'TP_PRESENCA_MT', 'CO_PROVA_CN', 'CO_PROVA_CH', 'CO_PROVA_LC', 'CO_PROVA_MT', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'TX_RESPOSTAS_CN', 'TX_RESPOSTAS_CH', 'TX_RESPOSTAS_LC', 'TX_RESPOSTAS_MT', 'TP_LINGUA', 'TX_GABARITO_CN', 'TX_GABARITO_CH', 'TX_GABARITO_LC', 'TX_GABARITO_MT', 'TP_STATUS_REDACAO', 'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5', 'NU_NOTA_REDACAO', 'Q001', 'Q002', 'Q003', 'Q004', 'Q005', 'Q006', 'Q007', 'Q008', 'Q009', 'Q010', 'Q011', 'Q012', 'Q013', 'Q014', 'Q015', 'Q016', 'Q017', 'Q018', 'Q019', 'Q020', 'Q021', 'Q022', 'Q023', 'Q024', 'Q025']

[**+ INFO**](/microdados_enem_2023/microdados-enem-2023.md)

### MICRODADOS DO ENADE 2023

`OBS: (Atualizado em 24/04/2025)`

> **ENADE**<br>
Microdados do Enade

Link fonte: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enade

[**+ INFO**](./microdados_enade_2023/microdados_enade_2023.md)

### MICRODADOS DO CENSO ESCOLAR DA EDUCAÇÃO BÁSICA 2025

> **CENSO ESCOLAR**<br>
Microdados do Censo Escolar da Educacação Básica

Link fonte: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar

[**+ INFO**](./microdados_censo_2025/microdados_censo_2025.md)

### MICRODADOS

> **MICRODADOS**<br>
Os microdados do Inep reúnem um conjunto de informações detalhadas relacionadas às pesquisas, aos exames e avaliações do Instituto. Os formatos de apresentação do conteúdo dos arquivos estão sendo reestruturados para suprimir a possibilidade de identificação de pessoas, em atendimento às normas previstas na Lei n.º 13.709, de 14 de agosto de 2018 – Lei Geral de Proteção de Dados Pessoais (LGPD).

| __MICRODADOS__                                       | __DESCRIÇÃO__                                                                              | __LINK__ |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------ | -------- |
| ANA                                                  | Microdados da Avaliação Nacional da Alfabetização                                          | https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/ana |
| CENSO DA EDUCAÇÃO SUPERIOR                           | Microdados do Censo da Educação Superior                                                   | https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-da-educacao-superior |
| CENSO ESCOLAR                                        | Microdados do Censo Escolar da Educação Básica                                             | https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar |
| ENADE                                                | Microdados do Enade                                                                        | https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enade |
| ENAMED                                               | Microdados do Enamed                                                                       | https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enamed |
| ENCCEJA                                              | Microdados do Exame Nacional para Certificação de Competências de Jovens e Adultos         | https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/encceja |
| ENEM                                                 | Microdados do Enem são o menor nível de desagregação de dados recolhidos por meio do exame | https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem |
| Enem por Escola                                      | Microdados do Exame Nacional do Ensino Médio por Escola                                    | https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem-por-escola |
| IDD                                                  | Microdados do Indicador da Diferença entre os Desempenhos Observado e Esperado             | https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/idd |
| PESQUISA DE AÇÕES DISCRIMINATÓRIAS NO ÂMBITO ESCOLAR | Microdados da Pesquisa de Ações Discriminatórias no Âmbito Escolar                         | https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/pesquisa-de-acoes-discriminatorias-no-ambito-escolar |
| PNERA                                                | Microdados da Pesquisa Nacional da Educação na Reforma Agrária                             | https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/pnera |
| SAEB                                                 | Microdados do Sistema de Avaliação da Educação Básica                                      | https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/saeb |
| TALIS                                                | Microdados da Pesquisa Internacional sobre Ensino e Aprendizagem                           | https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/talis |
| CENSO DOS PROFISSIONAIS DO MAGISTÉRIO                | Microdados do Censo dos Profissionais do Magistério                                        | https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-dos-profissionais-do-magisterio-1 |

Link fonte: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados


## :tada: CRIANDO UM AMBIENTE VIRTUAL NA VISUAL STUDIO CODE `venv`

- Execute o comando abaixo na raiz do projeto via prompt de comando:

~~~Shell
python -m venv venv
~~~

- Após criar seu ambiente virtual para o projeto atual. Ative o ambiente virtual com o comando abaixo:

~~~Shell
venv\Scripts\activate
~~~

- Caso queira desativar o ambiente virtal é só executar o comando abaixo:

~~~Shell
deactivate
~~~

</details>

<br>

<details><summary>Criando venv pelo terminal Git Bash</summary>

- Execute o comando abaixo na raiz do projeto via prompt de comando:

~~~Bash
python -m venv venv
~~~

- Após criar seu ambiente virtual para o projeto atual. Ative o ambiente virtual com o comando abaixo:

~~~Bash
source venv/Scripts/activate
~~~

- Caso queira desativar o ambiente virtal é só executar o comando abaixo:

~~~Bash
deactivate
~~~

</details>

<br>

- Validando as bibliotecas instaladas na `venv`:

~~~Bash
pip list
~~~

- Se precisar atualizar a versão do `pip`, execute:

~~~Bash
python.exe -m pip install --upgrade pip
~~~

- Instalando uma biblioteca:

~~~Bash
pip install nome_da_biblioteca
~~~

- Desinstalar uma biblioteca:

~~~Bash
pip uninstall nome_da_biblioteca
~~~

- Criando arquivo `requirements.txt`:

~~~Bash
pip freeze > requirements.txt
~~~

- Instalando bibliotecas do arquivo `requirements.txt`, se ele existir:

~~~Bash
pip install -r requirements.txt
~~~

</details><br>
