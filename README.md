# 📄 AI Resume Analyzer

This is a web-based tool that analyzes resumes based on a provided job description. It uses OpenAI or a local LLM via Ollama (like `gemma3:1b`) to provide suggestions, score resumes, and generate downloadable improved versions.

## 🚀 Features
- Upload Resume (`.pdf` or `.docx`) and Job Description
- Choose between OpenAI and Ollama (local LLM)
- Generates:
  - Suggestions to improve your resume
  - Percentage match using semantic similarity
  - Optional ATS score (Before & After)
- No user data is stored

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **LLM**: OpenAI or Ollama (LLaMA 3, Mistral, etc.)
- **Dockerized**
- **CI**: GitHub Actions + PyTest

## ⚙️ Setup Instructions

### 🔧 Prerequisites
- Python 3.10+
- `pip`
- Docker & Docker Compose (optional)
- [Ollama](https://ollama.com/) (for local LLM model)

### 1. 🔑 Setup `.env`
Create a `.env` file:
```env
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-3.5-turbo
LLM_PROVIDER=ollama # or openai
```

### 2. 🐍 Local Installation
```bash
git clone https://github.com/jramnai/ai-resume-analyzer
cd ai-resume-analyzer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. 🤖 Run the app (manually)
```bash
# Start backend
uvicorn backend.main:app --reload

# In a separate terminal
streamlit run frontend/app.py
```

## 🐳 Run with Docker
```bash
docker-compose up --build
```

Access:
- Frontend: http://localhost:8501
- Backend: http://localhost:8000

## ✅ Run Tests
```bash
pytest
```

## 🔐 Secrets
- Store secrets in `.env`
- Do **not** commit `.env`

## 🔁 Running Locally with Ollama
Ollama is a free and open-source LLM runner for local inference.

### 1. Install Ollama
Visit https://ollama.com/download and install for your OS (macOS, Linux, Windows)

### 2. Pull and run a model (e.g., Gemma3:1b)
```bash
ollama pull Gemma3:1b
ollama run Gemma3:1b
```
You can also try others like:
```bash
ollama pull llama3
ollama pull mistral
```

### 3. Confirm it works
Ollama should be running on `http://localhost:11434` by default.

### 4. Update `.env`
```bash
LLM_PROVIDER=ollama
```

Now the app will use your local LLM instead of OpenAI.

## 📦 Files
- `backend/main.py`: FastAPI endpoints
- `backend/utils.py`: Resume processing logic
- `frontend/app.py`: Streamlit UI

## Contribution
- PRs require all tests passing
- Code coverage tracked via CI

---

## 📜 License
MIT
