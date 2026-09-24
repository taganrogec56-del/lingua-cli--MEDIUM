import argparse
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from dictionary import run_word_command
from translator import run_translate_command


console = Console(force_terminal=True, color_system='truecolor')


def enable_rich_help(parser: argparse.ArgumentParser, title: str) -> None:
    original_print_help = parser.print_help

    def print_help(file=None) -> None:
        if file is not None:
            original_print_help(file)
            return
        console.print(
            Panel(
                Text(parser.format_help()),
                title=title,
                border_style='cyan',
            )
        )

    parser.print_help = print_help


def main():
    parser = argparse.ArgumentParser(
        prog='lingua-cli',
        description='Lingua CLI — переводчик текста и словарь английских слов',
        epilog=(
            'Примеры:\n'
            '  python main.py word hello\n'
            '  python main.py translate "Hello world" --to ru\n\n'
            'О возможной ошибке HTTP 522 см. python main.py word --help.'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparser = parser.add_subparsers(
        dest='command', required=True
    )
    word_parser = subparser.add_parser(
        'word',
        help='Найти информацию об английском слове',
        description='Получить транскрипцию, определения и примеры английского слова.',
        epilog=(
            'Пример: python main.py word hello\n\n'
            'HTTP 404: слово не найдено.\n'
            'HTTP 522: сервер словаря не ответил вовремя. Такое иногда бывает\n'
            'для редких или отсутствующих слов, но 522 не доказывает, что слово\n'
            'не найдено. Попробуйте позже.'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    word_parser.add_argument(
        'word',
        help='Английское слово для поиска',
    )
    translate_parser = subparser.add_parser(
        'translate',
        help='Перевести текст',
        description='Перевести текст через DeepL с определением исходного языка.',
        epilog=(
            'Пример: python main.py translate "Hello world" --to ru\n'
            'Для перевода нужен ключ DeepL в переменной TRANSLATOR_API_KEY.'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    translate_parser.add_argument(
        'text',
        help='Текст для перевода'
    )
    translate_parser.add_argument(
        '--to',
        required=True,
        help='Код языка перевода'
    )

    enable_rich_help(parser, 'Lingua CLI')
    enable_rich_help(word_parser, 'Команда word')
    enable_rich_help(translate_parser, 'Команда translate')

    args = parser.parse_args()

    if args.command == 'word':
        run_word_command(args.word)
    elif args.command == 'translate':
        run_translate_command(args.text, args.to)


if __name__ == '__main__':
    main()
