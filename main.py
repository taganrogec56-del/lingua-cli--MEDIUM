import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="lingua-cli",
        description='Lingua CLI — переводчик текста и словарь английских слов'
    )
    parser.parse_args()


if __name__ == '__main__':
    main()
