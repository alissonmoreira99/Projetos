CREATE DATABASE DataAnalystTest;
use DataAnalystTest

/* As bases que contém as pesquisas são compostas por colunas e valores dispostos em códigos. Por isso, 
e seguindo as informações disponíveis no dicionário das variáveis, 5 tabelas serão criadas para atender 
ao modelo. Pois a é ideia é ter uma tabela com todas as descrições no lugar dos códigos*/

/* A tabela Quesitos armazena os códigos e descrições dos quesitos, que estão nas colunas base de pesquisas. 
Dessa forma, é possível relacionar o código do quesito na base de pesquisas com a descrição do dicionário */
CREATE TABLE Quesitos (
    cod_quesito VARCHAR(10) NOT NULL PRIMARY KEY,
    desc_quesito VARCHAR(255) NOT NULL,
);


/* Assim como os quesitos, algumas respostas também possuem códigos. Sendo assim, a tabela
Respostas será criada com os seguintes atributos:
cod_resposta, cod_quesito (cada resposta pertence a um quesito), desc_resposta.
Para identificar cada registro, uma chave composta foi criada com o cod_resposta e cod_quesito*/
CREATE TABLE Respostas (
  cod_resposta INT NOT NULL,
  cod_quesito VARCHAR(10) NOT NULL,
  desc_resposta VARCHAR(255) NOT NULL,
  FOREIGN KEY (cod_quesito) REFERENCES Quesitos(cod_quesito),
  PRIMARY KEY (cod_resposta, cod_quesito)
);


/*De acordo com a estrutura definida, a maioria dos atributos possuem um "objeto resposta", 
que nada mais é do que uma resposta com código e descrição que pertence a um quesito. Para comportar essa estrutura 
no banco de dados, será criada uma tabela que relaciona a pesquisa com o quesito e a resposta.*/
CREATE TABLE Atributos (
   id_atributo INT IDENTITY(1,1) PRIMARY KEY,
   cod_quesito VARCHAR(10) NOT NULL,
   cod_resposta INT NOT NULL,
   id_pesquisa varchar(255) not null,
   FOREIGN KEY (cod_resposta, cod_quesito) REFERENCES Respostas(cod_resposta, cod_quesito),
   FOREIGN KEY (id_pesquisa) REFERENCES Pesquisa(id_pesquisa)
);


/* De acordo com a estrutura definida no dicionário das variáveis, alguns quesitos
não possuem "objetos respostas", e sim um valor que é posto diretamente no campo.
Por isso, a tabela atributos_valores será criada para separar os quesitos com respostas dos quesitos com valores
diretamente inseridos no campo.
Além disso, essa solução permite com que valores nulos não sejam inseridos nas tabelas*/
CREATE TABLE Atributos_valores (
   id_atributo INT IDENTITY(1,1) PRIMARY KEY,
   id_pesquisa varchar(255) not null,
   cod_quesito VARCHAR(10),
   valor VARCHAR(255),
   FOREIGN KEY (id_pesquisa) REFERENCES Pesquisa(id_pesquisa),
   FOREIGN KEY (cod_quesito) REFERENCES Quesitos(cod_quesito)
);


/* A tabela pesquisa identifica cada pesquisa e a qual mês e ano ela pertence*/
CREATE TABLE Pesquisa (
   id_pesquisa varchar(255) PRIMARY KEY,
   mes_ano varchar(10) NOT NULL
);

/* UTILIZE ESSA QUERY PARA VERIFICAR QUE A ESTRUTURA FUNCIONA E RETORNA 
TODAS AS RESPOSTAS PARA OS DEVIDOS QUESITOS, COM DESCRIÇÕES.

select a.id_atributo, a.cod_quesito, q.desc_quesito, a.cod_resposta, r.desc_resposta, p.id_pesquisa from Atributos A 
JOIN Pesquisa P on p.id_pesquisa = a.id_pesquisa
JOIN Respostas r on r.cod_quesito = a.cod_quesito and r.cod_resposta = a.cod_resposta
JOIN Quesitos q on R.cod_quesito = Q.cod_quesito
where p.id_pesquisa = 1

*/
select q.desc_quesito, r.desc_resposta, p.id_pesquisa from Atributos A 
JOIN Pesquisa P on p.id_pesquisa = a.id_pesquisa
JOIN Respostas r on r.cod_quesito = a.cod_quesito and r.cod_resposta = a.cod_resposta
JOIN Quesitos q on R.cod_quesito = Q.cod_quesito
where p.id_pesquisa = 0

-- Query para buscar os quesitos e as descrições, partindo da tabela Atributos_valores (tabela na qual
-- os quesitos não possuem "objetos resposta"
select q.desc_quesito, a.valor, p.id_pesquisa from Atributos_valores a
JOIN Pesquisa p on p.id_pesquisa = a.id_pesquisa
JOIN Quesitos q on a.cod_quesito = q.cod_quesito

/*Essa consulta é utilizada no power BI para transformar as linhas da tabela Atributos_valores em colunas.
Além disso, adiciono mais uma coluna classificando o entrevistado em alguma faixa etária*/
SELECT *,
       CASE
           WHEN [Idade do morador] >= 1 AND [Idade do morador] < 15 THEN '1-14'
           WHEN [Idade do morador] >= 15 AND [Idade do morador] < 25 THEN '15-24'
           WHEN [Idade do morador] >= 25 AND [Idade do morador] < 35 THEN '25-34'
           WHEN [Idade do morador] >= 35 AND [Idade do morador] < 45 THEN '35-44'
           WHEN [Idade do morador] >= 45 AND [Idade do morador] < 55 THEN '45-54'
           WHEN [Idade do morador] >= 55 AND [Idade do morador] < 64 THEN '55-64'
           WHEN [Idade do morador] >= 65 AND [Idade do morador] < 75 THEN '65-74'
           WHEN [Idade do morador] >= 75 AND [Idade do morador] <= 90 THEN '75-90'
           ELSE 'Outros'
       END AS Faixa_Etaria
FROM (
    SELECT q.desc_quesito, a.valor, p.id_pesquisa 
    FROM Atributos_valores a
    JOIN Pesquisa p on p.id_pesquisa = a.id_pesquisa
    JOIN Quesitos q on a.cod_quesito = q.cod_quesito
) src
PIVOT (
    MAX(valor) FOR desc_quesito IN ([Número da entrevista no domicílio], [Semana no mês], [Mês da pesquisa], 
	[Dia de nascimento],[Mês de nascimento],[Ano de Nascimento], [Número de ordem], [Idade do morador], [Projeção da população],
	[Domínios de projeção], [Estrato], [UPA], [Número de seleção do domicílio])
) pvt



/* A seguinte query é uma alternativa mais eficiente para transformar as linhas em colunas. Essa solução 
se deve ao fato de que existem muitos valores para serem transformados em colunas e esse processo é trabalhoso
para ser realizado manualmente*/

DECLARE @cols NVARCHAR(MAX);
DECLARE @query NVARCHAR(MAX);

-- Gerando a lista de colunas para a cláusula IN
SELECT @cols = STUFF((
    SELECT DISTINCT ',[' + q.desc_quesito + ']'
    FROM Quesitos q JOIN Atributos a on a.cod_quesito = q.cod_quesito
    FOR XML PATH('')
), 1, 1, '');

-- Construindo a consulta dinâmica
SET @query = N'
SELECT *
FROM (
    SELECT q.desc_quesito, r.desc_resposta, p.id_pesquisa
    FROM Atributos A
    JOIN Pesquisa P ON p.id_pesquisa = a.id_pesquisa
    JOIN Respostas r ON r.cod_quesito = a.cod_quesito AND r.cod_resposta = a.cod_resposta
    JOIN Quesitos q ON R.cod_quesito = Q.cod_quesito
) src
PIVOT (
    MAX(desc_resposta)
    FOR desc_quesito IN (' + @cols + ')
) pvt';

-- Executando a consulta dinâmica
EXEC sp_executesql @query;

-- tratamento necessário para a execução da query acima. Pois o SQL alegou que o tamanho da coluna é acima de 128 chars
UPDATE Quesitos SET desc_quesito = 'trabalho foi exercido no mesmo local em que costuma' 
where desc_quesito like 
'Na maior parte do tempo, na semana passada, esse trabalho (único ou principal) foi exercido no mesmo local em que costuma trabal%'
