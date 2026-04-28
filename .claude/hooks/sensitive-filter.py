#!/usr/bin/env python3
"""
Sensitive information filter.

Reads secrets.json to get real values and placeholders,
then scans content for sensitive information and replaces
real values with placeholders.

Also performs pattern-based detection for common sensitive
patterns (IP addresses, passwords near config keys).
"""

import argparse
import json
import os
import re
import sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SECRETS_PATH = os.path.join(SCRIPT_DIR, "secrets.json")

# IP address regex (matches any IPv4 address)
IP_PATTERN = re.compile(
    r'\b(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}'
    r'(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\b'
)

# Safe IPs that should not be flagged
SAFE_IPS = {"127.0.0.1", "0.0.0.0", "localhost"}

# Password pattern in YAML/config: password: <value> (not a placeholder)
PASSWORD_NEAR_KEY_PATTERN = re.compile(
    r'(?:password|passwd|pwd|secret|token|key|credential)\s*[=:]\s*([^\s{\n"][^\n]*?)(?:\s*$|\s*[,\}])',
    re.IGNORECASE
)

# Placeholder pattern to skip
PLACEHOLDER_REGEX = re.compile(r'\{\{[A-Z_]+\}\}')


def load_secrets():
    """Load secrets.json if it exists. Return None if not found."""
    if not os.path.exists(SECRETS_PATH):
        return None
    try:
        with open(SECRETS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def build_reverse_map(secrets):
    """Build a mapping from real values to placeholder keys."""
    reverse_map = {}
    if not secrets:
        return reverse_map

    real_values = secrets.get("real_values", {})
    placeholders = secrets.get("placeholders", {})

    # Build from placeholders (placeholder_key -> real_value)
    # We need real_value -> placeholder_key
    for placeholder_key, real_value in placeholders.items():
        if real_value and str(real_value).strip():
            reverse_map[str(real_value)] = placeholder_key

    return reverse_map


def is_private_ip(ip):
    """Check if an IP is in private ranges (10.x, 172.16-31.x, 192.168.x)."""
    parts = ip.split(".")
    if len(parts) != 4:
        return False

    first = int(parts[0])
    second = int(parts[1])

    # 10.0.0.0/8
    if first == 10:
        return True
    # 172.16.0.0/12
    if first == 172 and 16 <= second <= 31:
        return True
    # 192.168.0.0/16
    if first == 192 and second == 168:
        return True

    # Not private = public IP, also sensitive
    return False


def replace_real_values(content, reverse_map):
    """Replace known real values with placeholders."""
    new_content = content
    replacements = []

    for real_value, placeholder_key in reverse_map.items():
        if not real_value or real_value.strip() == "":
            continue
        # Skip if already a placeholder
        if PLACEHOLDER_REGEX.search(real_value):
            continue
        # Skip very short values that might cause false positives
        if len(real_value) < 3:
            continue
        # Only replace if placeholder is not already present nearby
        count = new_content.count(real_value)
        if count > 0:
            new_content = new_content.replace(real_value, placeholder_key)
            replacements.append({
                "type": "real_value",
                "original": real_value,
                "replaced_with": placeholder_key,
                "count": count,
            })

    return new_content, replacements


def detect_ip_addresses(content):
    """Detect IP addresses that are not safe (127.0.0.1, localhost)."""
    detections = []
    for match in IP_PATTERN.finditer(content):
        ip = match.group()
        if ip in SAFE_IPS:
            continue
        # Flag both private and public IPs as sensitive
        ip_type = "private" if is_private_ip(ip) else "public"
        detections.append({
            "type": "ip_address",
            "value": ip,
            "ip_type": ip_type,
            "position": match.start(),
        })
    return detections


def detect_password_patterns(content):
    """Detect password patterns near config keys."""
    detections = []
    for match in PASSWORD_NEAR_KEY_PATTERN.finditer(content):
        value = match.group(1).strip()
        # Skip if value is already a placeholder
        if PLACEHOLDER_REGEX.search(value):
            continue
        # Skip empty or very common default values
        if value in {"", "''", '""'}:
            continue
        # Skip if it's an environment variable reference
        if value.startswith("${"):
            continue
        detections.append({
            "type": "password_pattern",
            "value": value[:20] + "..." if len(value) > 20 else value,
            "full_match": match.group(),
            "position": match.start(),
        })
    return detections


def sanitize_content(content, secrets=None):
    """Sanitize content by replacing real values and detecting patterns."""
    reverse_map = build_reverse_map(secrets)

    # Step 1: Replace known real values
    new_content, replacements = replace_real_values(content, reverse_map)

    # Step 2: Detect IP addresses
    ip_detections = detect_ip_addresses(new_content)

    # Step 3: Detect password patterns
    password_detections = detect_password_patterns(new_content)

    # Combine all detections
    all_detections = replacements + ip_detections + password_detections

    return new_content, all_detections


def format_detections(detections):
    """Format detections as a readable report."""
    if not detections:
        return "No sensitive information detected."

    lines = ["Sensitive information detected:"]
    for d in detections:
        if d["type"] == "real_value":
            lines.append("  - Real value replaced: '" + d["original"][:30]
                         + "' -> '" + d["replaced_with"]
                         + "' (x" + str(d["count"]) + ")")
        elif d["type"] == "ip_address":
            lines.append("  - IP address: " + d["value"]
                         + " (" + d["ip_type"] + ")")
        elif d["type"] == "password_pattern":
            lines.append("  - Password pattern: " + d["value"])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Filter sensitive information from content. "
                    "Replaces known real values with placeholders and "
                    "detects common sensitive patterns."
    )
    parser.add_argument("--input-file", required=False,
                        help="Path to file to filter")
    parser.add_argument("--secrets-json", required=False,
                        default=SECRETS_PATH,
                        help="Path to secrets.json (default: " + SECRETS_PATH + ")")
    parser.add_argument("--content", required=False,
                        help="Content string to filter (alternative to --input-file)")
    parser.add_argument("--report-only", action="store_true",
                        help="Only report detections, do not output sanitized content")

    args = parser.parse_args()

    # Load secrets
    secrets = None
    secrets_path = args.secrets_json
    if os.path.exists(secrets_path):
        try:
            with open(secrets_path, "r", encoding="utf-8") as f:
                secrets = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print("WARNING: Failed to read secrets.json: " + str(e))
            print("Proceeding with pattern-based detection only.")
    else:
        print("INFO: secrets.json not found. Using pattern-based detection only.")
        print("Run: python .claude/tools/secrets-sync.py to generate it.")

    # Get content
    content = ""
    if args.input_file:
        if not os.path.exists(args.input_file):
            print("ERROR: Input file not found: " + args.input_file)
            sys.exit(1)
        with open(args.input_file, "r", encoding="utf-8") as f:
            content = f.read()
    elif args.content:
        content = args.content
    else:
        # Read from stdin
        try:
            content = sys.stdin.read()
        except EOFError:
            print("ERROR: No content provided. Use --input-file, --content, or stdin.")
            sys.exit(1)

    if not content:
        print("No content to filter.")
        sys.exit(0)

    # Sanitize
    sanitized, detections = sanitize_content(content, secrets)

    # Output
    if args.report_only:
        print(format_detections(detections))
    else:
        # Output sanitized content
        print(sanitized)
        # Output detection report after content
        if detections:
            print()
            print("---")
            print(format_detections(detections))


if __name__ == "__main__":
    main()