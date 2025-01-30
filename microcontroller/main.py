from machine import Pin, I2C
import network
import urequests
import time
import BME280
import utime


def get_iso_timestamp():

    t = utime.gmtime()
    ms = int((utime.time() % 1) * 1000)
    return "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.{:02d}".format(
        t[0], t[1], t[2], t[3]-3, t[4]-4, t[5], ms
    )


i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)
devices = i2c.scan()


def load_env(filename=".env"):
    env = {}
    try:
        with open(filename) as f:
            for line in f:
                key, value = line.strip().split("=", 1)
                env[key] = value
    except OSError:
        print("Error: Environment file not found.")
    return env


env = load_env()

SSID = env["WIFI_SSID"]
PASSWORD = env["WIFI_PASSWORD"]
SERVER_URL = env["SERVER_URL"]


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Connecting to  Wi-Fi...")

    while not wlan.isconnected():
        time.sleep(1)
        print(".", end="")

    print("\nConencted! IPv4:", wlan.ifconfig()[0])

    return wlan.ifconfig()[0]


def send_data(temp, hum, pressure):
    try:
        headers = {'Content-Type': 'application/json'}
        data = {"temperature": float(temp[:-1]),
                "humidity": float(hum[:-1]),
                "pressure": float(pressure[:-3]),
                "timestamp": get_iso_timestamp()}
        response = urequests.post(SERVER_URL+'weather/', json=data, headers=headers, timeout=5)
        response.close()
    except Exception as e:
        print("No response:", e)


def run_prediction(step=12):
    try:
        headers = {'Content-Type': 'application/json'}
        response = urequests.post(SERVER_URL+'forecast/run?steps='+str(step), headers=headers, timeout=5)
        response.close()
    except Exception as e:
        print("No response:", e)


def main():
    bme = BME280.BME280(i2c=i2c)
    connect_wifi()
    prediction_queue = 0
    while True:
        try:

            pressure = bme.pressure
            temp = bme.temperature
            hum = bme.humidity

            send_data(temp, hum, pressure)
            prediction_queue += 1

            if prediction_queue == 5:
                run_prediction()
                prediction_queue = 0

        except Exception as e:
            print("Chip is not available:", e)

        time.sleep(10)


main()
