import requests
from bs4 import BeautifulSoup
import json
import time


def get_weather_habarovsk():
    url = "https://www.meteoservice.ru/weather/now/habarovsk"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Извлечение текущей температуры
        temperature_tag = soup.find('div', class_='temperature')
        temperature = temperature_tag.text.strip(
        ) if temperature_tag else "Не удалось получить данные"

        # Извлечение описания погоды
        description_tag = soup.find(
            'div', class_='small-12 columns text-center padding-top-2')
        description = description_tag.text.strip(
        ) if description_tag else "Не удалось получить данные"

        # Извлечение даты
        date_tag = soup.find('span', class_='point-time')
        date = date_tag.text.strip() if date_tag else "Не удалось получить данные"

        return {
            "temperature": temperature,
            "small-12 columns text-center padding-top-2": description,
            "point-time": date,
        }
    else:
        return {
            "error": f"Не удалось получить данные с сайта. Статус код: {response.status_code}"
        }


if __name__ == "__main__":
    while True:
        weather_data = get_weather_habarovsk()
        with open('weather_data.json', 'w', encoding='utf-8') as json_file:
            json.dump(weather_data, json_file, ensure_ascii=False, indent=4)

        print("Данные о погоде записаны в файл weather_data.json")

        # Ожидание 10 минут (600 секунд) перед следующим запросом
        time.sleep(600)
