# 🏥 Medical Recommendation Agent

An AI-powered medical recommendation system built with FastAPI and Ollama (llama3).

## Features
- Symptom-based medicine recommendations
- Doctor/specialist suggestions
- 20+ diseases supported
- Runs locally using free AI (Ollama)

## Tech Stack
- Python + FastAPI
- Ollama (llama3) - free local AI
- Jinja2 Templates

## How to Run Locally

### Step 1 - Install Ollama
Download from https://ollama.com/download

### Step 2 - Pull AI Model
ollama pull llama3

### Step 3 - Clone this repo
git clone https://github.com/Sailaja-Kalle/medical-agent.git
cd medical-agent

### Step 4 - Create virtual environment
py -m venv venv
venv\Scripts\activate

### Step 5 - Install packages
pip install fastapi uvicorn requests python-dotenv jinja2

### Step 6 - Run the app
uvicorn main:app --reload --host 0.0.0.0 --port 8000

### Step 7 - Open browser
http://localhost:8000