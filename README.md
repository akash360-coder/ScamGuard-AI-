# ScamGuard AI

ScamGuard AI is an explainable AI app for detecting scam messages using a Gemini-powered classification workflow and a Streamlit interface.

## Features

- Scam vs legitimate classification
- Scam type inference
- Red flag extraction and intent detection
- Confidence scoring
- Reasoning and explainability output
- Streamlit UI for quick analysis

## Project structure

```text
scamguard-ai/
├── app/
│   └── streamlit_app.py
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── llm_interface.py
│   ├── prompts.py
│   ├── classifier.py
│   ├── explainer.py
│   └── utils.py
├── tests/
│   ├── test_classifier.py
│   └── test_prompts.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── data/
    ├── test_samples.csv
    └── red_flags.json
```

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your API key:

```bash
copy .env.example .env
```

Then edit `.env` and set `GEMINI_API_KEY`.

## Run the app

```bash
streamlit run app/streamlit_app.py
```

## Run tests

```bash
pytest
```

## Notes

This project is structured for extension into a full LLM-based scam detection platform using modular architecture and prompt-based classification.
