import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils import format_query, validate_query, extract_table_names


class TestFormatQuery:
    def test_basic_select(self):
        sql = "select * from customers"
        result = format_query(sql)
        assert "SELECT" in result
        assert "customers" in result

    def test_removes_markdown_backticks(self):
        sql = "```sql\nSELECT * FROM customers\n```"
        result = format_query(sql)
        assert "```" not in result

    def test_strips_whitespace(self):
        sql = "   SELECT * FROM customers   "
        result = format_query(sql)
        assert result == result.strip()


class TestValidateQuery:
    def test_valid_select(self):
        sql = "SELECT * FROM customers"
        is_valid, msg = validate_query(sql)
        assert is_valid is True

    def test_blocks_drop(self):
        sql = "DROP TABLE customers"
        is_valid, msg = validate_query(sql)
        assert is_valid is False
        assert "DROP" in msg

    def test_blocks_delete(self):
        sql = "DELETE FROM customers WHERE customer_id = 1"
        is_valid, msg = validate_query(sql)
        assert is_valid is False

    def test_blocks_insert(self):
        sql = "INSERT INTO customers VALUES (1, 'test')"
        is_valid, msg = validate_query(sql)
        assert is_valid is False

    def test_empty_query(self):
        sql = ""
        is_valid, msg = validate_query(sql)
        assert is_valid is False

    def test_valid_with_clause(self):
        sql = "WITH cte AS (SELECT * FROM orders) SELECT * FROM cte"
        is_valid, msg = validate_query(sql)
        assert is_valid is True


class TestExtractTableNames:
    def test_simple_from(self):
        sql = "SELECT * FROM customers"
        tables = extract_table_names(sql)
        assert "customers" in tables

    def test_join_tables(self):
        sql = "SELECT * FROM customers JOIN orders ON customers.customer_id = orders.customer_id"
        tables = extract_table_names(sql)
        assert len(tables) >= 1
