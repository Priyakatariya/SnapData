# 🧠 Talk2Data AI

> **Ask your data anything — in plain English.**

Talk2Data AI is a full-stack AI-powered data analytics tool that converts natural language questions into SQL queries, executes them on your database, and presents results with visualizations and plain-English explanations — all powered by Google Gemini AI.

---

## ✨ Features

- 🗣️ **Natural Language to SQL** — Type a question; get a valid SQL query back instantly
- 🤖 **Gemini AI Powered** — Uses Google's `gemini-1.5-flash` model for fast, accurate SQL generation
- 📊 **Data Visualizations** — Results rendered as interactive charts and tables
- 🛡️ **Safety First** — Blocks dangerous queries (INSERT, UPDATE, DELETE, DROP); only SELECT allowed
- 📈 **Confidence Scoring** — AI rates its own confidence; low-confidence results are filtered out
- 💡 **Plain-English Explanations** — Every query result comes with a human-readable explanation
- 🔌 **Multi-Database Support** — Works with SQLite, PostgreSQL, and MySQL via SQLAlchemy

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js 14, TypeScript, CSS |
| **Backend** | FastAPI (Python), Uvicorn |
| **AI** | Google Gemini AI (`google-genai`) |
| **Database ORM** | SQLAlchemy |
| **Database** | SQLite (default) / PostgreSQL / MySQL |

---

## 📁 Project Structure

```
talk2data/
├── backend/
│   ├── main.py               # FastAPI app entry point
│   ├── requirements.txt      # Python dependencies
│   ├── setup_db.py           # Database setup script
│   ├── .env.example          # Environment variables template
│   ├── routers/
│   │   ├── query.py          # POST /api/query endpoint
│   │   └── schema.py         # GET /api/schema endpoint
│   ├── services/
│   │   ├── gemini_service.py # Gemini AI integration
│   │   └── db_service.py     # Database operations
│   └── models/
│       └── schemas.py        # Pydantic request/response models
└── frontend/
    ├── app/
    │   ├── page.tsx          # Main application page
    │   ├── layout.tsx        # Root layout
    │   └── globals.css       # Global styles
    └── components/
        ├── QueryInput.tsx    # Natural language input component
        ├── ResultsPanel.tsx  # Results display panel
        ├── SqlDisplay.tsx    # SQL query viewer
        ├── Chart.tsx         # Data visualization chart
        └── ConfidenceScore.tsx # AI confidence indicator
```

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.10+
- **Node.js** 18+
- A **Gemini API key** → [Get one free at Google AI Studio](https://aistudio.google.com/)

---

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/talk2data.git
cd talk2data
```

---

### 2. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Configure environment variables
copy .env.example .env
```

Edit `.env` with your credentials:

```env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite:///./talk2data.db
```

> For PostgreSQL: `DATABASE_URL=postgresql://user:password@localhost:5432/talk2data`
> For MySQL: `DATABASE_URL=mysql+pymysql://user:password@localhost:3306/talk2data`

```bash
# (Optional) Seed the database with sample data
python setup_db.py

# Start the backend server
uvicorn main:app --reload
```

Backend runs at: **http://localhost:8000**
Interactive API docs: **http://localhost:8000/docs**

---

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment variables
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start the development server
npm run dev
```

Frontend runs at: **http://localhost:3000**

---

## 🔌 API Reference

### `POST /api/query`

Convert a natural language question to SQL and execute it.

**Request Body:**
```json
{
  "question": "What are the top 5 customers by total orders?",
  "confidence_threshold": 0.4
}
```

**Response:**
```json
{
  "question": "What are the top 5 customers by total orders?",
  "sql": "SELECT customer_name, COUNT(*) as total_orders FROM orders GROUP BY customer_name ORDER BY total_orders DESC LIMIT 5",
  "explanation": "This query counts the number of orders per customer and returns the top 5 with the most orders.",
  "confidence": 0.92,
  "columns": ["customer_name", "total_orders"],
  "results": [...],
  "row_count": 5
}
```

### `GET /api/schema`

Returns the connected database schema (tables and columns).

---

## 🔒 Security

- Only **SELECT** statements are allowed to run — all DDL and DML are blocked
- Queries returning a confidence score below the threshold are rejected
- API keys are managed via `.env` files (never committed to version control)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">
  Built with ❤️ · Powered by Gemini AI · Made for data accessibility
</div>
