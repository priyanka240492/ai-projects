import re
import sqlglot
from sqlglot import exp

BLOCKED = {'INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE', 'REPLACE', 'TRUNCATE', 'ATTACH', 'DETACH'}


def validate_sql(sql: str, schema_text: str) -> tuple[bool, str]:
    candidate = sql.strip().rstrip(';')
    if not candidate:
        return False, 'Generated SQL is empty.'
    try:
        tree = sqlglot.parse_one(candidate, read='sqlite')
    except Exception as exc:
        return False, f'SQL syntax error: {exc}'
    if not isinstance(tree, (exp.Select, exp.Union, exp.Subquery)):
        return False, 'Only read-only SELECT queries are allowed.'
    upper = candidate.upper()
    for keyword in BLOCKED:
        if re.search(rf'\b{keyword}\b', upper):
            return False, f'Blocked SQL operation: {keyword}'
    known_tables = set(re.findall(r'TABLE\s+([A-Za-z_][\w]*)', schema_text, flags=re.I))
    referenced = {t.name for t in tree.find_all(exp.Table)}
    unknown = referenced - known_tables
    if unknown:
        return False, f'Unknown table(s): {", ".join(sorted(unknown))}'
    return True, 'SQL is valid and read-only.'
