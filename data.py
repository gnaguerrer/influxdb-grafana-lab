import time
import requests
import schedule
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "lab1"
org = "gnaguerrer"
token = "A_TBnJ1YHNWKDSZrtGK6hREZJEVSuTaauldxMRCBEN-_xIVgewvOnL80LdDRA6LzMBj1dwMp06NcOtbN2mgsOw=="


# Store the URL of your InfluxDB instance
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)


def get_weather():
    # Realizar petición a la API de tiempo
    response = requests.get(
        'https://api.openweathermap.org/data/2.5/weather?q=Barranquilla&appid=79cc07714ea13101bd6fc7d25e0ed142')
    data = response.json()
    # Obtener la temperatura en grados Celsius
    temperature = data['main']['temp'] - 273.15
    humidity = data['main']['humidity']
    # Write script
    write_api = client.write_api(write_options=SYNCHRONOUS)
    p = influxdb_client.Point("temperature").field("value", temperature)
    write_api.write(bucket=bucket, org=org, record=p)
    p1 = influxdb_client.Point("humidity").field("value", humidity)
    write_api.write(bucket=bucket, org=org, record=p1)
    print(
        f'La temperatura actual es: {temperature}°C y la humedad es: {humidity}%')


# Programar la ejecución de la función cada 30 minutos
schedule.every(10).seconds.do(get_weather)

while True:
    schedule.run_pending()
    time.sleep(1)
