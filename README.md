# _weather_forecast_module_ 
## Project Description
The system consists of three main components:
+ Data acquisition module - a microcontroller with connected sensors collects data on temperature, humidity and atmospheric pressure.
+ Module for processing collected data and forecasting - a server part that receives data from sensors, stores it, analyzes and generates a forecast for the next 24 hours based on time series algorithms.
+ Web interface - User part that displays current data from sensors and a forecast for the next 24 hours.


## members 
+ Бровин Роман
+ Иванов Тимур
+ Суреева Анна

## Technologies
+ MicroPython
+ Python, Cython
+ HTML, CSS, Brython
  

## Startup instructions

### brython
+ cd brython
+ python -m http.server 8080

### microcontroller
+ esptool --port COM3 --baud 460800 write_flash --flash_size=detect 0 ESP8266_GENERIC-
20241129-v1.24.1.bin
+ mpremote connect COM3 cp main.py :
+ mpremote connect COM3 cp .env :  
+ mpremote connect COM3 cp BME280.py :
+ mpremote connect COM3 run main.py

### backend
+ cd backend
+ docker-compose up --build

## Links
+ [Yandex Tracker](https://tracker.yandex.ru/pages/projects/1)
+ [ТЗ](https://docs.google.com/document/d/1jqwq2AIuy9JbQfYT4eQSN86LeIlsva3Xh_djTVbTft4/edit?tab=t.0)
