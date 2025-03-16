# 1. Dev env
## 1.1 Create env
`python -m venv venv`
## 1.2 Activate
`venv/Scripts/activate`
## 1.3 install requirements
`pip install -r requirements.txt`
# 2. Create .env file:
Put inside:
* MODEL=ollama/llama3:latest
* API_BASE=http://127.0.0.1:11434
* CREWAI_TELEMETRY=disabled
* EXA_API_KEY=EXA_API_KEY
# 3. run code:
You have to get Ollama model before. And change the crew.py file to put Ollama provider instead.
`python code/src/news_podcast/main.py`