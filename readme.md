# Estudo sobre diferentes SGBDs para proveniência
* Estruturar o dado e explorar ele em múltiplos bancos de dados, mapear padrões de consulta e verificar pontos fortes de cada um dos bancos de dados, para aconselhar qual é melhor para cada necessidade de consulta.
# Comandos para Inicializar BDs
## Iniciar containers e Tratar devidas importações
```sh
bash start.sh
```
## Tratar monetdb
* Estou usando o dbeaver para fazer conexão com o banco monetdb...
	* jdbc url: jdbc:monetdb://localhost:50000/sciphy_dados
	* username e password: monetdb
## Tratar mongodb
* Tenha o compass instalado: https://www.mongodb.com/try/download/compass
* connection string: mongodb://root:root_password@localhost:27017/tcc
## Tratar neo4j
* Estou usando o dbeaver para fazer conexão com o banco neo4j...
	* jdbc url: jdbc:neo4j:bolt://localhost:7687/
	* host: localhost
	* port: 7687
	* username: neo4j
	* password: neo4j
### O neo4j libera na porta 7474 uma interface grafica
* Basta acessar http://localhost:7474
	* Informe as credenciais e veja os nodes construidos
## Tratar postgres
* Estou usando o dbeaver para fazer conexão com o banco postgres...
	* host: localhost
	* database: public
	* port: 5432
	* username: postgres
	* password: postgres
### Estrutura
* DOUBLE => DECIMAL
* CHARACTER LARGE OBJECT => TEXT
* SEQUENCES FORAM REMOVIDOS
	* DEVIDO AO PROBLEMA:
		* SQL Error [0A000]: ERROR: cannot use column reference in DEFAULT expression
			* Isso impedia configurar o valor do campo para ser o default que o sequence trouxesse.
## Documento do Projeto de Aplicação
https://docs.google.com/document/d/1UQB0x5TJVTB5x0rAHzSBzTY1mJK9CxdwBEkLoQZp-cY/edit?usp=sharing
