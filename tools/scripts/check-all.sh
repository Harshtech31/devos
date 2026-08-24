#!/usr/bin/env bash
# Run all repository validation checks.
# Usage: tools/scripts/check-all.sh

set -uo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

status=0

echo "== Specification conventions =="
python3 tools/validation/validate_specs.py || status=1

echo
echo "== Canonical schemas =="
python3 tools/validation/validate_schemas.py || status=1

if [[ $# -gt 0 && "$1" == "--with-examples" ]]; then
  echo
  echo "== Example instances =="
  python3 tools/validation/validate_schemas.py \
    --instance examples/workspaces/example-workspace.json \
    --schema manifest.schema.json || status=1
fi

exit $status
