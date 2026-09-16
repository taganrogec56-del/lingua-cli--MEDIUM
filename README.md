# Lingua CLI

English | [Русский](README.ru.md)

A Python command-line project for translating text and looking up English words.

## Project status

In development. The English dictionary command is functional and uses the
[Free Dictionary API](https://dictionaryapi.dev/). The CLI packaging,
`argparse` subcommands, formatted Rich output, and request error handling are
also implemented.

The `translate` subcommand and its arguments are already available, but it
currently prints a placeholder instead of calling a translation API. Selecting
a translation provider and implementing `config.py` and `translator.py` are the
next milestones.

## Available features

- Run the application as `lingua-cli` or through `main.py`.
- Display help for the CLI and its subcommands.
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

## Planned features

- Translate words and phrases into a selected language.
- Detect the source language through the translation API.
- Load the translation API key from a local `.env` file.
- Validate empty input, unsupported languages, and translation API errors.
- Format translation results with Rich.

## Technology stack

- **Python** — application logic and modules.
- **argparse** — command-line arguments and subcommands; part of the standard library.
- **requests** — HTTP requests to external APIs.
- **python-dotenv** — planned loading of local configuration from `.env`.
- **rich** — panels, colors, and the request activity indicator.
- **Free Dictionary API** — English dictionary data.

The translation API provider has not been selected yet.

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

## Current usage

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

The translation interface already accepts the intended arguments:

```powershell
lingua-cli translate "Hello world" --to ru
```

However, this command currently prints a development placeholder and does not
perform a translation request yet.

## Planned configuration

The translation integration will read `TRANSLATOR_API_KEY` from the environment
or a local `.env` file. Use `.env.example` as the configuration template:

```dotenv
TRANSLATOR_API_KEY=your_api_key_here
```

Keep the real key in `.env`, which is excluded from Git. The `.env.example`
template contains only a placeholder. Instructions for obtaining a key will be
added after the translation provider is selected.

## Current project structure

```text
lingua-cli/
├── main.py              # Argument parsing and command dispatch
├── dictionary.py        # Dictionary API, response parsing, and Rich output
├── pyproject.toml       # Packaging metadata and CLI command
├── .env.example         # Translation configuration template
├── .gitignore           # Local files excluded from Git
├── requirements.txt     # Third-party dependencies
├── lingua_cli_TZ.md     # Project specification in Russian
├── README.md            # Documentation in English
└── README.ru.md         # Documentation in Russian
```

The planned `translator.py` module will handle translation API access and
response parsing. The planned `config.py` module will load the API key and
shared settings. `main.py` will then call the translator instead of the current
placeholder.

## Learning goals

This portfolio project focuses on HTTP APIs, JSON parsing, nested dictionaries
and lists, network error handling, CLI design, terminal formatting, environment
variables, and organizing a small Python application into modules.

See [the project specification](lingua_cli_TZ.md) for requirements and acceptance
scenarios.
