import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table

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
                f'[bold]Транскрипция:[/bold] [green]{escape(str(transcription))}[/green]',
                title=f'[bold cyan]{escape(str(word))}[/bold cyan]',
                border_style='blue', )
        )

        table = Table(
            header_style='bold cyan',
            border_style='blue',
            show_lines=True,
            expand=True,
        )
        table.add_column('Часть речи', no_wrap=True)
        table.add_column('Определение', ratio=2)
        table.add_column('Пример', ratio=1)

        related_terms = []
        for meaning in entry.get('meanings', []):
            part_of_speech = str(meaning.get('partOfSpeech', 'не указана'))
            definitions = meaning.get('definitions', [])

            if not definitions:
                table.add_row(escape(part_of_speech), 'не указано', 'нет данных')

            for number, item in enumerate(definitions[:3], start=1):
                definition = str(item.get('definition', 'не указано'))
                example = str(item.get('example') or 'нет данных')
                table.add_row(
                    escape(part_of_speech),
                    f'{number}. {escape(definition)}',
                    escape(example),
                )

                synonyms = item.get('synonyms', [])
                antonyms = item.get('antonyms', [])
                if synonyms or antonyms:
                    related_terms.append((part_of_speech, number, synonyms, antonyms))

        if table.row_count:
            console.print(table)

        for part_of_speech, number, synonyms, antonyms in related_terms:
            label = f'{escape(part_of_speech)}, определение {number}'
            if synonyms:
                console.print(f'Синонимы ({label}): {escape(", ".join(synonyms))}')
            if antonyms:
                console.print(f'Антонимы ({label}): {escape(", ".join(antonyms))}')


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
