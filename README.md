# 🧠 Capital Compass Backend

This is the FastAPI backend for **Capital Compass**, which processes PDF files and returns summarized, structured insights using the OpenAI API.

---

## 🚀 Getting Started

### 📦 Requirements

- Python 3.9+
- pip
- virtualenv (recommended)

---

### ⚙️ Installation

Clone the repo and set up the virtual environment:

```bash
git clone https://github.com/kanishka-lamba/capital-compass-backend.git
cd capital-compass-backend
python -m venv venv
venv\Scripts\activate         # On Windows
# or
source venv/bin/activate     # On macOS/Linux

pip install -r requirements.txt
```

---

### 🔐 Environment Setup

Create a `.env` file in the root of the backend directory and add your own OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

> 🔑 You must use your own OpenAI API key. Sign up at [https://platform.openai.com](https://platform.openai.com).

---

### 🧪 Running the API Server

```bash
uvicorn main:app --reload
```

The backend will be available at: [http://localhost:8000](http://localhost:8000)

---

### 📤 API Endpoint

**POST** `/process_pdf/`

- Accepts: `multipart/form-data` (PDF file)
- Returns: JSON with summarized insights

---

## 📁 .gitignore

Make sure your `.env` and `venv/` folders are excluded:

```
venv/
.env
__pycache__/
```

---

## 👤 Author

Developed by Kanishka Lamba

GitHub: [https://github.com/kanishka-lamba](https://github.com/kanishka-lamba)
