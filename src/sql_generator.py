from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()

# Database schema context
DB_SCHEMA = """
Tables and columns in the database:

1. customers(customer_id, name, email, city, state, phone, created_at)
2. products(product_id, name, category, price, stock_quantity)
3. orders(order_id, customer_id, order_date, total_amount, status)
4. order_items(item_id, order_id, product_id, quantity, unit_price)
5. payments(payment_id, order_id, payment_date, amount, method)
"""

SQL_PROMPT_TEMPLATE = """
You are an expert SQL query generator. Convert the user's natural language question into a valid SQL query.

Database Schema:
{schema}

Database Type: {db_type}

Rules:
- Generate only the SQL query, nothing else
- Do not include any explanation or markdown
- Use proper SQL syntax for the specified database type
- Use table aliases for readability
- Handle JOINs when multiple tables are needed
- Use aggregate functions (COUNT, SUM, AVG) when appropriate
- Add LIMIT 100 by default unless specified otherwise
- Use proper date functions based on database type

User Question: {question}

SQL Query:
"""

def generate_sql(question: str, db_type: str = "SQLite (Demo)") -> str:
    """
    Generate SQL query from natural language using LLM.
    
    Args:
        question: Natural language question
        db_type: Target database type
        
    Returns:
        Generated SQL query string
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        # Return demo query if no API key
        return _generate_demo_sql(question)
    
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=api_key
    )
    
    prompt = PromptTemplate(
        input_variables=["schema", "db_type", "question"],
        template=SQL_PROMPT_TEMPLATE
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    result = chain.run(
        schema=DB_SCHEMA,
        db_type=db_type,
        question=question
    )
    
    return result.strip()


def _generate_demo_sql(question: str) -> str:
    """
    Generate demo SQL queries without API key for testing.
    
    Args:
        question: Natural language question
        
    Returns:
        Demo SQL query
    """
    question_lower = question.lower()
    
    if "customer" in question_lower and ("all" in question_lower or "show" in question_lower or "list" in question_lower):
        return "SELECT customer_id, name, email, city, state\nFROM customers\nLIMIT 100;"

    elif "top" in question_lower and "product" in question_lower:
        return """SELECT 
    p.name AS product_name,
    p.category,
    SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.name, p.category
ORDER BY total_revenue DESC
LIMIT 5;"""

    elif "order" in question_lower and ("count" in question_lower or "how many" in question_lower):
        return """SELECT 
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS total_revenue
FROM orders
WHERE strftime('%Y-%m', order_date) = strftime('%Y-%m', 'now', '-1 month');"""

    elif "average" in question_lower and "order" in question_lower:
        return """SELECT 
    c.city,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value,
    COUNT(o.order_id) AS total_orders
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.city
ORDER BY avg_order_value DESC
LIMIT 100;"""

    elif "more than" in question_lower and "order" in question_lower:
        return """SELECT 
    c.customer_id,
    c.name,
    c.email,
    c.city,
    COUNT(o.order_id) AS order_count
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.email, c.city
HAVING COUNT(o.order_id) > 3
ORDER BY order_count DESC
LIMIT 100;"""

    else:
        return """SELECT 
    c.name AS customer_name,
    c.city,
    o.order_id,
    o.total_amount,
    o.order_date,
    o.status
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
ORDER BY o.order_date DESC
LIMIT 100;"""
