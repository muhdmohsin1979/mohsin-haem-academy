#!/usr/bin/env bash
#
# install-hooks.sh — one-time setup to point git's hooksPath at the
# scripts/hooks directory in this repo.
#
# Run this once after cloning the repo:
#   bash scripts/install-hooks.sh
#
# Idempotent: safe to run multiple times.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "$REPO_ROOT" ]; then
  echo "install-hooks: not inside a git repository." >&2
  exit 1
fi
cd "$REPO_ROOT"

# Ensure the hook file is executable.
chmod +x scripts/hooks/pre-commit

# Point git at the versioned hooks folder.
git config core.hooksPath scripts/hooks

# Confirm.
CONFIGURED=$(git config --get core.hooksPath)
if [ "$CONFIGURED" = "scripts/hooks" ]; then
  echo "install-hooks: OK — core.hooksPath = $CONFIGURED"
  echo "pre-commit will now run tone_guard.py + preflight.py (PII only) on"
  echo "every commit that touches markdown or HTML files."
else
  echo "install-hooks: FAILED — core.hooksPath is '$CONFIGURED'" >&2
  exit 1
fi
