# Lingua CLI

English | [Русский](README.ru.md)

A Python command-line project for translating text and looking up English words.

## Project status

In development. The `word` command uses the
[Free Dictionary API](https://dictionaryapi.dev/), and `translate` sends requests
to the DeepL API Free endpoint. Both commands are available through `argparse`
and the installed `lingua-cli` command. Dictionary results use Rich; translation
results currently use plain text.

## Available features

- Run the application as `lingua-cli` or through `main.py`.
- Display help for the CLI and its subcommands.
- Translate words and phrases into a selected language through DeepL API Free.
- Show the source language detected by the translation API.
- Load the DeepL API key from a local `.env` file or an environment variable.
- Look up English words with `lingua-cli word <word>`.
- Display every dictionary entry returned for a word.
- Display phonetic transcription, parts of speech, and up to three definitions
  for each meaning.
- Display usage examples, synonyms, and antonyms, with fallback text when data
  is unavailable.
- Format dictionary output with Rich colors and panels.
- Show a spinner and elapsed time while waiting for the dictionary server.
- Handle timeouts, connection failures, general request errors, HTTP errors,
  and words that are not found.
- Handle missing translation API keys, empty translation input, invalid JSON,
  and common translation API errors.

## Planned features

- Format translation results with Rich.
- Complete the required manual test scenarios and improve guidance for missing
  API keys.

## Technology stack

- **Python** — application logic and modules.
- **argparse** — command-line arguments and subcommands; part of the standard library.
- **requests** — HTTP requests to external APIs.
- **python-dotenv** — loading local configuration from `.env`.
- **rich** — panels, colors, and the request activity indicator.
- **Free Dictionary API** — English dictionary data.
- **DeepL API Free** — text translation and source-language detection.

Translation requires a valid DeepL API Free key.

## Local setup

From the project directory, run these commands in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\Activate.ps1
```

If `.venv` already exists, use the existing environment and skip its creation.
The editable installation (`-e .`) installs the project and its dependencies
while keeping it linked to the source files. Repeat the installation after
changing packaging metadata.

With the environment activated, display the command-line help:

```powershell
lingua-cli --help
lingua-cli word --help
```

You can also run the application without activating the environment:

```powershell
.\.venv\Scripts\lingua-cli.exe --help
.\.venv\Scripts\lingua-cli.exe word hello
```

## Usage

Look up an English word:

```powershell
lingua-cli word hello
lingua-cli word programming
```

The same command can be run directly through Python when the environment is
activated:

```powershell
python main.py word hello
```

The dictionary command displays a Rich panel with the word and transcription,
followed by its parts of speech, definitions, examples, synonyms, and antonyms.
If the API returns several dictionary entries, all of them are processed.

Translate text into a selected language:

```powershell
lingua-cli translate "Hello world" --to ru
lingua-cli translate "Как дела?" --to en
```

The translation command sends a request to DeepL and prints the detected source
language, target language, and translated text. Its output is not yet formatted
with Rich.

## Configuration

Create a `.env` file in the project directory using `.env.example` as a template.
Put your DeepL API Free key in it:

```dotenv
TRANSLATOR_API_KEY=your_actual_deepl_key
```

The same variable can also be supplied through the environment. Keep the real
key in `.env`, which is excluded from Git; `.env.example` contains only a
placeholder. Without a key, the translation command reports an error. The word
command does not require a key.

## Current project structure

```text
lingua-cli/
├── main.py              # Argument parsing and command dispatch
├── dictionary.py        # Dictionary API, response parsing, and Rich output
├── translator.py        # DeepL request, response parsing, and error handling
├── config.py            # Environment loading and shared request timeout
├── pyproject.toml       # Packaging metadata and CLI command
├── .env.example         # Translation configuration template
├── .gitignore           # Local files excluded from Git
├── requirements.txt     # Third-party dependencies
├── lingua_cli_TZ.md     # Project specification in Russian
├── README.md            # Documentation in English
└── README.ru.md         # Documentation in Russian
```

`main.py` calls `run_word_command()` or `run_translate_command()` according to
the selected subcommand.

## Learning goals

This portfolio project focuses on HTTP APIs, JSON parsing, nested dictionaries
and lists, network error handling, CLI design, terminal formatting, environment
variables, and organizing a small Python application into modules.

See [the project specification](lingua_cli_TZ.md) for requirements and acceptance
scenarios.
