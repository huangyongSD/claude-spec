#!/usr/bin/env python3
"""
Secrets sync tool.

Reads database and Redis connection info from application YAML files
and writes it to .claude/tools/secrets.json.

Optionally scans .claude/ config files and replaces real sensitive
values with placeholders.
"""

import argparse
import json
import os
import re


def deep_merge(base, override):
    """Merge override dict into base dict recursively."""
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            deep_merge(base[key], value)
        else:
            base[key] = value
import sys

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml is not installed. Run: pip install -r .claude/tools/requirements.txt")
    sys.exit(1)


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
SECRETS_PATH = os.path.join(SCRIPT_DIR, "secrets.json")

# JDBC URL pattern: jdbc:mysql://host:port/database?params
JDBC_PATTERN = re.compile(
    r'jdbc:mysql://([^:]+):(\d+)/([^?]+)(\?.*)?'
)

# Placeholder key mapping: real value key -> placeholder string
PLACEHOLDER_MAP = {
    "db_master_url": "{{DB_MASTER_URL}}",
    "db_master_host": "{{DB_MASTER_HOST}}",
    "db_master_port": "{{DB_MASTER_PORT}}",
    "db_master_name": "{{DB_MASTER_NAME}}",
    "db_master_user": "{{DB_MASTER_USER}}",
    "db_master_password": "{{DB_MASTER_PASSWORD}}",
    "db_slave_url": "{{DB_SLAVE_URL}}",
    "db_slave_host": "{{DB_SLAVE_HOST}}",
    "db_slave_port": "{{DB_SLAVE_PORT}}",
    "db_slave_name": "{{DB_SLAVE_NAME}}",
    "db_slave_user": "{{DB_SLAVE_USER}}",
    "db_slave_password": "{{DB_SLAVE_PASSWORD}}",
    "redis_host": "{{REDIS_HOST}}",
    "redis_port": "{{REDIS_PORT}}",
    "redis_password": "{{REDIS_PASSWORD}}",
    "rabbit_host": "{{RABBIT_HOST}}",
    "rabbit_port": "{{RABBIT_PORT}}",
    "rabbit_user": "{{RABBIT_USER}}",
    "rabbit_password": "{{RABBIT_PASSWORD}}",
}


def parse_jdbc_url(url):
    """Parse a JDBC URL to extract host, port, and database name."""
    match = JDBC_PATTERN.match(url)
    if not match:
        return None
    return {
        "host": match.group(1),
        "port": int(match.group(2)),
        "database": match.group(3),
    }


def deep_get(data, path, default=None):
    """Get a nested value from a dict using a dot-separated path."""
    keys = path.split(".")
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


def read_application_yaml(profile):
    """Read the application YAML file for the given profile."""
    # Try multiple possible locations
    possible_paths = [
        os.path.join(PROJECT_ROOT, "yudao-boot-mini", "yudao-server",
                      "src", "main", "resources", "application-" + profile + ".yaml"),
        os.path.join(PROJECT_ROOT, "yudao-boot-mini", "yudao-server",
                      "src", "main", "resources", "application-" + profile + ".yml"),
        os.path.join(PROJECT_ROOT, "yudao-server",
                      "src", "main", "resources", "application-" + profile + ".yaml"),
        os.path.join(PROJECT_ROOT, "yudao-server",
                      "src", "main", "resources", "application-" + profile + ".yml"),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                # Spring YAML uses --- as document separator; merge all docs
                docs = list(yaml.safe_load_all(f))
                merged = {}
                for doc in docs:
                    if doc:
                        deep_merge(merged, doc)
                return merged, path

    print("ERROR: Could not find application-" + profile + ".yaml/.yml")
    print("Searched paths:")
    for p in possible_paths:
        print("  " + p)
    sys.exit(1)


def extract_db_config(data, prefix):
    """Extract database connection info from YAML data.

    prefix is 'master' or 'slave'.
    The YAML structure uses spring.datasource.dynamic.datasource.{prefix}.
    """
    ds_prefix = "spring.datasource.dynamic.datasource." + prefix

    url = deep_get(data, ds_prefix + ".url")
    username = deep_get(data, ds_prefix + ".username")
    password = deep_get(data, ds_prefix + ".password")

    if not url:
        # Try alternate structure
        url = deep_get(data, "spring.datasource." + prefix + ".url")
        username = deep_get(data, "spring.datasource." + prefix + ".username")
        password = deep_get(data, "spring.datasource." + prefix + ".password")

    if not url:
        # Try single datasource (no dynamic)
        url = deep_get(data, "spring.datasource.url")
        username = deep_get(data, "spring.datasource.username")
        password = deep_get(data, "spring.datasource.password")
        if url and prefix == "master":
            parsed = parse_jdbc_url(url)
            result = {
                "db_" + prefix + "_url": url,
                "db_" + prefix + "_host": parsed["host"] if parsed else "",
                "db_" + prefix + "_port": parsed["port"] if parsed else 3306,
                "db_" + prefix + "_name": parsed["database"] if parsed else "",
                "db_" + prefix + "_user": username or "",
                "db_" + prefix + "_password": str(password) if password else "",
            }
            return result
        return None

    parsed = parse_jdbc_url(url)
    result = {
        "db_" + prefix + "_url": url,
        "db_" + prefix + "_host": parsed["host"] if parsed else "",
        "db_" + prefix + "_port": parsed["port"] if parsed else 3306,
        "db_" + prefix + "_name": parsed["database"] if parsed else "",
        "db_" + prefix + "_user": username or "",
        "db_" + prefix + "_password": str(password) if password else "",
    }
    return result


def extract_redis_config(data):
    """Extract Redis connection info from YAML data."""
    redis_prefix = "spring.redis"
    # Try spring.data.redis (Spring Boot 2.x+)
    if deep_get(data, "spring.data.redis.host"):
        redis_prefix = "spring.data.redis"

    host = deep_get(data, redis_prefix + ".host", "127.0.0.1")
    port = deep_get(data, redis_prefix + ".port", 6379)
    password = deep_get(data, redis_prefix + ".password", "")

    return {
        "redis_host": host,
        "redis_port": port,
        "redis_password": password if password else "",
    }


def extract_rabbit_config(data):
    """Extract RabbitMQ connection info from YAML data."""
    rabbit_prefix = "spring.rabbitmq"

    host = deep_get(data, rabbit_prefix + ".host")
    port = deep_get(data, rabbit_prefix + ".port")
    username = deep_get(data, rabbit_prefix + ".username")
    password = deep_get(data, rabbit_prefix + ".password")

    if not host:
        return None

    return {
        "rabbit_host": host,
        "rabbit_port": port or 5672,
        "rabbit_user": username or "guest",
        "rabbit_password": password or "guest",
    }


def build_secrets(data):
    """Build the secrets.json structure from YAML data."""
    real_values = {}

    # Master database
    master_config = extract_db_config(data, "master")
    if master_config:
        real_values.update(master_config)

    # Slave database
    slave_config = extract_db_config(data, "slave")
    if slave_config:
        real_values.update(slave_config)

    # Redis
    redis_config = extract_redis_config(data)
    if redis_config:
        real_values.update(redis_config)

    # RabbitMQ
    rabbit_config = extract_rabbit_config(data)
    if rabbit_config:
        real_values.update(rabbit_config)

    # Build placeholders mapping (real_value -> placeholder_key)
    placeholders = {}
    for key, value in real_values.items():
        if key in PLACEHOLDER_MAP:
            placeholders[PLACEHOLDER_MAP[key]] = str(value)

    # Also build reverse: real value -> placeholder key for scan-configs
    reverse_map = {}
    for key, value in real_values.items():
        if key in PLACEHOLDER_MAP:
            placeholder_key = PLACEHOLDER_MAP[key]
            reverse_map[str(value)] = placeholder_key

    return {
        "real_values": real_values,
        "placeholders": placeholders,
        "reverse_map": reverse_map,
    }


def write_secrets(secrets):
    """Write secrets to secrets.json."""
    # Don't write reverse_map to file (it's only used internally for scanning)
    output = {
        "real_values": secrets["real_values"],
        "placeholders": secrets["placeholders"],
    }
    with open(SECRETS_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print("Written: " + SECRETS_PATH)


def scan_and_replace(secrets):
    """Scan .claude/ config files and replace real values with placeholders."""
    claude_dir = os.path.join(PROJECT_ROOT, ".claude")
    reverse_map = secrets.get("reverse_map", {})

    # Build reverse_map from placeholders if not present
    if not reverse_map:
        for placeholder_key, real_value in secrets["placeholders"].items():
            reverse_map[real_value] = placeholder_key

    # Scan patterns for file matching
    patterns = ["*.md", "*.json", "*.yaml", "*.yml"]
    scan_dir = claude_dir

    files_scanned = 0
    files_modified = 0
    replacements_made = 0

    for root, dirs, files in os.walk(scan_dir):
        # Skip tools directory (secrets.json lives there)
        if "tools" in dirs:
            dirs.remove("tools")
        # Skip specs directory (user-generated content)
        # Skip templates directory (template content)

        for filename in files:
            # Check if file matches our patterns
            ext = os.path.splitext(filename)[1]
            if ext not in [".md", ".json", ".yaml", ".yml"]:
                continue

            filepath = os.path.join(root, filename)
            # Skip secrets.json itself
            if filepath == SECRETS_PATH:
                continue

            files_scanned += 1

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            except (IOError, UnicodeDecodeError):
                continue

            new_content = content
            for real_value, placeholder_key in reverse_map.items():
                if not real_value or real_value.strip() == "":
                    continue
                # Don't replace if the placeholder is already there
                if placeholder_key in new_content:
                    continue
                # Only replace exact matches to avoid partial replacements
                count = new_content.count(real_value)
                if count > 0:
                    new_content = new_content.replace(real_value, placeholder_key)
                    replacements_made += count

            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                files_modified += 1
                print("  Modified: " + filepath)

    print("Scan complete: " + str(files_scanned) + " files scanned, "
          + str(files_modified) + " files modified, "
          + str(replacements_made) + " replacements made.")


def main():
    parser = argparse.ArgumentParser(
        description="Sync secrets from application YAML to secrets.json. "
                    "Optionally scan .claude/ config files and replace real values with placeholders."
    )
    parser.add_argument("--profile", choices=["local", "dev"], default="local",
                        help="Application profile to read (default: local)")
    parser.add_argument("--scan-configs", action="store_true",
                        help="Scan .claude/ config files and replace real sensitive values with placeholders")

    args = parser.parse_args()

    # Read application YAML
    print("Reading application-" + args.profile + ".yaml...")
    data, yaml_path = read_application_yaml(args.profile)
    print("  Found: " + yaml_path)

    # Extract secrets
    secrets = build_secrets(data)

    # Print extracted info (password hidden)
    print("Extracted configuration:")
    for key, value in secrets["real_values"].items():
        if "password" in key:
            print("  " + key + ": ****")
        else:
            print("  " + key + ": " + str(value))

    # Write secrets.json
    write_secrets(secrets)

    # Optionally scan and replace
    if args.scan_configs:
        print("\nScanning .claude/ config files for real sensitive values...")
        # Re-build reverse_map for scanning (read from written file)
        scan_secrets = {}
        scan_secrets["real_values"] = secrets["real_values"]
        scan_secrets["placeholders"] = secrets["placeholders"]
        scan_secrets["reverse_map"] = {}
        for key, value in secrets["real_values"].items():
            if key in PLACEHOLDER_MAP:
                scan_secrets["reverse_map"][str(value)] = PLACEHOLDER_MAP[key]
        scan_and_replace(scan_secrets)

    print("\nDone.")


if __name__ == "__main__":
    main()