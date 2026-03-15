# DICIONÁRIO DE VARIÁVEIS - ENEM 2023					

###  DADOS DO PARTICIPANTE

<details><summary><b>Expandir</b></summary>

| __NOME DA VARIÁVEL__ | __Descrição__       | __Variáveis Categóricas (Categoria - Descrição)__ | __Tamanho__ | __Tipo__ |
| -------------------- | ------------------- | ------------------------------------------------- | ----------- | -------- |
| NU_INSCRICAO         | Número de inscrição | 000000000000			                 | 12	       | Numérica |
| NU_ANO	       | Ano do Enem         | 2023                                              | 4	       | Numérica |
| TP_FAIXA_ETARIA      | Faixa etária²       | 1 -	Menor de 17 anos<br>2 - 17 anos<br>3 - 18 anos<br>4 - 19 anos<br>5 - 20 anos<br>6 - 21 anos<br>7 - 22 anos<br>8 -23 anos<br>9 - 24 anos<br>10 - 25 anos<br>11 - Entre 26 e 30 anos<br>12 - Entre 31 e 35 anos<br>13 - Entre 36 e 40 anos<br>14 - Entre 41 e 45 anos<br>15 - Entre 46 e 50 anos<br>16 - Entre 51 e 55 anos<br>17 - Entre 56 e 60 anos<br>18 - Entre 61 e 65 anos<br>19 - Entre 66 e 70 anos<br>20 - Maior de 70 anos<br> | 2	       | Numérica |       
| TP_SEXO              | Sexo                | M - Masculino<br>F - Feminino                     | 1	       | Alfanumérica |
| TP_ESTADO_CIVIL      | Estado Civil	     | 0 - Não informado<br>1 - Solteiro(a)<br>2 - Casado(a)/Mora com companheiro(a)<br>3 - Divorciado(a)/Desquitado(a)/Separado(a)<br>4 - Viúvo(a) | 1	       | Numérica     |
| TP_COR_RACA	       | Cor/raça            | 0 - Não declarado<br>1 - Branca<br>2 - Preta<br>3 - Parda<br>4 - Amarela<br>5 - Indígena<br>6 - Não dispõe da informação | 1           | Numérica     |
| TP_NACIONALIDADE     | Nacionalidade       | 0 -Não informado<br>1 - Brasileiro(a)<br>2 - Brasileiro(a) Naturalizado(a)<br>3 - Estrangeiro(a)<br>4 - Brasileiro(a) Nato(a), nascido(a) no exterior | 1            | Numérica    |
| TP_ST_CONCLUSAO      | Situação de conclusão do Ensino Médio | 1 - Já concluí o Ensino Médio<br>2 - Estou cursando e concluirei o Ensino Médio em 2023<br>3 - Estou cursando e concluirei o Ensino Médio após 2023<br>4 - Não concluí e não estou cursando o Ensino Médio | 1            | Numérica    |
| TP_ANO_CONCLUIU      | Ano de Conclusão do Ensino Médio |	0	Não informado<br>1 - 2022<br>2 - 2021<br>3 - 2020<br>4 - 2019<br>5 - 2018<br>6 - 2017<br>7 - 2016<br>8 - 2015<br>9 - 2014<br>10 - 2013<br>11 - 2012<br>12 - 2011<br>13 - 2010<br>14 - 2009<br>15 - 2008<br>16 - 2007<br>17 - Antes de 2007 | 1           | Numérica      |
| TP_ESCOLA            | Tipo de escola do Ensino Médio | 1 - Não Respondeu<br>2 - Pública<br>3 - Privada | 1            | Numérica     |
| TP_ENSINO            | Tipo de instituição que concluiu ou concluirá o Ensino Médio |	1 - Ensino Regular<br>2 - Educação Especial - Modalidade Substitutiva | 1            | Numérica     |
| IN_TREINEIRO	       | Indica se o inscrito fez a prova com intuito de apenas treinar seus conhecimento³ | 1 - Sim<br>0 - Não	| 1            | Numérica     |

</details>

### DADOS DA ESCOLA

<details><summary><b>Expandir</b></summary>

| __NOME DA VARIÁVEL__  | __Descrição__                            | __Variáveis Categóricas (Categoria - Descrição)__ | __Tamanho__ | __Tipo__     |
| --------------------- | ---------------------------------------- | ------------------------------------------------- | ----------- | ------------ |
| CO_MUNICIPIO_ESC      | código do município da escola<br>1º dígito: Região<br>1º e 2º dígitos: UF<br>3º, 4º, 5º e 6º dígitos: Município<br>7º dígito: dígito verificador | 0000000  | 7           | Numérica |
| NO_MUNICIPIO_ESC      | Nome do município da escola              | Nome Municipio	                               | 150	     | Alfanumérica |
| CO_UF_ESC	            | Código da Unidade da Federação da escola | 00         	                               | 2	     | Numérica     |
| SG_UF_ESC             | Sigla da Unidade da Federação da escola  | 00			                               | 2           | Alfanumérica |
| TP_DEPENDENCIA_ADM_ESC| Dependência administrativa (Escola)      | 1 - Federal<br><br>2 - Estadual<br>3 - Municipal<br>4 - Privada | 1           | Numérica     |
| TP_LOCALIZACAO_ESC    | Localização (Escola)                     | 1 - Urbana<br>2 - Rural                           | 1           | Numérica     |
| TP_SIT_FUNC_ESC       | Situação de funcionamento (Escola)       | 1 - Em atividade<br><br>2 - Paralisada<br>3 - Extinta<br>4 - Escola extinta em anos anteriores | 1	     | Numérica     |

</details>

### DADOS DO LOCAL DE APLICAÇÃO DA PROVA

<details><summary><b>Expandir</b></summary>

| __NOME DA VARIÁVEL__ | __Descrição__                                        | __Variáveis Categóricas (Categoria - Descrição)__ | __Tamanho__ | __Tipo__     |
| -------------------- | ---------------------------------------------------- | ------------------------------------------------- | ----------- | ------------ |
| CO_MUNICIPIO_PROVA   | Código do município da aplicação da prova<br>1º dígito: Região<br>1º e 2º dígitos: UF<br>3º, 4º, 5º e 6º dígitos: Município<br>7º dígito: dígito verificador | 0000000 | 7           | Numérica     |
| NO_MUNICIPIO_PROVA   | Nome do município da aplicação da prova              | Nome Municipio                                    | 150         | Alfanumérica |
| CO_UF_PROVA          | Código da Unidade da Federação da aplicação da prova | 00			                          | 2	        | Alfanumérica |
| SG_UF_PROVA	       | Sigla da Unidade da Federação da aplicação da prova  | SP			                          | 2	        | Alfanumérica |

</details>

### DADOS DA PROVA OBJETIVA

<details><summary><b>Expandir</b></summary>

| __NOME DA VARIÁVEL__ | __Descrição__                                      | __Variáveis Categóricas (Categoria - Descrição)__                     | __Tamanho__ | __Tipo__     |
| -------------------- | -------------------------------------------------- | --------------------------------------------------------------------- | ----------- | ------------ |
| TP_PRESENCA_CN       | Presença na prova objetiva de Ciências da Natureza | 0 - Faltou à prova<br>1 - Presente na prova<br>2 - Eliminado na prova | 1           | Numérica     |
| TP_PRESENCA_CH       | Presença na prova objetiva de Ciências Humanas     | 0 - Faltou à prova<br>1 - Presente na prova<br>2 - Eliminado na prova | 1           | Numérica     |
| TP_PRESENCA_LC       | Presença na prova objetiva de Linguagens e Códigos | 0 - Faltou à prova<br>1 - Presente na prova<br>2 - Eliminado na prova | 1           | Numérica     |
| TP_PRESENCA_MT       | Presença na prova objetiva de Matemática           | 0 - Faltou à prova<br>1 - Presente na prova<br>2 - Eliminado na prova | 1           | Numérica     |		
| CO_PROVA_CN	       | Código do tipo de prova de Ciências da Natureza    | 1221 - Azul<br>1222 - Amarela<br>1223 - Rosa<br>1224 - Cinza<br>1225 - Rosa - Ampliada<br>1226 - Rosa - Superampliada<br>1227 - Laranja - Braile<br>1228 - Laranja - Adaptada Ledor<br>1229 - Verde - Videoprova - Libras<br>1301 - Azul (Reaplicação)<br>1302 - Amarela (Reaplicação)<br>1303 - Cinza (Reaplicação)<br>1304 - Rosa (Reaplicação) | 4          | Numérica   |
| CO_PROVA_CH	       | Código do tipo de prova de Ciências Humanas	    | 1191 - Azul<br>1192 - Amarela<br>1193 - Branca<br>1194 - Rosa<br>1195 - Rosa - Ampliada<br>1196 - Rosa - Superampliada<br>1197 - Laranja - Braile<br>1198 - Laranja - Adaptada Ledor<br>1199 - Verde - Videoprova - Libras<br>1271 - Azul (Reaplicação)<br>1272 - Amarela (Reaplicação)<br>1273 - Branca (Reaplicação)<br>1274 - Rosa (Reaplicação) | 4	        | Numérica   |
| CO_PROVA_LC	       | Código do tipo de prova de Linguagens e Códigos    | 1201 - Azul<br>1202 - Amarela<br>1203 - Rosa<br>1204 - Branca<br>1205 - Rosa - Ampliada<br>1206 - Rosa - Superampliada<br>1207 - Laranja - Braile<br>1208 - Laranja - Adaptada Ledor<br>1209 - Verde - Videoprova - Libras<br>1281 - Azul (Reaplicação)<br>1282 - Amarela (Reaplicação)<br>1283 - Rosa (Reaplicação)<br>1284 - Branca (Reaplicação) | 4           | Numérica   |
| CO_PROVA_MT          | Código do tipo de prova de Matemática	            | 1211 - Azul<br>1212 - Amarela<br>1213 - Rosa<br>1214 - Cinza<br>1215 - Rosa - Ampliada<br>1216 - Rosa - Superampliada<br>1217 - Laranja - Braile<br>1218 - Laranja - Adaptada Ledor<br>1219 - Verde - Videoprova - Libras<br>1291 - Azul (Reaplicação)<br>1292 - Amarela (Reaplicação)<br>1293 - Rosa (Reaplicação)<br>1294 - Cinza (Reaplicação) | 4           | Numérica   |
| NU_NOTA_CN           | Nota da prova de Ciências da Natureza              | 000000000                                                             | 9           | Numérica     |
| NU_NOTA_CH           | Nota da prova de Ciências Humanas                  | 000000000			                                            | 9	          | Numérica     |
| NU_NOTA_LC           | Nota da prova de Linguagens e Códigos	            | 000000000 		                                            | 9	          | Numérica     |
| NU_NOTA_MT	       | Nota da prova de Matemática			    | 000000000                                                             | 9           | Numérica     |
| TX_RESPOSTAS_CN      | Vetor com as respostas da parte objetiva da prova de Ciências da Natureza^4 | A,B,C,D,E, *(dupla marcação), .(em branco)   | 45          | Alfanumérica |
| TX_RESPOSTAS_CH      | Vetor com as respostas da parte objetiva da prova de Ciências Humanas^4     | A,B,C,D,E, *(dupla marcação), .(em branco)   | 45          | Alfanumérica |
| TX_RESPOSTAS_LC      | Vetor com as respostas da parte objetiva da prova de Linguagens e Códigos^5 | A,B,C,D,E, *(dupla marcação), .(em branco), 9 (Item não apresentado) | 45     | Alfanumérica |
| TX_RESPOSTAS_MT      | Vetor com as respostas da parte objetiva da prova de Matemática^4           | A,B,C,D,E, *(dupla marcação), .(em branco)   | 45          | Alfanumérica |
| TP_LINGUA            | Língua Estrangeira                                 | 0 - Inglês<br>1 - Espanhol	                                    | 1           | Numérica     |
| TX_GABARITO_CN       | Vetor com o gabarito da parte objetiva da prova de Ciências da Natureza^6   |			                            | 45	  | Alfanumérica |
| TX_GABARITO_CH       | Vetor com o gabarito da parte objetiva da prova de Ciências Humanas^6 	     |		                                    | 45	  | Alfanumérica |
| TX_GABARITO_LC       | Vetor com o gabarito da parte objetiva da prova de Linguagens e Códigos^7   | 			                            | 50	  | Alfanumérica |
| TX_GABARITO_MT       | Vetor com o gabarito da parte objetiva da prova de Matemática^6	     | 		                                    | 45	  | Alfanumérica |

</details>

### DADOS DA REDAÇÃO

<details><summary><b>Expandir</b></summary>

| __NOME DA VARIÁVEL__ | __Descrição__                       | __Variáveis Categóricas (Categoria - Descrição)__ | __Tamanho__ | __Tipo__     |
| -------------------- | ----------------------------------- | ------------------------------------------------- | ----------- | ------------ |
| TP_STATUS_REDACAO    | Situação da redação do participante |	1 - Sem problemas<br>2 - Anulada<br>3 - Cópia Texto Motivador<br>4 - Em Branco<br>6 - Fuga ao tema<br>7 - Não atendimento ao tipo textual<br>8 - Texto insuficiente<br>9 - Parte desconectada | 1	       | Numérica     |
| NU_NOTA_COMP^1       | Nota da competência 1 - Demonstrar domínio da modalidade escrita formal da Língua Portuguesa |       | 9         | Numérica    |
| NU_NOTA_COMP^2       | Nota da competência 2 - Compreender a proposta de redação e aplicar conceitos das várias áreas de conhecimento para desenvolver o tema, dentro dos limites estruturais do texto dissertativo-argumentativo em prosa |       | 9         | Numérica    |
| NU_NOTA_COMP^3       | Nota da competência 3 - Selecionar, relacionar, organizar e interpretar informações, fatos, opiniões e argumentos em defesa de um ponto de vista |       | 9         | Numérica    |
| NU_NOTA_COMP^4       | Nota da competência 4 - Demonstrar conhecimento dos mecanismos linguísticos necessários para a construção da argumentação |       | 9         | Numérica    |
| NU_NOTA_COMP^5       | Nota da competência 5 - Elaborar proposta de intervenção para o problema abordado, respeitando os direitos humanos |       | 9         | Numérica    |
| NU_NOTA_REDACAO      | Nota da prova de redação            |                                                    | 9           | Numérica     |

</details>

<br>

---

<br>

`REFERÊNCIA E CITAÇÃO`
> **1.** Referente ao Enem 2023, trata-se de uma máscara e não o seu número de inscrição original no Enem. O mesmo NU_INSCRICAO para anos diferentes não identifica o mesmo participante no exame, não permite o acesso aos dados cadastrais como nome, endereço, RG etc, nem identifica o mesmo participante em microdados de pesquisas diferentes.					

> **2.** A partir da Idade do inscrito em 31/12/2023.					

> **3.** Foi considerado treineiro o inscrito que não havia concluído o ensino médio e não o concluiria em 2023					

> **4.** As 45 primeiras posições deste campo são referentes as respectivas respostas. O asterisco (*) indica dupla marcação e o ponto (.) resposta em branco.					

> **5.** As 45 primeiras posições deste campo são referentes as respectivas respostas, das quais as 5 primeiras correspondem a parte de língua estrangeira. O asterisco (*) indica dupla marcação e o ponto (.) resposta em branco.					

> **6.** As 45 primeiras posições deste campo são referentes ao respectivo gabarito					

> **7.** As 50 primeiras posições deste campo são referentes ao respectivo gabarito, das quais, para as 10 primeiras, as 5 primeiras correspondem à prova de Lingua Inglesa e as outras 5 à prova de Lingua Espanhola.					
