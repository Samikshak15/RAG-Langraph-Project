# Tokenization for Beginners

This project is a beginner-level introduction to tokenization for Generative AI.
Tokenization is the process of converting text into smaller pieces called tokens, which models use as input.

## What you will learn

- What tokenization means
- Why tokenization matters in generative AI
- Five tokenization styles, from simple to real-world:
  - Whitespace tokenization
  - Character tokenization
  - Simple subword tokenization
  - BERT tokenization (Hugging Face `transformers`)
  - GPT tokenization (OpenAI `tiktoken`)
- How to compare token counts across tokenizers, and how that relates to LLM API cost

## Files

- `src/tokenization_demo.py` - Tokenizer functions plus a CLI demo with sample output.
- `app.py` - Streamlit UI ("Tokenizer Playground") to interactively compare tokenizers.
- `requirements.txt` - Python dependencies for the demo and the app.

## Setup

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate it:

- Windows PowerShell:
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- Windows Command Prompt:
  ```cmd
  .venv\Scripts\activate.bat
  ```

3. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the demo (command line)

```bash
python src/tokenization_demo.py
```

## Run the Tokenizer Playground (Streamlit UI)

```bash
streamlit run app.py
```

This opens a browser app where you can type any text, pick a tokenizer
(Whitespace, Character, Simple Subword, BERT, or GPT), and see the tokens,
token count, token IDs, and an estimated API cost for GPT tokens.

## Notes

This project is designed for beginners. It explains tokenization with easy examples and clear output. You can use it as a learning base before exploring real tokenizer libraries like Hugging Face Transformers or tiktoken.
