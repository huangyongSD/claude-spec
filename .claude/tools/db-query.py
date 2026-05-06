#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Read-only database query tool (PostgreSQL/HighGo via JDBC).

Only SELECT queries are allowed. SHOW/DESC equivalents use information_schema.
Connection info is read from .claude/tools/secrets.json.
"""

import argparse
import json
import os
import re
import sys

# Force UTF-8 encoding for output (fix Chinese character display)
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    import jaydebeapi
except ImportError:
    print("ERROR: jaydebeapi is not installed. Run: pip install jaydebeapi")
    sys.exit(1)

# Java 17 path for JDBC driver
JAVA17_HOME = "C:/tools/java/jdk-17.0.12"


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

# Database type to JDBC driver mapping
DB_DRIVER_MAP = {
    "postgresql": ("org.postgresql.Driver", "jdbc:postgresql://"),
    "highgo": ("com.highgo.jdbc.Driver", "jdbc:highgo://"),
}

# JDBC jar file patterns
DB_JAR_PATTERNS = {
    "postgresql": ["postgresql", "pg_jdbc"],
    "highgo": ["HgdbJdbc"],
}


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


def get_secrets_url_config(secrets):
    """Extract full URL and parse host/port/database/schema from db_master_url."""
    real = secrets["real_values"]
    full_url = real.get("db_master_url", "")

    # Detect database type from URL prefix
    db_type = None
    for dtype, (driver_class, url_prefix) in DB_DRIVER_MAP.items():
        if full_url.startswith(url_prefix):
            db_type = dtype
            break

    if db_type is None:
        print("ERROR: Unknown database type in URL: " + full_url)
        print("Supported types: postgresql, highgo")
        sys.exit(1)

    # Parse URL: jdbc:postgresql://host:port/database?params
    url_prefix = DB_DRIVER_MAP[db_type][1]
    pattern = re.escape(url_prefix) + r'([^/:]+):(\d+)/([^?]+)\??(.*)'
    match = re.match(pattern, full_url)
    if not match:
        return None

    host = match.group(1)
    port = int(match.group(2))
    database = match.group(3)
    params = match.group(4)

    # Parse schema from currentSchema param
    schema = None
    for param in params.split('&'):
        if param.startswith('currentSchema='):
            schema = param.split('=')[1]
            break

    return {
        "host": host,
        "port": port,
        "database": database,
        "schema": schema,
        "user": real["db_master_user"],
        "password": real["db_master_password"],
        "full_url": full_url,
        "db_type": db_type
    }


def get_connection_config(secrets, source="master"):
    """Extract connection config from secrets for master or slave."""
    if source == "master" and "db_master_url" in secrets["real_values"]:
        # Use URL parsing for master to extract schema
        url_config = get_secrets_url_config(secrets)
        if url_config:
            return url_config

    # Fallback to individual keys
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
    if config.get("schema"):
        print("  Schema:   " + config["schema"])
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
    if config.get("schema"):
        print("  Schema:   " + config["schema"])
    print("  Username: " + config["user"])
    print("  Password: ****")
    db_type = config.get("db_type", "postgresql")
    driver_class = DB_DRIVER_MAP.get(db_type, DB_DRIVER_MAP["postgresql"])[0]
    print("  Driver:   " + driver_class)


# Fixed HighGo JDBC driver path
HIGHGO_FIXED_JAR = "C:/Users/andyh/.m2/repository/com/highgo/hgdb-pgjdbc/42.5.0/hgdb-pgjdbc-42.5.0.jar"


def get_jdbc_jars(db_type="postgresql"):
    """Find JDBC jar files from local Maven repository based on database type."""
    # Use fixed HighGo driver if available
    if os.path.exists(HIGHGO_FIXED_JAR):
        return [HIGHGO_FIXED_JAR]

    m2_path = os.path.expanduser("~/.m2/repository")

    patterns = DB_JAR_PATTERNS.get(db_type, DB_JAR_PATTERNS["postgresql"])
    jars = []
    for root, dirs, files in os.walk(m2_path):
        for f in files:
            for pattern in patterns:
                if f.startswith(pattern) and f.endswith(".jar"):
                    jars.append(os.path.join(root, f))
                    break

    return jars


def build_jdbc_url(config):
    """Build JDBC URL from connection config based on database type."""
    host = config["host"]
    port = config["port"]
    database = config["database"]
    schema = config.get("schema")
    db_type = config.get("db_type", "postgresql")

    # Use full URL if available (preserves all params including currentSchema)
    if "full_url" in config:
        return config["full_url"]

    url_prefix = DB_DRIVER_MAP.get(db_type, DB_DRIVER_MAP["postgresql"])[1]
    url = f"{url_prefix}{host}:{port}/{database}?useUnicode=true&characterEncoding=UTF-8"
    if schema:
        url += f"&currentSchema={schema}"
    return url


def add_schema_prefix(query, schema):
    """Add schema prefix to table names in FROM/JOIN clauses if not already specified.

    This ensures queries operate on the correct schema's tables.
    - Already schema-qualified tables (e.g., 'pg_catalog.pg_class') are left unchanged
    - pg_ system tables get pg_catalog prefix (e.g., pg_class -> pg_catalog.pg_class)
    - information_schema stays unchanged (SQL standard, not schema-specific)
    - Other tables get the configured schema prefix
    - String literals and subqueries are preserved
    """
    if not schema:
        return query

    def replace_table(match):
        prefix = match.group(1)  # FROM, JOIN, INTO, etc.
        after = match.group(2)   # whitespace after keyword
        table = match.group(3)   # full table name (potentially with schema prefix)

        table_lower = table.lower()

        # Already schema-qualified (e.g., 'pg_catalog.pg_class' or 'test.hld_area')
        if '.' in table:
            return match.group(0)

        # pg_ system tables use pg_catalog schema
        if table_lower.startswith('pg_'):
            return f"{prefix}{after}pg_catalog.{table}"

        # information_schema is SQL standard, not schema-specific
        if table_lower == 'information_schema':
            return match.group(0)

        # Add configured schema prefix for user tables
        return f"{prefix}{after}{schema}.{table}"

    # Match FROM/JOIN/INTO keywords followed by table name
    # Table name can include schema prefix (e.g., pg_catalog.pg_class)
    pattern = r'\b(FROM|JOIN|INTO)(\s+)([\w."]+)'

    return re.sub(pattern, replace_table, query, flags=re.IGNORECASE)


def execute_query(config, query, limit=100, timeout=30):
    """Execute the validated read-only query and return results."""
    # Add schema prefix to table names if schema is configured
    schema = config.get("schema")
    query = add_schema_prefix(query, schema)

    limit_clause = ""
    if not re.search(r'\bLIMIT\b', query, re.IGNORECASE):
        limit_clause = " LIMIT " + str(limit)

    full_query = query + limit_clause

    jdbc_url = build_jdbc_url(config)

    # Set JAVA_HOME for JayDeBeApi to use Java 17
    os.environ["JAVA_HOME"] = JAVA17_HOME
    os.environ["PATH"] = os.path.join(JAVA17_HOME, "bin") + os.pathsep + os.environ.get("PATH", "")
    # Set JVM encoding for Chinese character support
    os.environ["JAVA_TOOL_OPTIONS"] = "-Dfile.encoding=UTF-8"

    db_type = config.get("db_type", "postgresql")

    jars = get_jdbc_jars(db_type)
    if not jars:
        print(f"ERROR: {db_type} JDBC driver not found.")
        print(f"Expected patterns: {DB_JAR_PATTERNS.get(db_type)}")
        print("Please ensure the driver is installed.")
        sys.exit(1)

    jdbc_driver = jars[0]
    print(f"Using JDBC driver: {jdbc_driver}", file=sys.stderr)

    # Use fixed HighGo driver (still uses org.postgresql.Driver class)
    if jdbc_driver == HIGHGO_FIXED_JAR:
        driver_class = "org.postgresql.Driver"
    else:
        driver_class = DB_DRIVER_MAP.get(db_type, DB_DRIVER_MAP["postgresql"])[0]

    try:
        conn = jaydebeapi.connect(
            driver_class,
            jdbc_url,
            [config["user"], config["password"]],
            jdbc_driver,
        )
    except Exception as e:
        print("ERROR: Connection failed: " + str(e))
        print("  Host: " + config["host"] + ", Port: " + str(config["port"]))
        print("  Database: " + config["database"] + ", User: " + config["user"])
        sys.exit(1)

    try:
        cursor = conn.cursor()
        cursor.execute(full_query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        cursor.close()
    except Exception as e:
        conn.close()
        print("ERROR: Query execution failed: " + str(e))
        sys.exit(1)
    finally:
        conn.close()

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
        description="Read-only HighGo/PostgreSQL query tool via JDBC. Only SELECT allowed."
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
