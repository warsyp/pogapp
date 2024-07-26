import json
import time
import psycopg2
from psycopg2 import sql


def read_weather_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def insert_weather_data(data):
    try:
        # Настройки подключения к базе данных
        conn = psycopg2.connect(
            dbname="zeus_db",
            user="transp",
            password="112233",
            host="192.168.1.70",
            port="5432"
        )
        cursor = conn.cursor()

        # SQL-запрос для вставки данных
        insert_query = sql.SQL("""
            INSERT INTO weather_data (temperature, small-12 columns text-center padding-top-2, point-time)
            VALUES (%s, %s, %s)
        """)

        # Данные для вставки
        values = (
            data.get('temperature', 'Не удалось получить данные'),
            data.get('small-12 columns text-center padding-top-2',
                     'Не удалось получить данные'),
            data.get('point-time', 'Не удалось получить данные'),
        )

        # Выполнение запроса на вставку данных
        cursor.execute(insert_query, values)

        # Фиксация изменений
        conn.commit()

        # Закрытие курсора и соединения
        cursor.close()
        conn.close()

        print("Данные успешно записаны в базу данных")

    except Exception as e:
        print(f"Ошибка при записи данных в базу данных: {e}")


if __name__ == "__main__":
    while True:
        file_path = 'weather_data.json'
        weather_data = read_weather_data(file_path)
        insert_weather_data(weather_data)

        # Ожидание 5 минут (300 секунд) перед следующим запуском
        time.sleep(300)
