from src.sql_validator import validate_sql

SCHEMA = 'TABLE customers\n  - customer_id: INTEGER\nTABLE orders\n  - order_id: INTEGER\n'


def test_valid_select():
    ok, _ = validate_sql('SELECT customer_id FROM customers', SCHEMA)
    assert ok


def test_reject_write_statement():
    ok, _ = validate_sql('DELETE FROM customers', SCHEMA)
    assert not ok


def test_reject_unknown_table():
    ok, _ = validate_sql('SELECT * FROM payments', SCHEMA)
    assert not ok
