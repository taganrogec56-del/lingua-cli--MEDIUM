import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException
from rich.console import Console
from rich.panel import Panel

from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

console = Console(
    force_terminal=True,
    color_system='truecolor',
)


def get_word_info(word: str) -> list[dict]:
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


def display_word_info(data_from_api: list[dict]) -> None:
    for entry in data_from_api:
        word = entry.get('word', 'Написание слова отсутствует')

        phonetic_text = get_transcription(entry)
        transcription = phonetic_text or 'Нет данных'

        console.print(
            Panel.fit(
                f'[bold]Транскрипция:[/bold] [green]{transcription}[/green]',
                title=f'[bold cyan]{word}[/bold cyan]',
                border_style='blue', )
        )

        for meaning in entry.get('meanings', []):
            console.print(f"[bold]Часть речи:[/bold] {meaning.get('partOfSpeech', 'не указана')}")
            definitions = meaning.get('definitions', [])

            for item in definitions[:3]:
                console.print(f"  [italic]Определение:[/italic] {item.get('definition', 'не указано')}")
                example = item.get('example') or 'нет данных'
                if example:
                    console.print(f'  Пример: {example}')

                synonyms = item.get('synonyms', [])
                if synonyms:
                    console.print(f'  Синонимы: {", ".join(synonyms)}')
                else:
                    console.print('  Синонимы: нет данных')

                antonyms = item.get('antonyms', [])
                if antonyms:
                    console.print(f'  Антонимы: {", ".join(antonyms)}')
                else:
                    console.print('  Антонимы: нет данных')


def run_word_command(word: str) -> None:
    try:
        with Progress(
                SpinnerColumn(
                    spinner_name='dots',
                    style='bold cyan',
                ),
                TextColumn(
                    '[bold cyan]Ожидание ответа сервера...[/bold cyan]'
                ),
                TimeElapsedColumn(),
                console=console,
                transient=True,
        ) as progress:
            progress.add_task('request', total=None)
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
