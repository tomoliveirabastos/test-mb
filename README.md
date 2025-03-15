# test-mb

### Dependencias
```bash
uv - geranciador de pacotes https://github.com/astral-sh/uv
fastapi - framework web https://fastapi.tiangolo.com/
sqlalchemy - orm de bancos de dados https://www.sqlalchemy.org/
mysql - banco de dados https://www.mysql.com/
docker/docker-compose - container da aplicacao https://www.docker.com/
make - para automatizar comandos e sequencias de tarefas para facilitar o trabalho
curl - para requisicoes
crontab - para executar o work em segundo plano
```

### para buildar voce pode usar o comando make container, ele vai criar os containers de docker e setar o nginx como proxy e loadbalance

# buildar usando docker
```bash
make container
ou
docker-compose build && docker-compose up -d
```

# executar comando com container de migracao
```bash
docker exec -t ap1 python migrate.py
```

# executar worker com container para plotar dados
```bash
docker exec -t ap1 python worker.py :numero_de_dias
```

# buidar sem docker
você precisará instalar o mysql, curl
usar o comando:
```bash
uv sync
```

após rodar todos comandos e instalar o mysql e curl você terá que executar o comando para criar o banco de dados:
```bash
uv run migrate.py
```

executar o comando do worker para plotar dados:
```bash
uv run worker.py :numero_de_dias
```

executar o servidor web
```bash
uv run fastapi dev app.py
ou
make
```

### executar tests
```bash
uv run test.py
ou
docker exec -t ap1 python test.py
```

Para executar diariamente a busca na API do mercadobitcoin precisará colocar o worker na execução do cronjobs,
no arquivo crontab tem um exemplo de linha de execução no crontab.
A necessidade de colocar o numero de dias no primeiro argumento do worker é para fazer a contagem do dia de hoje para trás, ou seja se o argumento for 2, vai contar de hoje até 2 dias atrás.

### Documentação de referencia da api
http://127.0.0.1/docs

### Exemplo de requets
http://127.0.0.1:8000/BRLBTC/mms?from_timestamp=1712004438&to_timestamp=1742004438&range=20