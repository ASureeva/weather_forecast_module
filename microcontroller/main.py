import network
import urequests
import time
import os


def load_env(filename=".env"):
    env = {}
    try:
        with open(filename) as f:
            for line in f:
                key, value = line.strip().split("=", 1)
                env[key] = value
    except OSError:
        print("Ошибка: файл окружения не найден")
    return env


env = load_env()

SSID = env.get("WIFI_SSID")
PASSWORD = env.get("WIFI_PASSWORD")
SERVER_URL = env.get("SERVER_URL")


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Подключение к Wi-Fi...")

    while not wlan.isconnected():
        time.sleep(1)
        print(".", end="")

    print("\nПодключено! IP-адрес:", wlan.ifconfig()[0])

    return wlan.ifconfig()[0]


def send_data(temp, hum, measure):
    try:
        headers = {'Content-Type': 'application/json'}
        data = {"temperature": temp, "humidity": hum, "measure": measure}
        response = urequests.post(SERVER_URL, json=data, headers=headers, timeout=5)
        print("Ответ сервера:", response.text)
        response.close()
    except Exception as e:
        print("Ошибка при отправке данных:", e)


def main():
    ip = connect_wifi()

    while True:
        try:

            measure = '12'
            temp = '13'
            hum = '14'

            print(f"Температура: {temp}°C, Влажность: {hum}%, sensor: {measure}")

            send_data(temp, hum, measure)

        except Exception as e:
            print("Ошибка чтения датчика:", e)

        time.sleep(10)


main()
