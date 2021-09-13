docker-compose down
docker-compose up --build -d
docker exec -it projeto_aplicacao_monetdb bash -c "monetdbd create mydbfarm && cd mydbfarm && monetdbd get all ./ && monetdb create sciphy_dados && monetdb release sciphy_dados && cp ../.monetdb .monetdb && cd ../../../var/data && mclient -d sciphy_dados \< dados_sciphy.sql"