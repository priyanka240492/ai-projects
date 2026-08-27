from .database import execute_read_only


def execute_sql(sql: str) -> list[dict]:
    return execute_read_only(sql)
