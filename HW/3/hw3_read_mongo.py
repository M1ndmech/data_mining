import json
import pandas as pd
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

# Выбор базы данных и коллекции
db = client['scraping']
collection = db['books']

# вывод первой записи в коллекции
all_books = collection.find()
first_book = all_books[0]

# Вывод объекта JSON
pretty_json = json.dumps(first_book, indent=4, default=str)
print(pretty_json)

# Получение количества документов в коллекции с помощью функции count_documents()
count = collection.count_documents({})
print(f'Число записей в базе данных: {count}')

# фильтрация документов по критериям
query = {"stock": 20}
print(f"Количество книг с остатком запасов, равным 20: {collection.count_documents(query)}")

# Использование проекции
query = {"stock": 20}
projection = {"title": 1, "price": 1, "_id": 0}
proj_docs = collection.find(query, projection)
for doc in proj_docs:
    print(doc)

# Использование оператора $lt и $gte
query = {"stock": {"$lt": 5}}
print(f"Количество книг c остатком < 5: {collection.count_documents(query)}")
query = {"stock": {"$gte": 21}}
print(f"Количество книг c остатком >= 21: {collection.count_documents(query)}")

# Использование оператора $regex
query = {"description": {"$regex": "music", "$options": "i"}}
print(f"Количество книг, содержащих 'music' в описании: {collection.count_documents(query)}")

# Использование оператора $in
query = {"stock": {"$in": [20, 22]}}
print(f"Количество книг с остатком 20 или 22: {collection.count_documents(query)}")

'''
# Использование оператора $all
query = {"properties.rdconfigur": {"$all": ["TWO-WAY", "DIVIDED"]}}
print(f"Количество документов в категории rdconfigur: {collection.count_documents(query)}")

# для случаев, когда в одном из полей массив и требуюется поиск соответствия по нескольким значениям внутри такового
'''

# Использование оператора $ne
query = {"stock" : {"$ne": 1}}
print(f"Количество книг с остатком не равным 1: {collection.count_documents(query)}")

