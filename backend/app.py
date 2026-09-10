"""Tokenizer Playground

A beginner-friendly Streamlit app that shows how the same text gets
broken into tokens by different tokenization methods.
"""

from __future__ import annotations

import streamlit as st

from src.tokenization_demo import (
    character_tokenizer,
    demo_gpt_tokenizer,
    demo_transformers_tokenizer,
    simple_subword_tokenizer,
    whitespace_tokenizer,
)

st.set_page_config(page_title="Tokenizer Playground", page_icon="🔤")

st.title("🔤 Tokenizer Playground")
st.write(
    "Type some text and see how different tokenizers break it down into "
    "tokens. Tokenization is the first step every language model takes "
    "before it can understand text."
)

text = st.text_area(
    "Enter text",
    value="Hello, world! Tokenization is the first step in generative AI.",
    height=100,
)

method = st.selectbox(
    "Choose a tokenizer",
    [
        "Whitespace",
        "Character",
        "Simple Subword",
        "BERT (Hugging Face)",
        "GPT (tiktoken)",
    ],
)

# Simple color palette to visually separate tokens
COLORS = ["#ffd6a5", "#caffbf", "#9bf6ff", "#a0c4ff", "#bdb2ff", "#ffc6ff", "#fdffb6"]


def render_tokens(tokens: list[str]) -> None:
    chips = ""
    for i, token in enumerate(tokens):
        color = COLORS[i % len(COLORS)]
        display = token if token.strip() else "·"
        chips += (
            f'<span style="background-color:{color}; color:#111; '
            f'padding:2px 6px; margin:2px; border-radius:6px; '
            f'display:inline-block; font-family:monospace;">{display}</span>'
        )
    st.markdown(chips, unsafe_allow_html=True)


if st.button("Tokenize", type="primary") and text.strip():
    if method == "Whitespace":
        tokens = whitespace_tokenizer(text)
        render_tokens(tokens)
        st.info(f"Token count: {len(tokens)}")

    elif method == "Character":
        tokens = character_tokenizer(text)
        render_tokens(tokens)
        st.info(f"Token count: {len(tokens)}")

    elif method == "Simple Subword":
        tokens = simple_subword_tokenizer(text)
        render_tokens(tokens)
        st.info(f"Token count: {len(tokens)}")

    elif method == "BERT (Hugging Face)":
        result = demo_transformers_tokenizer(text)
        if result is None:
            st.error("Hugging Face `transformers` is not installed. Run `pip install -r requirements.txt`.")
        else:
            tokens, ids = result
            render_tokens(tokens)
            st.info(f"Token count: {len(tokens)}")
            with st.expander("Token IDs"):
                st.code(str(ids))

    elif method == "GPT (tiktoken)":
        result = demo_gpt_tokenizer(text)
        if result is None:
            st.error("`tiktoken` is not installed. Run `pip install -r requirements.txt`.")
        else:
            tokens, ids = result
            render_tokens(tokens)
            st.info(f"Token count: {len(tokens)}")
            with st.expander("Token IDs"):
                st.code(str(ids))
            # Rough cost estimate using GPT-4o-mini style pricing ($0.15 / 1M input tokens)
            est_cost = (len(ids) / 1_000_000) * 0.15
            st.caption(f"Estimated input cost at $0.15 / 1M tokens: ${est_cost:.6f}")

st.divider()
st.caption(
    "Tip: try the same sentence with 'BERT' vs 'GPT' — different models "
    "use different tokenizers, so token counts (and API costs) differ."
)
