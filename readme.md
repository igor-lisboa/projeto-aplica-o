# Estudo sobre diferentes SGBDs para proveniência
* Estruturar o dado e explorar ele em múltiplos bancos de dados, mapear padrões de consulta e verificar pontos fortes de cada um dos bancos de dados, para aconselhar qual é melhor para cada necessidade de consulta.
# Comandos para Inicializar BDs
## Iniciar containers
```sh
docker compose up --build -d
```
## Tratar monetdb
### Restaurando databse a partir do dump
```sh
docker exec -it projeto_aplicacao_monetdb bash
```
* comando que entra no terminal dentro do container
```sh
monetdbd create mydbfarm && cd mydbfarm && monetdbd get all ./ && monetdb create sciphy_dados && monetdb release sciphy_dados && cd ../../../var/data
```
```sh
mclient -u monetdb -d sciphy_dados
password: monetdb
```
```sql
\<dados_sciphy.sql
```
### SGBD
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
## Tratar postgres
* Estou usando o dbeaver para fazer conexão com o banco postgres...
	* host: localhost
	* database: tcc
	* port: 5432
	* username: postgres
	* password: postgres
## Tratar redis
* Tenha o Redis Desktop Manager instalado: https://rdm.dev/pricing (para linux é gratuito)
* connection string: redis://localhost:6379