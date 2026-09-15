import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException


def get_word_info(word: str):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    response = requests.get(url, timeout=40)
    response.raise_for_status()
    data_word = response.json()
    return data_word


def get_transcription(entry_dict: dict) -> str | None:
    phonetic = entry_dict.get('phonetic')
    if phonetic:
        return phonetic
    phonetics = entry_dict.get('phonetics', [])
    for item_phonetic in phonetics:
        text = item_phonetic.get('text')
        if text:
            return text
    return None


def display_word_info(data_from_api) -> None:
    for entry in data_from_api:
        phonetic_text = get_transcription(entry)
        if phonetic_text:
            print(f'Транскрипция: {phonetic_text}')
        else:
            print('Транскрипция: нет данных')

        for meaning in entry.get('meanings', []):
            print(f"Часть речи: {meaning.get('partOfSpeech', 'не указана')}")
            definitions = meaning.get('definitions', [])

            for item in definitions[:3]:
                print(f"  Определение: {item.get('definition', 'не указано')}")
                example = item.get('example')
                if example:
                    print(f'  Пример: {example}')
                else:
                    print('  Пример: нет данных')

                synonyms = item.get('synonyms', [])
                if synonyms:
                    print(f'  Синонимы: {", ".join(synonyms)}')
                else:
                    print('  Синонимы: нет данных')

                antonyms = item.get('antonyms', [])
                if antonyms:
                    print(f'  Антонимы: {", ".join(antonyms)}')
                else:
                    print('  Антонимы: нет данных')


def run_word_command(word: str) -> None:
    try:
        data = get_word_info(word)
    except Timeout:
        print('Ошибка: сервер слишком долго отвечает.')
    except ConnectionError:
        print('Ошибка: не удалось подключиться к серверу.')
        print('Проверьте интернет-соединение.')
    except HTTPError as error:
        if error.response is not None and error.response.status_code == 404:
            print(f'Слово "{word}" не найдено.')
        else:
            status_code = (
                error.response.status_code
                if error.response is not None
                else 'неизвестен'
            )
            print(f'Ошибка HTTP: код {status_code}.')
    except RequestException as error:
        print(f'Ошибка запроса: {error}')
    else:
        display_word_info(data)
