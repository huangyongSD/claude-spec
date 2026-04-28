#!/usr/bin/env python3
"""
Read-only database query tool (PostgreSQL).

Only SELECT queries are allowed. SHOW/DESC equivalents use information_schema.
Connection info is read from .claude/tools/secrets.json.
"""

import argparse
import json
import os
import re
import sys

try:
    import psycopg2
except ImportError:
    print("ERROR: psycopg2 is not installed. Run: pip install -r .claude/tools/requirements.txt")
    sys.exit(1)


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SECRETS_PATH = os.path.join(SCRIPT_DIR, "secrets.json")
CONFIRM_FLAG_PATH = os.path.join(SCRIPT_DIR, ".db-query-confirmed")

# Blocked SQL keywords (write operations)
BLOCKED_KEYWORDS = re.compile(
    r'\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE|GRANT|REVOKE|REPLACE|CALL|EXEC)\b',
    re.IGNORECASE
)

# Single-statement check: no semicolons except at the very end
MULTI_STATEMENT_PATTERN = re.compile(r';\s*\S', re.IGNORECASE)


def load_secrets():
    """Load secrets.json. If missing, print error and exit."""
    if not os.path.exists(SECRETS_PATH):
        print("ERROR: secrets.json not found at " + SECRETS_PATH)
        print("Run: python .claude/tools/secrets-sync.py first to generate it.")
        sys.exit(1)
    try:
        with open(SECRETS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print("ERROR: Failed to read secrets.json: " + str(e))
        sys.exit(1)


def get_connection_config(secrets, source="master"):
    """Extract connection config from secrets for master or slave."""
    real = secrets["real_values"]
    prefix = "db_master" if source == "master" else "db_slave"

    host_key = prefix + "_host"
    port_key = prefix + "_port"
    name_key = prefix + "_name"
    user_key = prefix + "_user"
    pass_key = prefix + "_password"

    required_keys = [host_key, port_key, name_key, user_key, pass_key]
    for k in required_keys:
        if k not in real:
            print("ERROR: Missing key '" + k + "' in secrets.json real_values.")
            sys.exit(1)

    config = {
        "host": real[host_key],
        "port": int(real[port_key]),
        "database": real[name_key],
        "user": real[user_key],
        "password": real[pass_key],
    }
    return config


def validate_query(query):
    """Validate that the query is read-only and single-statement."""
    stripped = query.strip()
    if stripped.endswith(";"):
        stripped = stripped[:-1].strip()

    # Check for blocked keywords
    match = BLOCKED_KEYWORDS.search(stripped)
    if match:
        print("ERROR: Blocked SQL keyword detected: " + match.group(1))
        print("Only SELECT queries are allowed.")
        sys.exit(1)

    # Check for multiple statements
    if MULTI_STATEMENT_PATTERN.search(stripped):
        print("ERROR: Multiple statements detected. Only single statements are allowed.")
        sys.exit(1)

    # Verify it starts with SELECT
    allowed_start = re.compile(r'^\s*SELECT\b', re.IGNORECASE)
    if not allowed_start.match(stripped):
        print("ERROR: Query must start with SELECT.")
        print("For table inspection, use information_schema queries like:")
        print("  SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
        print("  SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'xxx'")
        print("  SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'xxx'")
        sys.exit(1)

    return stripped


def is_confirmed():
    """Check if connection has been previously confirmed."""
    return os.path.exists(CONFIRM_FLAG_PATH)


def mark_confirmed():
    """Mark connection as confirmed for future runs."""
    with open(CONFIRM_FLAG_PATH, "w") as f:
        f.write("confirmed\n")


def confirm_interactive(config):
    """Interactive confirmation of connection details."""
    print("Connection details:")
    print("  Host:     " + config["host"])
    print("  Port:     " + str(config["port"]))
    print("  Database: " + config["database"])
    print("  Username: " + config["user"])
    print("  Password: ****")
    print()
    response = input("Confirm this connection? [y/N]: ").strip().lower()
    if response == "y" or response == "yes":
        mark_confirmed()
        return True
    else:
        print("Connection not confirmed. Exiting.")
        sys.exit(0)


def show_config(secrets, source="master"):
    """Print connection config without executing any query. Password hidden."""
    config = get_connection_config(secrets, source)
    print("Connection configuration (" + source + "):")
    print("  Host:     " + config["host"])
    print("  Port:     " + str(config["port"]))
    print("  Database: " + config["database"])
    print("  Username: " + config["user"])
    print("  Password: ****")


def execute_query(config, query, limit=100, timeout=30):
    """Execute the validated read-only query and return results."""
    limit_clause = ""
    if not re.search(r'\bLIMIT\b', query, re.IGNORECASE):
        limit_clause = " LIMIT " + str(limit)

    full_query = query + limit_clause

    try:
        connection = psycopg2.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            dbname=config["database"],
            connect_timeout=timeout,
        )
    except psycopg2.OperationalError as e:
        print("ERROR: Connection failed: " + str(e))
        print("  Host: " + config["host"] + ", Port: " + str(config["port"]))
        print("  Database: " + config["database"] + ", User: " + config["user"])
        sys.exit(1)

    try:
        with connection.cursor() as cursor:
            cursor.execute(full_query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
    except psycopg2.OperationalError as e:
        print("ERROR: Query execution failed: " + str(e))
        sys.exit(1)
    except psycopg2.ProgrammingError as e:
        print("ERROR: Query syntax error: " + str(e))
        sys.exit(1)
    finally:
        connection.close()

    return columns, rows


def format_as_json(columns, rows):
    """Format results as JSON."""
    result = []
    for row in rows:
        row_dict = {}
        for i, col in enumerate(columns):
            value = row[i]
            if isinstance(value, bytes):
                try:
                    value = value.decode("utf-8")
                except UnicodeDecodeError:
                    value = value.decode("utf-8", errors="replace")
            if hasattr(value, '__float__'):
                value = float(value)
            row_dict[col] = value
        result.append(row_dict)
    return json.dumps(result, ensure_ascii=False, indent=2)


def format_as_table(columns, rows):
    """Format results as a readable text table."""
    if not columns:
        return "(no results)"

    str_rows = []
    for row in rows:
        str_row = []
        for val in row:
            if isinstance(val, bytes):
                try:
                    s = val.decode("utf-8")
                except UnicodeDecodeError:
                    s = val.decode("utf-8", errors="replace")
            else:
                s = str(val) if val is not None else "NULL"
            str_row.append(s)
        str_rows.append(str_row)

    widths = [len(col) for col in columns]
    for row in str_rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(val))

    header = " | ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "-+-".join("-" * w for w in widths)

    lines = [header, separator]
    for row in str_rows:
        line = " | ".join(val.ljust(widths[i]) for i, val in enumerate(row))
        lines.append(line)

    lines.append("")
    lines.append("(" + str(len(rows)) + " rows)")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Read-only PostgreSQL query tool. Only SELECT allowed."
    )
    parser.add_argument("--query", required=False, help="SQL query to execute")
    parser.add_argument("--source", choices=["master", "slave"], default="master",
                        help="Database source: master or slave (default: master)")
    parser.add_argument("--format", choices=["json", "table"], default="json",
                        help="Output format: json or table (default: json)")
    parser.add_argument("--limit", type=int, default=100,
                        help="Max rows to return (default: 100)")
    parser.add_argument("--timeout", type=int, default=30,
                        help="Query timeout in seconds (default: 30)")
    parser.add_argument("--confirm", action="store_true",
                        help="Confirm connection (required on first run)")
    parser.add_argument("--show-config", action="store_true",
                        help="Show connection config without executing query")

    args = parser.parse_args()

    secrets = load_secrets()

    if args.show_config:
        show_config(secrets, args.source)
        return

    if not args.query:
        parser.error("--query is required unless --show-config is used")

    if not is_confirmed() and not args.confirm:
        print("ERROR: Connection not confirmed. First run requires --confirm flag.")
        print("Run: python .claude/tools/db-query.py --confirm --query \"SELECT tablename FROM pg_tables WHERE schemaname = 'public'\"")
        sys.exit(1)

    config = get_connection_config(secrets, args.source)

    if not is_confirmed():
        if args.confirm:
            mark_confirmed()
            print("Connection auto-confirmed via --confirm flag.")
        else:
            confirm_interactive(config)

    validated_query = validate_query(args.query)
    columns, rows = execute_query(config, validated_query, args.limit, args.timeout)

    if args.format == "json":
        print(format_as_json(columns, rows))
    else:
        print(format_as_table(columns, rows))


if __name__ == "__main__":
    main()