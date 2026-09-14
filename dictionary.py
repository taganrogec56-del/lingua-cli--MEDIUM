import requests
from requests.exceptions import RequestException


def get_word_info(word: str):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    response = requests.get(url, timeout=40)
    response.raise_for_status()
    data = response.json()
    return data



if __name__ == '__main__':
    try:
        data = get_word_info('hello')
    except RequestException as error:
        print(error)
    else:
        for entry in data:
            for meaning in entry.get('meanings', []):
                print(f"Часть речи: {meaning.get('partOfSpeech', 'не указана')}")
                definitions = meaning.get('definitions', [])

                for item in definitions[:3]:
                    print(f"  Определение: {item.get('definition', 'не указано')}")
                    example = item.get('example')
                    if example:
                        print(f'  Пример: {example}')
                    else:
                        print('  Нет данных')

                    synonyms = item.get('synonyms', [])
                    if synonyms:
                        print(f'  Синонимы: {', '.join(synonyms)}')
                    else:
                        print('  Синонимы: нет данных')

                    antonyms = item.get('antonyms', [])
                    if antonyms:
                        print(f'  Антонимы: {', '.join(antonyms)}')
                    else:
                        print('  Антонимы: нет данных')