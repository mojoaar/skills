#!/usr/bin/env bash
# Resolve latest stable version of an npm package.
# Usage: ./resolve-version.sh <package-name>
# Output: exact version string (e.g., "1.2.3")
set -euo pipefail

if [ $# -eq 0 ]; then
  echo "Usage: resolve-version.sh <package-name>" >&2
  exit 1
fi

npm info "$1" version 2>/dev/null || {
  echo "ERROR: Package '$1' not found on npm" >&2
  exit 1
}
