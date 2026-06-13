import streamlit as st
from src.sql_generator import generate_sql
from src.db_handler import execute_query, get_schema_info
from src.utils import format_query, validate_query
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="LLM SQL Query Generator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1rem;
        color: #6c757d;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sql-box {
        background: #1e1e2e;
        color: #cdd6f4;
        padding: 1rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        font-size: 0.95rem;
    }
    .result-header {
        color: #1a1a2e;
        font-weight: 600;
        font-size: 1.1rem;
    }
    .stButton>button {
        background-color: #1a1a2e;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #16213e;
        color: #e94560;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-title">🧠 LLM SQL Query Generator</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Convert plain English to SQL queries using AI — no SQL knowledge required</p>', unsafe_allow_html=True)

st.divider()

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    db_type = st.selectbox(
        "Database Type",
        ["SQLite (Demo)", "MySQL", "PostgreSQL"],
        help="Select the target database type"
    )

    st.divider()
    st.subheader("📋 Sample Database Schema")
    schema = get_schema_info()
    st.code(schema, language="sql")

    st.divider()
    st.subheader("💡 Example Questions")
    examples = [
        "Show all customers from Mumbai",
        "Find top 5 products by revenue",
        "Count orders placed last month",
        "Show customers with more than 3 orders",
        "Find average order value by city"
    ]
    for ex in examples:
        if st.button(f"→ {ex}", key=ex):
            st.session_state["user_input"] = ex

# Main layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📝 Enter Your Question")

    user_input = st.text_area(
        label="Natural Language Query",
        placeholder="e.g. Show me all customers who placed more than 5 orders last month...",
        height=120,
        key="user_input",
        label_visibility="collapsed"
    )

    generate_btn = st.button("⚡ Generate SQL", use_container_width=True)

    if generate_btn and user_input:
        with st.spinner("Generating SQL query..."):
            try:
                sql_query = generate_sql(user_input, db_type)
                formatted_query = format_query(sql_query)
                st.session_state["generated_sql"] = formatted_query
                st.session_state["last_input"] = user_input
            except Exception as e:
                st.error(f"Error generating SQL: {str(e)}")

with col2:
    st.subheader("🔍 Generated SQL Query")

    if "generated_sql" in st.session_state:
        sql = st.session_state["generated_sql"]
        st.code(sql, language="sql")

        col_copy, col_run = st.columns(2)
        with col_copy:
            st.download_button(
                "📋 Download SQL",
                data=sql,
                file_name="query.sql",
                mime="text/plain",
                use_container_width=True
            )
        with col_run:
            run_btn = st.button("▶️ Execute Query", use_container_width=True)

        if run_btn or st.session_state.get("run_query"):
            with st.spinner("Executing query..."):
                try:
                    is_valid, message = validate_query(sql)
                    if is_valid:
                        results = execute_query(sql)
                        if results is not None and not results.empty:
                            st.success(f"✅ Query returned {len(results)} rows")
                            st.dataframe(results, use_container_width=True)
                        else:
                            st.info("Query executed successfully. No results returned.")
                    else:
                        st.warning(f"⚠️ Query validation: {message}")
                except Exception as e:
                    st.error(f"Execution error: {str(e)}")
    else:
        st.info("Your generated SQL query will appear here.")

# Query History
st.divider()
st.subheader("📜 Query History")

if "history" not in st.session_state:
    st.session_state["history"] = []

if "generated_sql" in st.session_state and "last_input" in st.session_state:
    entry = {
        "Question": st.session_state["last_input"],
        "SQL Query": st.session_state["generated_sql"]
    }
    if entry not in st.session_state["history"]:
        st.session_state["history"].append(entry)

if st.session_state["history"]:
    history_df = pd.DataFrame(st.session_state["history"])
    st.dataframe(history_df, use_container_width=True)
    if st.button("🗑️ Clear History"):
        st.session_state["history"] = []
        st.rerun()
else:
    st.info("Your query history will appear here after generating queries.")

# Footer
st.divider()
st.markdown("""
<div style='text-align:center; color:#6c757d; font-size:0.85rem;'>
    Built with ❤️ using OpenAI API + LangChain + Streamlit &nbsp;|&nbsp; 
    <a href='https://github.com/yourusername/llm-sql-query-generator' target='_blank'>GitHub</a>
</div>
""", unsafe_allow_html=True)
