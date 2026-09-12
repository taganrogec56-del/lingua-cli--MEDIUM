# Техническое задание: Lingua CLI — терминальный переводчик и словарь

## 1. Цель проекта

Создать консольное Python-приложение для перевода слов и фраз, а также получения словарной информации об английских словах.

Программа должна работать через команды терминала, обращаться к внешним API по HTTP, получать данные в формате JSON и красиво отображать результат в консоли.

Основные возможности:

- перевод слов и целых фраз;
- выбор языка перевода;
- автоматическое определение исходного языка;
- получение транскрипции английского слова;
- получение части речи;
- получение определений;
- получение примеров использования;
- получение синонимов и антонимов;
- обработка HTTP-ошибок;
- безопасное хранение API-ключа;
- красивый вывод через `rich`.

Проект должен показать умение работать с:

```text
HTTP
REST API
JSON
requests
argparse
python-dotenv
rich
```

---

## 2. Название проекта

Рекомендуемое название репозитория:

```text
lingua-cli
```

В дальнейшем приложение можно превратить в полноценную CLI-команду:

```bash
lingua translate "Hello world" --to ru
lingua word hello
```

В основной версии запуск выполняется так:

```bash
python main.py
```

---

## 3. Используемые API

Приложение должно использовать два внешних API.

### API №1 — сервис перевода

Для перевода текста использовать API переводчика, например DeepL API или аналогичный сервис с API-ключом.

Он отвечает за:

- перевод текста;
- определение исходного языка;
- перевод фраз и предложений.

### API №2 — Free Dictionary API

Использовать словарный API для английских слов.

Он отвечает за:

- транскрипцию;
- фонетику;
- часть речи;
- определения;
- примеры;
- синонимы;
- антонимы;
- при наличии — ссылку на аудио произношения.

---

## 4. Структура проекта

```text
lingua-cli/
│
├── main.py
├── translator.py
├── dictionary.py
├── config.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

Назначение файлов:

```text
main.py
```

- обработка аргументов командной строки;
- выбор команды;
- запуск нужной функции;
- вывод результата.

```text
translator.py
```

- работа с API переводчика;
- HTTP-запрос;
- обработка ответа;
- возврат результата перевода.

```text
dictionary.py
```

- работа со словарным API;
- поиск слова;
- разбор JSON;
- получение транскрипции, значений, примеров и синонимов.

```text
config.py
```

- загрузка переменных окружения;
- чтение API-ключа;
- настройки приложения.

---

## 5. Установка зависимостей

Проект должен использовать:

```text
requests
python-dotenv
rich
```

Установка:

```bash
pip install requests python-dotenv rich
```

Создать файл:

```text
requirements.txt
```

с содержимым:

```text
requests
python-dotenv
rich
```

---

## 6. Скрытие API-ключа

API-ключ запрещено записывать прямо в Python-код.

Плохо:

```python
API_KEY = "abc123secret"
```

Правильно — хранить ключ в:

```text
.env
```

Пример:

```env
TRANSLATOR_API_KEY=your_real_api_key
```

В Python:

```python
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("TRANSLATOR_API_KEY")
```

---

## 7. Файл `.gitignore`

Файл `.env` обязательно добавить в:

```text
.gitignore
```

Минимальный вариант:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

API-ключ не должен попадать в GitHub.

---

## 8. Файл `.env.example`

В репозитории должен находиться:

```text
.env.example
```

Пример:

```env
TRANSLATOR_API_KEY=your_api_key_here
```

Настоящего ключа в нём быть не должно.

---

## 9. Интерфейс через argparse

Вместо обычного `input()` основные команды должны передаваться через аргументы терминала.

Использовать:

```python
import argparse
```

Программа должна поддерживать минимум две команды:

```text
translate
word
```

---

## 10. Команда `translate`

Пример запуска:

```bash
python main.py translate "Hello world" --to ru
```

Где:

```text
translate
```

— команда перевода;

```text
"Hello world"
```

— текст;

```text
--to ru
```

— язык результата.

---

## 11. Примеры команды translate

```bash
python main.py translate "Hello world" --to ru
python main.py translate "Как дела?" --to en
python main.py translate "Ich liebe Python" --to ru
```

---

## 12. Результат перевода

Использовать библиотеку:

```python
rich
```

Пример:

```text
╭──────────── Translation ────────────╮
│ Source: Hello world                │
│ Translation: Привет, мир           │
│ Language: EN → RU                  │
╰────────────────────────────────────╯
```

Можно использовать:

```python
from rich.console import Console
from rich.panel import Panel
```

---

## 13. Автоматическое определение языка

Если API поддерживает определение исходного языка, пользователь не должен обязательно указывать его вручную.

Например:

```bash
python main.py translate "Bonjour" --to ru
```

Программа должна показать, например:

```text
FR → RU
```

---

## 14. Команда `word`

Команда предназначена для получения словарной информации об английском слове.

Пример:

```bash
python main.py word hello
```

---

## 15. Результат команды word

Пример:

```text
╭──────────── hello ─────────────╮
│ Transcription: /həˈləʊ/       │
╰────────────────────────────────╯

Part of speech:
noun / verb / adjective / ...

Definition:
...

Example:
...

Synonyms:
...

Antonyms:
...
```

Если API возвращает несколько значений, необходимо показать несколько.

---

## 16. Структура словарного ответа

API может возвращать сложный JSON.

Примерная логика:

```text
response
│
├── word
├── phonetics
│   ├── text
│   └── audio
│
└── meanings
    ├── partOfSpeech
    └── definitions
        ├── definition
        ├── example
        ├── synonyms
        └── antonyms
```

Задача проекта — научиться безопасно работать с вложенными структурами JSON.

---

## 17. Получение транскрипции

Если API возвращает транскрипцию, вывести:

```text
Transcription: /ˈpʌɪθ(ə)n/
```

Если транскрипции нет:

```text
Transcription: not available
```

---

## 18. Части речи

Если слово имеет несколько частей речи, желательно вывести каждую отдельно.

Например:

```text
Noun
Definition: ...

Verb
Definition: ...
```

---

## 19. Определения

Выводить минимум одно определение.

Для основной версии достаточно максимум 3 определения на одну часть речи.

---

## 20. Примеры использования

Если API возвращает пример:

```text
Example:
She gave me a beautiful smile.
```

Если примера нет:

```text
Example: not available
```

---

## 21. Синонимы и антонимы

Если данные есть:

```text
Synonyms:
nice, attractive, lovely
```

```text
Antonyms:
ugly, unpleasant
```

Если данных нет, программа должна вывести понятное сообщение или не отображать пустой блок.

---

## 22. HTTP-запросы

Для запросов использовать:

```python
import requests
```

Примерная структура:

```python
response = requests.get(
    url,
    params=params,
    headers=headers,
    timeout=10
)
```

или:

```python
requests.post(...)
```

в зависимости от выбранного API.

Обязательно использовать `timeout`.

---

## 23. Обработка JSON

После успешного запроса:

```python
data = response.json()
```

Затем разобрать необходимые поля.

Не выводить пользователю весь необработанный JSON.

---

## 24. Проверка HTTP-статуса

Нужно понимать и обрабатывать:

```text
200 — запрос выполнен успешно
400 — неправильный запрос
401 — неправильный или отсутствующий API-ключ
403 — доступ запрещён
404 — ресурс или слово не найдено
429 — превышен лимит запросов
500+ — ошибка сервера
```

Можно использовать:

```python
response.raise_for_status()
```

Пользователь должен получать понятное сообщение, а не traceback.

---

## 25. Обработка сетевых ошибок

Предусмотреть:

```python
requests.exceptions.Timeout
requests.exceptions.ConnectionError
requests.exceptions.RequestException
```

Пример:

```text
Ошибка: не удалось подключиться к серверу.
Проверьте интернет-соединение.
```

При таймауте:

```text
Ошибка: сервер слишком долго отвечает.
```

---

## 26. Отсутствующий API-ключ

Если:

```python
os.getenv("TRANSLATOR_API_KEY")
```

возвращает `None`, вывести:

```text
Ошибка: API-ключ переводчика не найден.

Создайте файл .env и добавьте:

TRANSLATOR_API_KEY=your_api_key
```

---

## 27. Неверный API-ключ

Если сервер возвращает ошибку авторизации, вывести:

```text
Ошибка авторизации API.
Проверьте ключ в файле .env.
```

---

## 28. Слово не найдено

Если пользователь вводит:

```bash
python main.py word asdfghjkl
```

вывести:

```text
Слово "asdfghjkl" не найдено.
```

---

## 29. Пустой текст

Команда:

```bash
python main.py translate "" --to ru
```

не должна отправлять запрос.

Вывести:

```text
Ошибка: текст для перевода пуст.
```

---

## 30. Проверка языка

Если пользователь вводит неподдерживаемый язык, программа должна вывести понятную ошибку.

Допустимо:

- проверять язык самостоятельно;
- корректно обработать ответ API.

---

## 31. Дополнительная команда languages

Можно добавить:

```bash
python main.py languages
```

Она может выводить:

```text
EN — English
RU — Russian
DE — German
FR — French
ES — Spanish
...
```

Это необязательная функция основной версии.

---

## 32. Использование rich

Минимально использовать:

```python
Console
Panel
Table
```

Словарные значения удобно показывать таблицей.

---

## 33. Требования к `translator.py`

Рекомендуемые функции:

```python
translate_text()
build_translate_request()
parse_translate_response()
```

Минимально достаточно:

```python
translate_text(text, target_language)
```

Функция должна:

1. получить текст;
2. отправить HTTP-запрос;
3. проверить ответ;
4. получить JSON;
5. вернуть перевод и исходный язык.

---

## 34. Требования к `dictionary.py`

Рекомендуемые функции:

```python
get_word_info()
get_transcription()
get_meanings()
get_synonyms()
get_antonyms()
```

Главное — не помещать весь код разбора словаря в `main.py`.

---

## 35. Требования к `config.py`

Файл должен:

1. загрузить `.env`;
2. получить API-ключ;
3. хранить общие настройки.

---

## 36. Требования к `main.py`

В `main.py` должны находиться:

- настройка `argparse`;
- команды;
- аргументы;
- вызов функций из других модулей;
- отображение результата.

HTTP-логика должна находиться в отдельных модулях.

---

## 37. Subcommands в argparse

Нужно изучить:

```python
add_subparsers()
```

Архитектура CLI:

```text
main.py
│
├── translate
│   ├── text
│   └── --to
│
└── word
    └── word
```

---

## 38. Справка CLI

Команда:

```bash
python main.py --help
```

должна выводить понятную справку.

Также должна работать:

```bash
python main.py translate --help
```

---

## 39. Точка входа

Использовать:

```python
def main():
    ...
```

и:

```python
if __name__ == "__main__":
    main()
```

---

## 40. Что нужно изучить в проекте

Необходимо закрепить:

- HTTP;
- REST API;
- GET;
- POST;
- headers;
- query parameters;
- request body;
- HTTP status codes;
- JSON;
- вложенные словари;
- вложенные списки;
- `requests`;
- `response.json()`;
- `response.status_code`;
- `response.raise_for_status()`;
- `timeout`;
- исключения `requests`;
- `.env`;
- переменные окружения;
- `os.getenv()`;
- `python-dotenv`;
- `.gitignore`;
- `argparse`;
- subcommands;
- `rich`;
- импорты между собственными модулями.

---

## 41. Что пока не использовать

В основной версии не нужны:

- классы;
- ООП;
- SQLite;
- PostgreSQL;
- Flask;
- Django;
- FastAPI;
- GUI;
- асинхронность;
- многопоточность.

Основная задача проекта:

```text
научиться работать с внешними API
```

---

## 42. README.md

README должен содержать:

```markdown
# Lingua CLI

Terminal translator and English dictionary written in Python.

## Features

- text translation;
- automatic source language detection;
- English word definitions;
- phonetic transcription;
- examples;
- synonyms;
- antonyms;
- beautiful terminal output.

## Installation

pip install -r requirements.txt

## Configuration

Create `.env`:

TRANSLATOR_API_KEY=your_api_key

## Usage

python main.py translate "Hello world" --to ru

python main.py word hello
```

---

## 43. Примеры использования в README

```bash
python main.py translate "Hello world" --to ru
python main.py translate "Как дела?" --to en
python main.py word programming
python main.py word beautiful
```

---

## 44. Безопасность репозитория

Перед `git push` проверить:

```bash
git status
```

В GitHub не должны попасть:

```text
.env
API keys
tokens
passwords
```

В репозитории должен быть:

```text
.env.example
```

---

## 45. Дополнительные задания

### Уровень 1 — выбор количества определений

```bash
python main.py word run --limit 5
```

### Уровень 2 — аудио произношения

Если API возвращает ссылку на аудио, отображать её.

### Уровень 3 — история переводов

Сохранять последние запросы в:

```text
history.json
```

### Уровень 4 — команда history

```bash
python main.py history
```

### Уровень 5 — очистка истории

```bash
python main.py history --clear
```

### Уровень 6 — перевод из файла

```bash
python main.py translate-file article.txt --to ru
```

Результат сохранять в новый `.txt` файл.

### Уровень 7 — интерактивный режим

```bash
python main.py interactive
```

### Уровень 8 — установка как настоящей CLI-команды

После упаковки проекта:

```bash
pip install .
```

можно получить:

```bash
lingua translate "Hello world" --to ru
```

---

## 46. Обязательные тестовые сценарии

### Тест 1

```bash
python main.py translate "Hello world" --to ru
```

### Тест 2

```bash
python main.py translate "Как дела?" --to en
```

### Тест 3

```bash
python main.py word hello
```

### Тест 4

```bash
python main.py word programming
```

### Тест 5

Отключить интернет.

Программа должна вывести понятное сообщение об ошибке соединения.

### Тест 6

Удалить API-ключ из `.env`.

Программа должна объяснить, что ключ не найден.

### Тест 7

Указать неправильный API-ключ.

Программа должна корректно обработать ошибку авторизации.

### Тест 8

```bash
python main.py word asdfghjkl
```

Программа должна сообщить, что слово не найдено.

### Тест 9

Передать неподдерживаемый язык.

Программа не должна завершаться с traceback.

### Тест 10

```bash
python main.py --help
```

Справка должна быть понятной.

---

## 47. Критерии готовности

Проект считается завершённым, если:

- приложение запускается из терминала;
- используется `argparse`;
- есть команды `translate` и `word`;
- перевод работает через внешний API;
- словарь работает через внешний API;
- HTTP выполняется через `requests`;
- JSON корректно разбирается;
- исходный язык определяется автоматически, если это поддерживает API;
- транскрипция отображается корректно;
- определения отображаются корректно;
- примеры обрабатываются;
- синонимы обрабатываются;
- API-ключ хранится в `.env`;
- `.env` находится в `.gitignore`;
- есть `.env.example`;
- сетевые ошибки обрабатываются;
- HTTP-ошибки не приводят к traceback для пользователя;
- используется `timeout`;
- вывод оформлен через `rich`;
- проект разделён на несколько модулей;
- есть `requirements.txt`;
- есть качественный `README.md`;
- секретные данные не попали в GitHub.

---

## 48. Итоговая архитектура

```text
                     ┌──────────────────────┐
                     │       main.py        │
                     │      argparse        │
                     └──────────┬───────────┘
                                │
                  ┌─────────────┴─────────────┐
                  │                           │
             translate                      word
                  │                           │
                  ▼                           ▼
        ┌─────────────────┐        ┌─────────────────┐
        │  translator.py  │        │  dictionary.py  │
        └────────┬────────┘        └────────┬────────┘
                 │                          │
                 ▼                          ▼
        Translation API          Free Dictionary API
                 │                          │
                 └──────────┬───────────────┘
                            ▼
                          JSON
                            │
                            ▼
                     Python objects
                            │
                            ▼
                          rich
                            │
                            ▼
                      Terminal output
```

---

## 49. Результат

После выполнения проекта должна получиться полноценная терминальная утилита, которой можно пользоваться в повседневной работе.

Проект показывает следующий рост навыков:

```text
Python
↓
модули
↓
CLI / argparse
↓
HTTP
↓
REST API
↓
requests
↓
JSON
↓
API authentication
↓
.env
↓
обработка сетевых ошибок
↓
rich
↓
структура реального небольшого приложения
```

Это пятый проект Python-портфолио:

```text
1. Expense Tracker
2. Task Manager с JSON
3. Анализатор текста
4. Организатор файлов
5. Lingua CLI — переводчик и словарь
```
