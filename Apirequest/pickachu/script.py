import requests

url = "https://pokeapi.co/api/v2/"

def pickachu_info(name):
    full_api = f"{url}/pokemon/{name}"
    response = requests.get(full_api)
    if response.status_code == 200:
        data = response.json()
        return data
        # print(data)

pickache_name = "pikachu"
pickachi_data = pickachu_info(pickache_name)

for i in pickachi_data:

    if pickachi_data:
        name = pickachi_data.get('name')
        print(name)
        print(f"{pickachi_data['id']}")
        print(f"{pickachi_data["height"]}")
        weight = pickachi_data.get('weight')
        print(weight)