from src.database import get_connection
from src.schema_inspector import get_schema


def test_schema_discovery(tmp_path, monkeypatch):
    monkeypatch.setattr('src.database.DATABASE_PATH', tmp_path / 'test.db')
    with get_connection() as conn:
        conn.execute('CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, name TEXT)')
    schema = get_schema()
    assert 'TABLE customers' in schema
    assert 'customer_id' in schema
