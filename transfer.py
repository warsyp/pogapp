import psycopg2
import json
import time

def transfer_to_db():
    # Параметры подключения к базе данных
    conn = psycopg2.connect(
        host="172.20.10.8",
        port="5432",
        database="zeus_db",
        user="transp",
        password="112233"
    )

    cursor = conn.cursor()

    with open('weather_data.json', 'r', encoding='utf-8') as json_file:
        weather_data = json.load(json_file)

    # Проверка на наличие ошибки в данных
    if "error" in weather_data:
        print(f"Ошибка при получении данных: {weather_data['error']}")
        return

    # SQL-запрос для вставки данных
    insert_query = """
    INSERT INTO weather_date (temperature, description, date)
    VALUES (%s, %s, %s)
    """

    try:
        # Извлечение данных
        temperature = weather_data['temperature']
        description = weather_data['description']
        date = weather_data['date']

        # Выполнение запроса на вставку данных
        cursor.execute(insert_query, (temperature, description, date))

        # Фиксация изменений
        conn.commit()

        print("Данные успешно записаны в базу данных.")

    except Exception as e:
        print(f"Ошибка при вставке данных: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    while True:
        transfer_to_db()
        # Ожидание 5 минут (300 секунд) перед следующим запросом
        time.sleep(650)
