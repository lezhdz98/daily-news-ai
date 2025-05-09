

# 📰 Daily News Browser AI Agent

The **Daily News Browser AI Agent** is a Streamlit-powered application that leverages the [`browser-use`](https://github.com/browser-use/browser-use) Python package to autonomously browse the web, gather real-time news, and generate concise summaries. The app highlights the top news of the day and allows you to download a full summary as a PDF for offline reading.

Using the `browser-use` package, the AI agent mimics human-like web behavior by autonomously clicking links, reading pages, and collecting relevant headlines each day. This makes it an efficient tool for anyone looking to stay updated with the latest news.
## Features

- Automatically browses top news sources using `browser-use`
- Summarizes key news in the format selected by the user
- AI-powered agent mimics human-like web exploration
- Download a summary of the day’s news as a PDF
- Clean Streamlit interface
## Installation
### Requirements

- Python 3.12.7
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/#installation-methods) for virtual environment management
- **OpenAI API Key**: You'll need to obtain an OpenAI API key and store it in the `.env` file for authentication purposes.
### Setup Instructions
1. **Clone the repository**

```bash
git clone https://github.com/lezhdz98/daily-news-ai.git 
cd daily-news-ai
```

2. **Install `uv` for virtual environment management:**
#### For macOS:
You have two options to install `uv`:
- **Option 1: Use `curl` to download the script and execute it with `sh`**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
- **Option 2: Install via Homebrew**

```bash
brew install uv
```
#### For Windows:

```bash
pip install uv
```

3. **Create a virtual environment using `uv`**

```bash
uv venv --python python3.12 
source .env/bin/activate # For macOS/Linux
.venv\Scripts\activate # For Windows
```  

4. **Install dependencies using `uv`**
  
```bash
uv pip install -r requirements.txt
```

5. **Create the `.env` file** in the root directory of the project and add your OpenAI API key:

```bash
OPENAI_API_KEY=your_openai_api_key
```

## Run Application

**Run the Streamlit app**

```bash
streamlit run frontend/dashboard.py
```