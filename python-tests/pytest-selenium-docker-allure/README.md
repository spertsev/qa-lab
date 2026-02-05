# Автотесты на Python + Pytest + Selenium + Docker + Allure

Проект демонстрирует минимальную структуру автотестов на Python + Pytest + Selenium, используя Selenium Manager для автоматической установки и управления WebDriver.

Проект поддерживает запуск автотестов как локально, так и в контейнеризованной среде (Docker).

В репозитории представлена Docker-конфигурация для запуска автотестов в контейнере.
При запуске в Docker автотесты выполняются в отдельном контейнере и подключаются к контейнеру с браузером Google Chrome, запущенному на основе стандартного образа Selenium standalone-chrome.

Результаты выполнения автотестов формируются в виде отчетов Allure.

## Требования
- Python 3.8+
- установлен один из браузеров:
  - Chrome 
  - Chromium
  - Firefox
  - Edge
  - Safari (только macOS)
- Selenium 4.6+ (ставится из `requirements.txt`)

## Подготовка окружения
### Создание виртуального окружения
```bash
python -m venv venv
```
### Активация виртуального окружения
### Windows: 
```powershell
venv\Scripts\activate
```
### Linux / macOS:
```bash
source venv/bin/activate
```
### Установка необходимых пакетов
```bash
pip install -r requirements.txt
```

## Запуск тестов
### Windows: 
```powershell
pytest .\tests -v
```
### Linux / macOS:
```bash
pytest ./tests -v
```

## Необязательные параметры запуска тестов
- `--browser=<имя>`   тип браузера (без указания используется Chrome)
  - Поддерживаемые значения:
    - chrome
    - chromium
    - firefox
    - edge
    - safari (только macOS)
  - Пример:
    `pytest .\tests\ -v --browser=edge`
- `--headless=<on|off>`   режим headless браузера (по умолчанию: off)
  - Пример:
    `pytest .\tests\ -v --headless=on`

## Получение HTML-отчёта Allure

Результаты Allure генерируются автоматически при каждом запуске тестов в директорию `allure-results` (настроено в `pytest.ini`).

### 1. Генерация HTML-отчёта
```bash
allure generate allure-results -o allure-report --clean
```

### 3. Открытие HTML-отчёта
#### Вариант 1: Открыть в браузере (статические файлы)
```bash
allure open allure-report
```

#### Вариант 2: Запустить локальный сервер (рекомендуется)
```bash
allure serve allure-results
```
Команда автоматически сгенерирует отчёт и откроет его в браузере по адресу `http://localhost:XXXX`

**Примечание:** Для работы с Allure необходимо установить [Allure Commandline](https://github.com/allure-framework/allure2/releases) или использовать Docker-образ с Allure.

## Запуск тестов в Docker + получение отчётов

### Предусловия
- Docker и Docker Compose установлены на машине.

### Запуск Selenium + тестов в контейнерах
Из корня проекта:

```bash
docker compose -f docker/selenium-standalone-chrome-and-python-tests-docker-compose.yml up --build
```

- поднимется контейнер `selenium` с образом `selenium/standalone-chrome`;
- затем запустится контейнер `tests`, внутри которого будет выполнен `pytest ./tests`.

При таком запуске Chrome внутри контейнера `selenium` работает в **обычном (не headless)** режиме: используется виртуальный дисплей, а на хосте проброшен порт `5900`, к которому можно **подключиться по VNC**, чтобы визуально наблюдать выполнение тестов в браузере.

### Где искать Allure-отчёты при запуске в Docker

В файле `pytest.ini` настроена опция:

```ini
[pytest]
addopts = --alluredir=allure-results
```

В `docker/selenium-standalone-chrome-and-python-tests-docker-compose.yml` директория с результатами примонтирована в корень проекта:

```yaml
volumes:
  - ../allure-results:/tests/allure-results
```

Поэтому:
- при запуске **локально** и при запуске **в Docker** результаты всегда лежат в одной и той же директории `allure-results` в корне проекта;
- команды для генерации и просмотра отчётов (`allure generate`, `allure serve`) остаются такими же, как описано выше.

### Просмотр консольного вывода контейнеров

- онлайн-логирование:

```bash
docker compose -f docker/selenium-standalone-chrome-and-python-tests-docker-compose.yml logs -f tests
```

- просмотр логов всех сервисов:

```bash
docker compose -f docker/selenium-standalone-chrome-and-python-tests-docker-compose.yml logs -f
```

### Сохранение возможности локального запуска

Локальный запуск тестов **не изменён**:

- по-прежнему можно запускать:
  - `pytest ./tests -v` (Linux / macOS)
  - `pytest .\tests -v` (Windows)
- Allure по‑прежнему пишет результаты в `allure-results` за счёт настройки в `pytest.ini`;
- Docker-конфигурация влияет только на запуск тестов внутри контейнеров и не мешает локальному запуску.