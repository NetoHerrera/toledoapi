import requests

id = input("Digite o numero do usuário: ")
retorno = requests.get(f"https://reqres.in/api/users/{id}")
usuario = retorno.json()
print(f'O usuário  numero {id} é: {usuario["data"]["first_name"]} {usuario["data"]["last_name"]}')