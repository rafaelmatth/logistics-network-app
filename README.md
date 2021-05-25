# executando logistics-network-app 

Para rodar o projeto é importante que tenha uma virtualenv instalada, assim poderá isolar uma versão especifica de python, no caso desse projeto, python3.

Neste link é possivel baixar uma virtualenv pelo gerenciador de pacotes do python pip: https://pypi.org/project/virtualenv/
- 1. `pip install virtualenv` -> assim você instala a virtualenv
- 2. `virtualenv nome_da_sua_venv` -> assim você cria uma nova virtualenv, lembrando que 'nome_da_sua_venv' pode ser qualquer um definido por você.

Após baixar é preciso ligar sua virtualenv com o comando no diretório instalado -> `source nome_da_sua_env/bin/activate`

Após termos uma versão de python isolada, vamos baixar as dependências do projeto, para isso, entre no diretório deste repositório e execute o comando: 
`pip install -r requirements.txt`


Em seguida teremos que rodar todas as migrações para um banco sqlite de teste com o comando `python manage.py migrate` no diretório deste repositório

E antes de rodar um projeto vamos criar um super usuário, basta rodar `python manage.py createsuperuser` e colocar suas credenciais

feito isso, vamos rodar o projeto: `python manage.py runserver`

OBS: Você também pode ter toda a gerência da sua base de dados através do admin localizado na rotal `localhost:8000/admin/`, utilize o seu superusuário para logar nele

# API

Agora vamos falar um pouco sobre as demais rotas que temos na api.


Registro de usuário (POST)
----------
`localhost:8000/auth/register`
 com o método POST você pode adicionar um novo usuário relizando uma requisição com esse exemplo de json: 
```json
{
	"username": "test@email.com",
	"password": "@@12345@@"
}
```
Após logar um usuário você obterá um token na resposta da requisição, é importante guarda-lo para realizar as futuras requisições.

Realizando login (POST)
----------
`localhost:8000/auth/login` Após ter um usuário cadastrado você poderá consumir o endpoint de login para sempre obter o seu token com o seguinte exemplo de json utilizando o método POST: 
```json
{
	"username": "test@email.com",
	"password": "@@12345@@"
}
```
Após registrar um usuário você obterá um token na resposta da requisição, é importante guarda-lo para realizar as futuras requisições.

Criando um mapa (POST)(Authorization  Token exemple_token)
----------
`localhost:8000/create/map` Agora é possivel registrar um mapa, e basta apenas fornecer um nome para ele como no exemplo do json abaixo. Também será necessário a partir de agora informar o token nas demais requisições,
para isso, forneça um header com o nome Authorization e com o valor Token seu_token, um exemplo ficaria assim 
- `Authorization  Token 11f0e6e64becb3f2b5a96651f46f01ae467a08fa`

```json
{
	"name": "Mapa SP"
}
```
Após registrar um usuário você obterá um token na resposta da requisição, é importante guarda-lo para realizar as futuras requisições.

Criando uma malha logística (POST)(Authorization  Token admin_exemple_token)
----------
`localhost:8000/logistics_network` para criar uma malha logística é necessário um token de admin, então pegue o token do seu superadmin criado e substitua no header da requisição. Além disso, para criar a malha é necessário fornecer dados como o nome do mapa, cidade de origem, cidade de destino e a distância entre eles, assim como no exemplo abaixo:

```json
{
  "map_name": "Mapa SP",
  "origin_city": "R",
  "destination_city": "F",
  "distance": "40.5"
}
```

Listando malhas logística (GET)(Authorization  Token admin_exemple_token)
----------
`localhost:8000/logistics_network` para listar todas as malhas logísticas basta relizar uma requisição get fornecendo um token de admin

Editando malha logística (PUT)(Authorization  Token admin_exemple_token)
----------
`localhost:8000/logistics_network` para editar uma malha forneça um json seguindo a regra dos dados abaixo com o método PUT. OBS: o id da malha você poderá obter no endpoint de listagem de malhas, também é necessário o token de um admin.
```json
{
  "id": 20,
  "origin_city": "D",
  "destination_city": "F",
  "distance": "43.5"
}
```

Deletando malha logística (DELETE)(Authorization  Token admin_exemple_token)
----------
`localhost:8000/logistics_network` para deletar uma malha é necessário apenas fornecer o id da mesma, e um token de admin.
```json
{
	"id": 20
}
```

Consultando Malhas (POST)(Authorization  Token exemple_token)
----------
`localhost:8000/get_travel_value` para obter o menor percurso entra as rotas das malhas registradas de um determinado mapa, é necessário realizar uma requisição POST
e fornecer dados como, nome do mapa, cidade de origin, cidade de destino, autonomia do veículo km/l, e o preço da gasolina, além de um token, veja o exemplo abaixo.
```json
{
  "map_name": "Mapa 1",
  "origin_city": "A",
  "destination_city": "C",
  "vehicle_autonomy": "10",
  "fuel_value": "2.50"
}
```

Verificando número de rotas de uma cidade (POST)(Authorization  Token exemple_token)
----------
`localhost:8000/total_routes_city` Nesse endpoind podemos ver quantas rotas tem uma determinada cidade fornecendo o nome dela e um token no header.

```json
{
	"city_name": "D"
}
```
