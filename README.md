# _weather_forecast_module_ - _Платформа мониторинга и прогнозирования погоды_

## Описание проекта
Система состоит из трёх основных компонентов:
+ Модуль сбора данных — микроконтроллер с подключенными датчиками собирает данные о температуре, влажности и атмосферном давлении.
+ Модуль обработки собранных данных и прогнозирования — серверная часть, которая принимает данные с датчиков, сохраняет их, анализирует и генерирует прогноз на следующие 24 часа на основе алгоритмов временных рядов.
+ Веб-интерфейс — Пользовательская часть, которая отображает текущие данные с датчиков и прогноз на следующие 24 часа.


## Участники 
+ Бровин Роман
+ Иванов Тимур
+ Суреева Анна

## Технологии
+ MicroPython
+ Python, Cython
+ HTML, CSS, Brython
  

## Инструкция по запуску
in progress...
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


## Использование
in progress...

## Полезные ссылки
+ [Яндекс Трекер](https://tracker.yandex.ru/pages/projects/1)
+ [ТЗ](https://docs.google.com/document/d/1jqwq2AIuy9JbQfYT4eQSN86LeIlsva3Xh_djTVbTft4/edit?tab=t.0)
