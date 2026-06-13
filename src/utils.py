import re
import sqlparse


def format_query(sql: str) -> str:
    """
    Format SQL query for better readability.

    Args:
        sql: Raw SQL query string

    Returns:
        Formatted SQL query
    """
    # Remove extra whitespace
    sql = sql.strip()

    # Remove markdown code blocks if present
    sql = re.sub(r"```sql\n?", "", sql)
    sql = re.sub(r"```\n?", "", sql)

    # Format using sqlparse
    formatted = sqlparse.format(
        sql,
        reindent=True,
        keyword_case="upper",
        identifier_case="lower",
        strip_comments=False,
        indent_width=4
    )

    return formatted.strip()


def validate_query(sql: str) -> tuple[bool, str]:
    """
    Basic validation of SQL query for safety.

    Args:
        sql: SQL query string

    Returns:
        Tuple of (is_valid, message)
    """
    if not sql or not sql.strip():
        return False, "Empty query"

    sql_upper = sql.upper().strip()

    # Block dangerous operations
    dangerous_keywords = ["DROP", "DELETE", "TRUNCATE", "ALTER", "CREATE", "INSERT", "UPDATE", "GRANT", "REVOKE"]

    for keyword in dangerous_keywords:
        pattern = r'\b' + keyword + r'\b'
        if re.search(pattern, sql_upper):
            return False, f"Operation '{keyword}' is not allowed. Only SELECT queries are permitted."

    # Must start with SELECT or WITH
    if not (sql_upper.startswith("SELECT") or sql_upper.startswith("WITH")):
        return False, "Only SELECT queries are allowed."

    return True, "Query is valid"


def extract_table_names(sql: str) -> list:
    """
    Extract table names from SQL query.

    Args:
        sql: SQL query string

    Returns:
        List of table names
    """
    parsed = sqlparse.parse(sql)[0]
    tables = []
    from_seen = False

    for token in parsed.tokens:
        if token.ttype is sqlparse.tokens.Keyword and token.value.upper() in ("FROM", "JOIN"):
            from_seen = True
        elif from_seen:
            if hasattr(token, "get_real_name"):
                name = token.get_real_name()
                if name:
                    tables.append(name)
            from_seen = False

    return tables
