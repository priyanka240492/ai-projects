from .database import get_connection


def get_schema() -> str:
    with get_connection() as conn:
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall()
        sections = []
        for (table_name,) in tables:
            columns = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
            foreign_keys = conn.execute(f"PRAGMA foreign_key_list({table_name})").fetchall()
            lines = [f"TABLE {table_name}"]
            for col in columns:
                pk = " PRIMARY KEY" if col[5] else ""
                lines.append(f"  - {col[1]}: {col[2]}{pk}")
            for fk in foreign_keys:
                lines.append(f"  - FOREIGN KEY {fk[3]} REFERENCES {fk[2]}({fk[4]})")
            sections.append("\n".join(lines))
    return "\n\n".join(sections)
