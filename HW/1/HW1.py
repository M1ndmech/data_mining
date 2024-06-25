import requests
import json

# Ваши учетные данные API
client_id = "RMALVHIRBVH3KAORAJNNB3PZKORL5KK02XIHMU2O1MH0FDEH"
client_secret = "VRQXNVUUPYLHZKXY3ZOFAL3OBVGLJ2XMWZXDC3Z2MOSY5SDG"


# Конечная точка API
endpoint = "https://api.foursquare.com/v3/places/search"

# Определение параметров для запроса API
city = input("Введите название города: ")
category = input("Введите категорию: ")
params = {
    "client_id": client_id,
    "client_secret": client_secret,
    "near": city,
    "query": category
}

params_short = {
    "client_id": client_id,
    "client_secret": client_secret,
}

headers = {
    "Accept": "application/json",
    "Authorization": "fsq3R4LbR1wFfJp/0Gq+4ErE7lJiNeaS80qHZNX0rdFiUsI="
}

# Отправка запроса API и получение ответа
response = requests.get(endpoint, params=params,headers=headers)

# Проверка успешности запроса API
if response.status_code == 200:
    print("Успешный запрос API!")
    data = json.loads(response.text)
    venues = data["results"]
    for venue in venues:
        place_id = venue['fsq_id']
        details_endpoint = f"https://api.foursquare.com/v3/places/{place_id}?fields=rating"
        response_details = requests.get(details_endpoint, params=params_short,headers=headers)
        if response_details.status_code == 200:
            details_data = json.loads(response_details.text)
        print("Название:", venue["name"])
        print("Адрес:", venue["location"]["address"])
        print("Рейтинг:", details_data['rating'])
else:
    print("Запрос API завершился неудачей с кодом состояния:", response.status_code)
    print(response.text)
