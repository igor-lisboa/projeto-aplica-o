echo "===============INICIALIZACAO INICIADA==============="
docker-compose down
docker-compose up --build -d
sleep 5
docker exec -it projeto_aplicacao_monetdb bash -c "monetdbd create mydbfarm && cd mydbfarm && monetdbd get all ./ && monetdb create sciphy_dados && monetdb release sciphy_dados && cp ../.monetdb .monetdb && cd ../../../var/data && mclient -d sciphy_dados \< dados_sciphy.sql"
sleep 5
docker exec -it projeto_aplicacao_pyimporter bash -c "cd /var/app && rm -R venv -f && rm -R env -f && python3 -m pip install --upgrade pip && python3 -m venv ./venv && source venv/bin/activate && pip install -r requirements.txt && python3 -m postgresImporter"
sleep 5
echo "===============INICIALIZACAO FINALIZADA==============="