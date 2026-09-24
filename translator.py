import requests
from requests.exceptions import (
    Timeout,
    ConnectionError,
    HTTPError,
    RequestException,
    JSONDecodeError,
)
from config import REQUEST_TIMEOUT, get_translator_api_key

TRANSLATE_URL = 'https://api-free.deepl.com/v2/translate'


def run_translate_command(text: str, lang: str) -> None:
    text = text.strip()
    if not text:
        print('Пустой текст для перевода. Запрос приостановлен.')
        return
    lang = lang.strip().upper()
    if not lang:
        print('Пустой язык для перевода. Запрос приостановлен.')
        return

    try:
        translated_text, source_language = translate_text(text, lang)
    except Timeout:
        print('Ошибка: сервер слишком долго отвечает.')
    except ConnectionError:
        print('Ошибка: не удалось подключиться к серверу.')
        print('Проверьте интернет-соединение.')
    except HTTPError as error:
        status_code = (
            error.response.status_code
            if error.response is not None
            else None
        )
        if status_code is None:
            print('Ошибка HTTP: не удалось определить код ответа.')
        elif status_code in (401, 403):
            print('Ошибка авторизации API. Проверьте ключ в .env.')
        elif status_code == 400:
            print('Ошибка: проверьте параметры перевода и код языка.')
        elif status_code == 429:
            print('Ошибка: слишком много запросов. Попробуйте позже.')
        elif status_code == 456:
            print('Ошибка: исчерпан лимит символов DeepL.')
        elif status_code >= 500:
            print('Ошибка: сервер перевода временно недоступен.')
        else:
            print(f'Ошибка HTTP: код {status_code}.')
    except JSONDecodeError:
        print('Ошибка: сервер вернул некорректный JSON.')
    except ValueError as error:
        print(f'Ошибка: {error}')
    except RequestException:
        print('Ошибка: не удалось выполнить запрос на перевод.')
    else:
        print(f'Перевод с {source_language} на {lang}')
        print(f'Текст перевода: {translated_text}')


def translate_text(text: str, target_language: str) -> tuple[str, str]:
    api_key = get_translator_api_key()
    if api_key is None:
        raise ValueError('API-ключ переводчика не найден')
    headers = {
        'Authorization': f'DeepL-Auth-Key {api_key}',
        'Content-Type': 'application/json',
    }
    payload = {
        'text': [text],
        'target_lang': target_language.upper(),
    }
    response = requests.post(
        TRANSLATE_URL,
        headers=headers,
        json=payload,
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    data: dict = response.json()

    translations = data.get('translations', [])

    if not translations:
        raise ValueError('API не вернул результат перевода')

    translation = translations[0]
    translated_text = translation.get('text')
    source_language = translation.get('detected_source_language')

    if not translated_text or not source_language:
        raise ValueError('Ответ API не содержит необходимых данных')

    return translated_text, source_language
