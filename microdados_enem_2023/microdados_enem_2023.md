# DICIONÁRIO DE VARIÁVEIS - ENEM 2023					

###  DADOS DO PARTICIPANTE

<details><summary><b>Expandir</b></summary>

| __NOME DA VARIÁVEL__ | __Descrição__       | __Variáveis Categóricas (Categoria - Descrição)__ | __Tamanho__ | __Tipo__ |
| -------------------- | ------------------- | ------------------------------------------------- | ----------- | -------- |
| NU_INSCRICAO         | Número de inscrição | 000000000000			                             | 12	       | Numérica |
| NU_ANO	           | Ano do Enem		 | 2023                                              | 4	       | Numérica |
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

| __NOME DA VARIÁVEL__ | __Descrição__       | __Variáveis Categóricas (Categoria - Descrição)__ | __Tamanho__ | __Tipo__ |
| -------------------- | ------------------- | ------------------------------------------------- | ----------- | -------- |

CO_MUNICIPIO_ESC 	Código do município da escola 			7	Numérica
    1º dígito: Região				
    1º e 2º dígitos: UF				
    3º, 4º, 5º e 6º dígitos: Município				
    7º dígito: dígito verificador				
NO_MUNICIPIO_ESC	Nome do município da escola			150	Alfanumérica
CO_UF_ESC	Código da Unidade da Federação da escola			2	Numérica
SG_UF_ESC	Sigla da Unidade da Federação da escola			2	Alfanumérica
TP_DEPENDENCIA_ADM_ESC	Dependência administrativa (Escola)	1	Federal	1	Numérica
        2	Estadual		
        3	Municipal		
        4	Privada		
TP_LOCALIZACAO_ESC	Localização (Escola)	1	Urbana	1	Numérica
        2	Rural		
TP_SIT_FUNC_ESC	Situação de funcionamento (Escola)	1	Em atividade	1	Numérica
        2	Paralisada		
        3	Extinta		
        4	Escola extinta em anos anteriores.

</details>

### DADOS DO LOCAL DE APLICAÇÃO DA PROVA

<details><summary><b>Expandir</b></summary>

| __NOME DA VARIÁVEL__ | __Descrição__       | __Variáveis Categóricas (Categoria - Descrição)__ | __Tamanho__ | __Tipo__ |
| -------------------- | ------------------- | ------------------------------------------------- | ----------- | -------- |

CO_MUNICIPIO_PROVA	Código do município da aplicação da prova			7	Numérica
    1º dígito: Região				
    1º e 2º dígitos: UF				
    3º, 4º, 5º e 6º dígitos: Município				
    7º dígito: dígito verificador				
NO_MUNICIPIO_PROVA	Nome do município da aplicação da prova			150	Alfanumérica
CO_UF_PROVA	Código da Unidade da Federação da aplicação da prova			2	Alfanumérica
SG_UF_PROVA	Sigla da Unidade da Federação da aplicação da prova			2	Alfanumérica

</details>

### DADOS DA PROVA OBJETIVA

<details><summary><b>Expandir</b></summary>

| __NOME DA VARIÁVEL__ | __Descrição__       | __Variáveis Categóricas (Categoria - Descrição)__ | __Tamanho__ | __Tipo__ |
| -------------------- | ------------------- | ------------------------------------------------- | ----------- | -------- |

TP_PRESENCA_CN	Presença na prova objetiva de Ciências da Natureza	0	Faltou à prova	1	Numérica
        1	Presente na prova		
        2	Eliminado na prova		
TP_PRESENCA_CH	Presença na prova objetiva de Ciências Humanas	0	Faltou à prova	1	Numérica
        1	Presente na prova		
        2	Eliminado na prova		
TP_PRESENCA_LC	Presença na prova objetiva de Linguagens e Códigos	0	Faltou à prova	1	Numérica
        1	Presente na prova		
        2	Eliminado na prova		
TP_PRESENCA_MT	Presença na prova objetiva de Matemática	0	Faltou à prova	1	Numérica
        1	Presente na prova		
        2	Eliminado na prova		
CO_PROVA_CN	Código do tipo de prova de Ciências da Natureza	1221	Azul	4	Numérica
        1222	Amarela		
        1223	Rosa		
        1224	Cinza		
        1225	Rosa - Ampliada		
        1226	Rosa - Superampliada		
        1227	Laranja - Braile		
        1228	Laranja - Adaptada Ledor		
        1229	Verde - Videoprova - Libras		
        1301	Azul (Reaplicação)		
        1302	Amarela (Reaplicação)		
        1303	Cinza (Reaplicação)		
        1304	Rosa (Reaplicação)		
CO_PROVA_CH	Código do tipo de prova de Ciências Humanas	1191	Azul	4	Numérica
        1192	Amarela		
        1193	Branca		
        1194	Rosa		
        1195	Rosa - Ampliada		
        1196	Rosa - Superampliada		
        1197	Laranja - Braile		
        1198	Laranja - Adaptada Ledor		
        1199	Verde - Videoprova - Libras		
        1271	Azul (Reaplicação)		
        1272	Amarela (Reaplicação)		
        1273	Branca (Reaplicação)		
        1274	Rosa (Reaplicação)		
CO_PROVA_LC	Código do tipo de prova de Linguagens e Códigos	1201	Azul	4	Numérica
        1202	Amarela		
        1203	Rosa		
        1204	Branca		
        1205	Rosa - Ampliada		
        1206	Rosa - Superampliada		
        1207	Laranja - Braile		
        1208	Laranja - Adaptada Ledor		
        1209	Verde - Videoprova - Libras		
        1281	Azul (Reaplicação)		
        1282	Amarela (Reaplicação)		
        1283	Rosa (Reaplicação)		
        1284	Branca (Reaplicação)		
CO_PROVA_MT	Código do tipo de prova de Matemática	1211	Azul	4	Numérica
        1212	Amarela		
        1213	Rosa		
        1214	Cinza		
        1215	Rosa - Ampliada		
        1216	Rosa - Superampliada		
        1217	Laranja - Braile		
        1218	Laranja - Adaptada Ledor		
        1219	Verde - Videoprova - Libras		
        1291	Azul (Reaplicação)		
        1292	Amarela (Reaplicação)		
        1293	Rosa (Reaplicação)		
        1294	Cinza (Reaplicação)		
NU_NOTA_CN	Nota da prova de Ciências da Natureza			9	Numérica
NU_NOTA_CH	Nota da prova de Ciências Humanas			9	Numérica
NU_NOTA_LC	Nota da prova de Linguagens e Códigos			9	Numérica
NU_NOTA_MT	Nota da prova de Matemática			9	Numérica
TX_RESPOSTAS_CN	Vetor com as respostas da parte objetiva da prova de Ciências da Natureza4 		A,B,C,D, E, * (dupla marcação), . (em branco)	45	Alfanumérica
TX_RESPOSTAS_CH	Vetor com as respostas da parte objetiva da prova de Ciências Humanas4		A,B,C,D, E, * (dupla marcação), . (em branco)	45	Alfanumérica
TX_RESPOSTAS_LC	Vetor com as respostas da parte objetiva da prova de Linguagens e Códigos5 		A,B,C,D, E, * (dupla marcação), . (em branco), 9 (Item não apresentado)	45	Alfanumérica
TX_RESPOSTAS_MT	Vetor com as respostas da parte objetiva da prova de Matemática4 		A,B,C,D, E, * (dupla marcação), . (em branco)	45	Alfanumérica
TP_LINGUA	Língua Estrangeira 	0	Inglês	1	Numérica
        1	Espanhol		
TX_GABARITO_CN	Vetor com o gabarito da parte objetiva da prova de Ciências da Natureza6 			45	Alfanumérica
TX_GABARITO_CH	Vetor com o gabarito da parte objetiva da prova de Ciências Humanas6 			45	Alfanumérica
TX_GABARITO_LC	Vetor com o gabarito da parte objetiva da prova de Linguagens e Códigos7 			50	Alfanumérica
TX_GABARITO_MT	Vetor com o gabarito da parte objetiva da prova de Matemática6			45	Alfanumérica

</details>

### DADOS DA REDAÇÃO

<details><summary><b>Expandir</b></summary>

| __NOME DA VARIÁVEL__ | __Descrição__       | __Variáveis Categóricas (Categoria - Descrição)__ | __Tamanho__ | __Tipo__ |
| -------------------- | ------------------- | ------------------------------------------------- | ----------- | -------- |

TP_STATUS_REDACAO	Situação da redação do participante	1	Sem problemas	1	Numérica
        2	Anulada		
        3	Cópia Texto Motivador		
        4	Em Branco		
        6	Fuga ao tema		
        7	Não atendimento ao tipo textual		
        8	Texto insuficiente		
        9	Parte desconectada		
NU_NOTA_COMP1	Nota da competência 1 - Demonstrar domínio da modalidade escrita formal da Língua Portuguesa.			9	Numérica
NU_NOTA_COMP2	Nota da competência 2 - Compreender a proposta de redação e aplicar conceitos das várias áreas de conhecimento para desenvolver o tema, dentro dos limites estruturais do texto dissertativo-argumentativo em prosa.			9	Numérica
NU_NOTA_COMP3	Nota da competência 3 - Selecionar, relacionar, organizar e interpretar informações, fatos, opiniões e argumentos em defesa de um ponto de vista.			9	Numérica
NU_NOTA_COMP4	Nota da competência 4 - Demonstrar conhecimento dos mecanismos linguísticos necessários para a construção da argumentação.			9	Numérica
NU_NOTA_COMP5	Nota da competência 5 - Elaborar proposta de intervenção para o problema abordado, respeitando os direitos humanos.			9	Numérica
NU_NOTA_REDACAO	Nota da prova de redação			9	Numérica
DADOS DO QUESTIONÁRIO SOCIOECONÔMICO					
Q001	Até que série seu pai, ou o homem responsável por você, estudou?	A	Nunca estudou.	1	Alfanumérica
        B	Não completou a 4ª série/5º ano do Ensino Fundamental.		
        C	Completou a 4ª série/5º ano, mas não completou a 8ª série/9º ano do Ensino Fundamental.		
        D	Completou a 8ª série/9º ano do Ensino Fundamental, mas não completou o Ensino Médio.		
        E	Completou o Ensino Médio, mas não completou a Faculdade.		
        F	Completou a Faculdade, mas não completou a Pós-graduação.		
        G	Completou a Pós-graduação.		
        H	Não sei.		
Q002	Até que série sua mãe, ou a mulher responsável por você, estudou?	A	Nunca estudou.	1	Alfanumérica
        B	Não completou a 4ª série/5º ano do Ensino Fundamental.		
        C	Completou a 4ª série/5º ano, mas não completou a 8ª série/9º ano do Ensino Fundamental.		
        D	Completou a 8ª série/9º ano do Ensino Fundamental, mas não completou o Ensino Médio.		
        E	Completou o Ensino Médio, mas não completou a Faculdade.		
        F	Completou a Faculdade, mas não completou a Pós-graduação.		
        G	Completou a Pós-graduação.		
        H	Não sei.		
Q003	A partir da apresentação de algumas ocupações divididas em grupos ordenados, indique o grupo que contempla a ocupação mais próxima da ocupação do seu pai ou do homem responsável por você. (Se ele não estiver trabalhando, escolha uma ocupação pensando no último trabalho dele).	A	Grupo 1: Lavrador, agricultor sem empregados, bóia fria, criador de animais (gado, porcos, galinhas, ovelhas, cavalos etc.), apicultor, pescador, lenhador, seringueiro, extrativista.	1	Alfanumérica
        B	Grupo 2: Diarista, empregado doméstico, cuidador de idosos, babá, cozinheiro (em casas particulares), motorista particular, jardineiro, faxineiro de empresas e prédios, vigilante, porteiro, carteiro, office-boy, vendedor, caixa, atendente de loja, auxiliar administrativo, recepcionista, servente de pedreiro, repositor de mercadoria.		
        C	Grupo 3: Padeiro, cozinheiro industrial ou em restaurantes, sapateiro, costureiro, joalheiro, torneiro mecânico, operador de máquinas, soldador, operário de fábrica, trabalhador da mineração, pedreiro, pintor, eletricista, encanador, motorista, caminhoneiro, taxista.		
        D	Grupo 4: Professor (de ensino fundamental ou médio, idioma, música, artes etc.), técnico (de enfermagem, contabilidade, eletrônica etc.), policial, militar de baixa patente (soldado, cabo, sargento), corretor de imóveis, supervisor, gerente, mestre de obras, pastor, microempresário (proprietário de empresa com menos de 10 empregados), pequeno comerciante, pequeno proprietário de terras, trabalhador autônomo ou por conta própria.		
        E	Grupo 5: Médico, engenheiro, dentista, psicólogo, economista, advogado, juiz, promotor, defensor, delegado, tenente, capitão, coronel, professor universitário, diretor em empresas públicas ou privadas, político, proprietário de empresas com mais de 10 empregados.		
        F	Não sei.		
Q004	A partir da apresentação de algumas ocupações divididas em grupos ordenados, indique o grupo que contempla a ocupação mais próxima da ocupação da sua mãe ou da mulher responsável por você. (Se ela não estiver trabalhando, escolha uma ocupação pensando no último trabalho dela).	A	Grupo 1: Lavradora, agricultora sem empregados, bóia fria, criadora de animais (gado, porcos, galinhas, ovelhas, cavalos etc.), apicultora, pescadora, lenhadora, seringueira, extrativista.	2	Numérica
        B	Grupo 2: Diarista, empregada doméstica, cuidadora de idosos, babá, cozinheira (em casas particulares), motorista particular, jardineira, faxineira de empresas e prédios, vigilante, porteira, carteira, office-boy, vendedora, caixa, atendente de loja, auxiliar administrativa, recepcionista, servente de pedreiro, repositora de mercadoria.		
        C	Grupo 3: Padeira, cozinheira industrial ou em restaurantes, sapateira, costureira, joalheira, torneira mecânica, operadora de máquinas, soldadora, operária de fábrica, trabalhadora da mineração, pedreira, pintora, eletricista, encanadora, motorista, caminhoneira, taxista.		
        D	Grupo 4: Professora (de ensino fundamental ou médio, idioma, música, artes etc.), técnica (de enfermagem, contabilidade, eletrônica etc.), policial, militar de baixa patente (soldado, cabo, sargento), corretora de imóveis, supervisora, gerente, mestre de obras, pastora, microempresária (proprietária de empresa com menos de 10 empregados), pequena comerciante, pequena proprietária de terras, trabalhadora autônoma ou por conta própria.		
        E	Grupo 5: Médica, engenheira, dentista, psicóloga, economista, advogada, juíza, promotora, defensora, delegada, tenente, capitã, coronel, professora universitária, diretora em empresas públicas ou privadas, política, proprietária de empresas com mais de 10 empregados.		
        F	Não sei.		
Q005	Incluindo você, quantas pessoas moram atualmente em sua residência?	1	1, pois moro sozinho(a).	2	Numérica
        2	2		
        3	3		
        4	4		
        5	5		
        6	6		
        7	7		
        8	8		
        9	9		
        10	10		
        11	11		
        12	12		
        13	13		
        14	14		
        15	15		
        16	16		
        17	17		
        18	18		
        19	19		
        20	20		
Q006	Qual é a renda mensal de sua família? (Some a sua renda com a dos seus familiares.)	A	Nenhuma Renda	1	Alfanumérica
        B	Até R$ 1.320,00		
        C	De R$ 1.320,01 até R$ 1.980,00.		
        D	De R$ 1.980,01 até R$ 2.640,00.		
        E	De R$ 2.640,01 até R$ 3.300,00.		
        F	De R$ 3.300,01 até R$ 3.960,00.		
        G	De R$ 3.960,01 até R$ 5.280,00.		
        H	De R$ 5.280,01 até R$ 6.600,00.		
        I	De R$ 6.600,01 até R$ 7.920,00.		
        J	De R$ 7.920,01 até R$ 9240,00.		
        K	De R$ 9.240,01 até R$ 10.560,00.		
        L	De R$ 10.560,01 até R$ 11.880,00.		
        M	De R$ 11.880,01 até R$ 13.200,00.		
        N	De R$ 13.200,01 até R$ 15.840,00.		
        O	De R$ 15.840,01 até R$19.800,00.		
        P	De R$ 19.800,01 até R$ 26.400,00.		
        Q	Acima de R$ 26.400,00.		
Q007	Em sua residência trabalha empregado(a) doméstico(a)?	A	Não.	1	Alfanumérica
        B	Sim, um ou dois dias por semana.		
        C	Sim, três ou quatro dias por semana.		
        D	Sim, pelo menos cinco dias por semana.		
Q008	Na sua residência tem banheiro?	A	Não.	1	Alfanumérica
        B	Sim, um.		
        C	Sim, dois.		
        D	Sim, três.		
        E	Sim, quatro ou mais.		
Q009	Na sua residência tem quartos para dormir?	A	Não.	1	Alfanumérica
        B	Sim, um.		
        C	Sim, dois.		
        D	Sim, três.		
        E	Sim, quatro ou mais.		
Q010	Na sua residência tem carro?	A	Não.	1	Alfanumérica
        B	Sim, um.		
        C	Sim, dois.		
        D	Sim, três.		
        E	Sim, quatro ou mais.		
Q011	Na sua residência tem motocicleta?	A	Não.	1	Alfanumérica
        B	Sim, uma.		
        C	Sim, duas.		
        D	Sim, três.		
        E	Sim, quatro ou mais.		
Q012	Na sua residência tem geladeira?	A	Não.	1	Alfanumérica
        B	Sim, uma.		
        C	Sim, duas.		
        D	Sim, três.		
        E	Sim, quatro ou mais.		
Q013	Na sua residência tem freezer (independente ou segunda porta da geladeira)?	A	Não.	1	Alfanumérica
        B	Sim, um.		
        C	Sim, dois.		
        D	Sim, três.		
        E	Sim, quatro ou mais.		
Q014	Na sua residência tem máquina de lavar roupa? (o tanquinho NÃO deve ser considerado)	A	Não.	1	Alfanumérica
        B	Sim, uma.		
        C	Sim, duas.		
        D	Sim, três.		
        E	Sim, quatro ou mais.		
Q015	Na sua residência tem máquina de secar roupa (independente ou em conjunto com a máquina de lavar roupa)?	A	Não.	1	Alfanumérica
        B	Sim, uma.		
        C	Sim, duas.		
        D	Sim, três.		
        E	Sim, quatro ou mais.		
Q016	Na sua residência tem forno micro-ondas?	A	Não.	1	Alfanumérica
        B	Sim, um.		
        C	Sim, dois.		
        D	Sim, três.		
        E	Sim, quatro ou mais.		
Q017	Na sua residência tem máquina de lavar louça?	A	Não.	1	Alfanumérica
        B	Sim, uma.		
        C	Sim, duas.		
        D	Sim, três.		
        E	Sim, quatro ou mais.		
Q018	Na sua residência tem aspirador de pó?	A	Não.	1	Alfanumérica
        B	Sim.		
Q019	Na sua residência tem televisão em cores?	A	Não.	1	Alfanumérica
        B	Sim, uma.		
        C	Sim, duas.		
        D	Sim, três.		
        E	Sim, quatro ou mais.		
Q020	Na sua residência tem aparelho de DVD?	A	Não.	1	Alfanumérica
        B	Sim.		
Q021	Na sua residência tem TV por assinatura?	A	Não.	1	Alfanumérica
        B	Sim.		
Q022	Na sua residência tem telefone celular?	A	Não.	1	Alfanumérica
        B	Sim, um.		
        C	Sim, dois.		
        D	Sim, três.		
        E	Sim, quatro ou mais.		
Q023	Na sua residência tem telefone fixo?	A	Não.	1	Alfanumérica
        B	Sim.		
Q024	Na sua residência tem computador?	A	Não.	1	Alfanumérica
        B	Sim, um.		
        C	Sim, dois.		
        D	Sim, três.		
        E	Sim, quatro ou mais.		
Q025	Na sua residência tem acesso à Internet?	A	Não.	1	Alfanumérica
        B	Sim.

</details>

<br>

---

<br>

`REFERÊNCIA`
1. Referente ao Enem 2023, trata-se de uma máscara e não o seu número de inscrição original no Enem. O mesmo NU_INSCRICAO para anos diferentes não identifica o mesmo participante no exame, não permite o acesso aos dados cadastrais como nome, endereço, RG etc, nem identifica o mesmo participante em microdados de pesquisas diferentes.					
2. A partir da Idade do inscrito em 31/12/2023.					
3. Foi considerado treineiro o inscrito que não havia concluído o ensino médio e não o concluiria em 2023					
4. As 45 primeiras posições deste campo são referentes as respectivas respostas. O asterisco (*) indica dupla marcação e o ponto (.) resposta em branco.					
5. As 45 primeiras posições deste campo são referentes as respectivas respostas, das quais as 5 primeiras correspondem a parte de língua estrangeira. O asterisco (*) indica dupla marcação e o ponto (.) resposta em branco.					
6. As 45 primeiras posições deste campo são referentes ao respectivo gabarito					
7. As 50 primeiras posições deste campo são referentes ao respectivo gabarito, das quais, para as 10 primeiras, as 5 primeiras correspondem à prova de Lingua Inglesa e as outras 5 à prova de Lingua Espanhola.					
