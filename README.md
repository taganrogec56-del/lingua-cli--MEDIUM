# Lingua CLI

English | [Русский](README.ru.md)

A Python command-line project for translating text and looking up English words.

## Project status

In development. The initial project setup and Python entry point are in place.
Command-line parsing, API integrations, and formatted output are planned and are
not implemented yet.

## Planned features

- Translate words and phrases into a selected language.
- Detect the source language through the translation API.
- Look up English definitions, phonetic transcriptions, and parts of speech.
- Display usage examples, synonyms, and antonyms when available.
- Format results with Rich panels and tables.
- Handle invalid input, missing API keys, HTTP errors, and network timeouts.

## Technology stack

- **Python** — application logic and modules.
- **argparse** — command-line arguments and subcommands; part of the standard library.
- **requests** — HTTP requests to external APIs.
- **python-dotenv** — loading local configuration from a `.env` file.
- **rich** — terminal output formatting.

The dictionary integration will use Free Dictionary API. The translation API
provider has not been selected yet.

## Local setup

From the project directory, run these commands in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

If `.venv` already exists, use the existing environment and skip its creation.

To run the current entry point:

```powershell
.\.venv\Scripts\python.exe main.py
```

At this stage, the entry point exits without producing output.

## Planned configuration

The translation integration will read `TRANSLATOR_API_KEY` from the environment
or a local `.env` file. Use `.env.example` as the configuration template:

```dotenv
TRANSLATOR_API_KEY=your_api_key_here
```

Keep the real key in `.env`, which is excluded from Git. The `.env.example`
template contains only a placeholder. Details for obtaining a key will be
added after the translation provider is selected.

## Planned usage

These commands describe the intended interface and are not functional yet:

```powershell
.\.venv\Scripts\python.exe main.py translate "Hello world" --to ru
.\.venv\Scripts\python.exe main.py word hello
.\.venv\Scripts\python.exe main.py --help
```

## Current project structure

```text
lingua-cli/
├── main.py              # Application entry point
├── .env.example         # Configuration template
├── .gitignore           # Local files excluded from Git
├── requirements.txt     # Third-party dependencies
├── lingua_cli_TZ.md      # Project specification in Russian
├── README.md            # Documentation in English
└── README.ru.md         # Documentation in Russian
```

As implementation progresses, `translator.py` and `dictionary.py` will handle
API access and response parsing, while `config.py` will handle configuration.
`main.py` will parse arguments, call the appropriate functions, and display results.

## Learning goals

This portfolio project focuses on HTTP APIs, JSON parsing, API authentication,
error handling, and organizing a small CLI application into Python modules.

See [the project specification](lingua_cli_TZ.md) for requirements and acceptance
scenarios.
