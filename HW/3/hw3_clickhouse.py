from clickhouse_driver import Client
import uuid
import json

# Подключение к серверу ClickHouse
client = Client(host='localhost',
                user='default',
                password='',
                port=9000)

# Создание базы данных (если она не существует)
client.execute('CREATE DATABASE IF NOT EXISTS scraping')

# Создание таблицы
# Создание основной таблицы 'crashes'
client.execute('''
CREATE TABLE IF NOT EXISTS scraping.books (
    id VARCHAR(255) DEFAULT generateUUIDv4(),
    title String,
    price Float64,
    stock Int64,           
    description String
) ENGINE = MergeTree()
ORDER BY title
''')

print("Таблица создана успешно.")

with open(r'C:\Users\Alexey\Desktop\GB\Data_collection\books_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


# Вставка данных в таблицу
for item in data:

    # Вставка данных
    client.execute("""
    INSERT INTO scraping.books (
        id, title, price,
        stock, description
    ) VALUES""",
    [("DEFAULT",
      item['title'] or "",
      item['price'] or 0,
      item['stock'] or 0,
      item['description'] or "",
      )])

print("Данные введены успешно.")

# Проверка успешности вставки
result = client.execute("SELECT * FROM scraping.books")
print("Вставленная запись:", result[0])