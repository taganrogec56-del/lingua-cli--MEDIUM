import argparse
from dictionary import run_word_command
from translator import run_translate_command


def main():
    parser = argparse.ArgumentParser(
        prog='lingua-cli',
        description='Lingua CLI — переводчик текста и словарь английских слов'
    )
    subparser = parser.add_subparsers(
        dest='command', required=True
    )
    word_parser = subparser.add_parser(
        'word',
        help='Найти информацию об английском слове'
    )
    word_parser.add_argument(
        'word',
        help='Английское слово для поиска',
    )
    translate_parser = subparser.add_parser(
        'translate',
        help='Перевести текст'
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

    args = parser.parse_args()

    if args.command == 'word':
        run_word_command(args.word)
    elif args.command == 'translate':
        run_translate_command(args.text, args.to)


if __name__ == '__main__':
    main()
