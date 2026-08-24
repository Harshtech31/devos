#!/usr/bin/env python3
"""Validate canonical JSON schemas under schemas/.

Checks, per Rule 17 of SPECIFICATION_RULES.md:
  1. Every *.schema.json parses as JSON.
  2. Every schema carries $schema and $id under the reserved namespace.
  3. Every schema validates against the Draft 2020-12 meta-schema
     (requires the jsonschema package; falls back to structural checks).
  4. Cross-file $ref targets resolve within the directory.

Usage:
  python3 tools/validation/validate_schemas.py [--instance FILE --schema NAME]

Exit code 0 on success, 1 on any failure.
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = REPO_ROOT / "schemas"
RESERVED_NS = "https://devos.dev/schemas/v0/"

try:
    from jsonschema import Draft202012Validator
    import referencing

    HAVE_JSONSCHEMA = True
except ImportError:
    HAVE_JSONSCHEMA = False


def load_store():
    store = {}
    failures = []
    for path in sorted(SCHEMA_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text())
        except Exception as exc:
            failures.append(f"{path.name}: invalid JSON: {exc}")
            continue
        if "$id" not in data or not str(data["$id"]).startswith(RESERVED_NS):
            failures.append(f"{path.name}: missing or off-namespace $id")
        if "$schema" not in data:
            failures.append(f"{path.name}: missing $schema declaration")
        store[str(data.get("$id", path.name))] = data
    return store, failures


def check_meta_and_refs(store):
    failures = []
    if not HAVE_JSONSCHEMA:
        print("jsonschema not installed; running structural fallback only.")
        for name, data in store.items():
            if "type" not in data and "properties" not in data and "$defs" not in data:
                failures.append(f"{name}: no type/properties/$defs found")
        return failures

    registry = referencing.Registry().with_resources(
        [(k, referencing.Resource.from_contents(v)) for k, v in store.items()]
    )
    for name, data in sorted(store.items()):
        try:
            Draft202012Validator.check_schema(data)
        except Exception as exc:
            failures.append(f"{name}: meta-schema invalid: {exc}")
            continue
        validator = Draft202012Validator(data, registry=registry)
        seen = set()
        base_id = str(data.get("$id", "")).rsplit("/", 1)[0]

        def walk(node, base=base_id):
            if isinstance(node, dict):
                ref = node.get("$ref")
                if isinstance(ref, str) and not ref.startswith("#"):
                    target = ref.split("#")[0]
                    if target not in store and "://" in target:
                        resolved = target
                    elif target not in store:
                        resolved = f"{base}/{target}"
                    else:
                        resolved = target
                    if resolved not in store and resolved not in seen:
                        seen.add(resolved)
                        failures.append(f"{name}: unresolved $ref -> {ref}")
                for value in node.values():
                    walk(value, base)
            elif isinstance(node, list):
                for item in node:
                    walk(item, base)

        walk(data)
        print(f"meta-valid: {name.rsplit('/', 1)[-1]}")
    return failures


def validate_instance(store, instance_path, schema_name):
    failures = []
    if not HAVE_JSONSCHEMA:
        return ["--instance requires the jsonschema package."]
    candidates = [n for n in store if n.endswith(schema_name)]
    if len(candidates) != 1:
        return [f"schema '{schema_name}' matched {len(candidates)} files."]
    try:
        instance = json.loads(Path(instance_path).read_text())
    except Exception as exc:
        return [f"instance unreadable: {exc}"]
    registry = referencing.Registry().with_resources(
        [(k, referencing.Resource.from_contents(v)) for k, v in store.items()]
    )
    validator = Draft202012Validator(store[candidates[0]], registry=registry)
    errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)
    for err in errors:
        location = "/".join(str(p) for p in err.absolute_path) or "<root>"
        failures.append(f"instance error at {location}: {err.message}")
    if not failures:
        print(f"instance valid against {candidates[0]}")
    return failures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--instance", help="JSON file to validate")
    parser.add_argument("--schema", help="schema filename for --instance, e.g. manifest.schema.json")
    args = parser.parse_args()

    if not SCHEMA_DIR.is_dir():
        print(f"schemas/ not found at {SCHEMA_DIR}", file=sys.stderr)
        return 1

    store, failures = load_store()
    print(f"loaded {len(store)} schemas from {SCHEMA_DIR}")
    failures += check_meta_and_refs(store)

    if args.instance or args.schema:
        if not (args.instance and args.schema):
            failures.append("--instance and --schema must be used together.")
        else:
            failures += validate_instance(store, args.instance, args.schema)

    for failure in failures:
        print(f"FAIL: {failure}")
    print(f"\nresult: {'FAILED' if failures else 'OK'} ({len(failures)} problems)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
