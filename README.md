# Podcast Bot

A bot that allows you to pass in a YouTube URL to be transcribed, summarized, and you can follow up by asking the bot to clarify any parts of the transcript. This is built using Streamlit, Speechmatics Python SDK and Anthropic's Claude API.

## Getting Started

Install all the required Python dependencies with:

```
pip3 install -r requirements.txt
```

Define your Speechmatics and Anthropic API keys in `.streamlit/secrets.toml`:

```bash
SM_API_KEY = "XYZ"
ANTHROPIC_API_KEY = "ABC"
```

## Running

Start the app with

```bash
streamlit run app.py
```

## Docs

The Speechmatics Python SDK and CLI is documented at https://speechmatics.github.io/speechmatics-python.

The Speechmatics API and product documentation can be found at https://docs.speechmatics.com.
