# 🧠 LLM-Powered SQL Query Generator

> Convert plain English to SQL queries instantly using OpenAI GPT + LangChain + Streamlit

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red.svg)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.13-green.svg)](https://langchain.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-orange.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 About

**LLM SQL Query Generator** is an AI-powered application that converts natural language questions into accurate, optimized SQL queries. No SQL knowledge required — just type your question in plain English and get production-ready SQL instantly.

Built as a fresher-level AI/ML portfolio project demonstrating:
- LLM integration via OpenAI API
- Prompt engineering for structured outputs
- End-to-end application development with Streamlit
- Database interaction and query execution

---

## ✨ Features

- 🔤 **Natural Language to SQL** — Type in plain English, get SQL instantly
- ⚡ **Live Query Execution** — Run queries on a built-in SQLite demo database
- 📋 **Query History** — Track all generated queries in the session
- 🛡️ **Query Validation** — Blocks dangerous operations (DROP, DELETE, etc.)
- 🎨 **Clean UI** — Intuitive Streamlit interface with syntax highlighting
- 🔌 **Demo Mode** — Works without an API key using rule-based fallback
- 📥 **Download SQL** — Export generated queries as `.sql` files

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | OpenAI GPT-3.5-turbo |
| **AI Framework** | LangChain |
| **Frontend** | Streamlit |
| **Database** | SQLite |
| **Language** | Python 3.9+ |
| **Query Formatting** | sqlparse |

---

## 📁 Project Structure

```
llm-sql-query-generator/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore
├── README.md
│
├── src/
│   ├── __init__.py
│   ├── sql_generator.py    # LLM-powered SQL generation (LangChain + OpenAI)
│   ├── db_handler.py       # SQLite database setup and query execution
│   └── utils.py            # Query formatting, validation, utilities
│
├── tests/
│   └── test_utils.py       # Unit tests (pytest)
│
└── data/
    └── demo.db             # Auto-generated SQLite demo database
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/llm-sql-query-generator.git
cd llm-sql-query-generator
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

> 💡 **No API key?** The app runs in demo mode with pre-built query templates — perfect for testing!

### 5. Run the Application

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 💬 Example Queries

| Natural Language | Generated SQL |
|---|---|
| Show all customers from Mumbai | `SELECT * FROM customers WHERE city = 'Mumbai'` |
| Top 5 products by revenue | `SELECT ... ORDER BY revenue DESC LIMIT 5` |
| Count orders placed last month | `SELECT COUNT(*) FROM orders WHERE ...` |
| Average order value by city | `SELECT city, AVG(total_amount) FROM ... GROUP BY city` |
| Customers with more than 3 orders | `SELECT ... HAVING COUNT(order_id) > 3` |

---

## 🗄️ Demo Database Schema

```sql
customers   (customer_id, name, email, city, state, phone, created_at)
products    (product_id, name, category, price, stock_quantity)
orders      (order_id, customer_id, order_date, total_amount, status)
order_items (item_id, order_id, product_id, quantity, unit_price)
payments    (payment_id, order_id, payment_date, amount, method)
```

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 📊 How It Works

```
User Input (Plain English)
        ↓
Prompt Engineering (Schema + Context + Rules)
        ↓
OpenAI GPT-3.5-turbo via LangChain
        ↓
SQL Query Generation
        ↓
Query Validation & Formatting (sqlparse)
        ↓
Execution on SQLite Database
        ↓
Results displayed in Streamlit UI
```

---

## 🔒 Security

- Only `SELECT` and `WITH` queries are allowed
- Dangerous operations (`DROP`, `DELETE`, `INSERT`, `UPDATE`, `ALTER`, `TRUNCATE`) are blocked
- API key stored securely in `.env` file (never committed to Git)

---



---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## ⭐ Show Your Support

If this project helped you, please give it a ⭐ on GitHub!
