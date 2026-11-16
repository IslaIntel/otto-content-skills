#!/usr/bin/env bash
# Otto Content Skills installer: copies each skill into ~/.claude/skills/
set -euo pipefail

SKILLS_DIR="${HOME}/.claude/skills"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "${SKILLS_DIR}"
for dir in "${SCRIPT_DIR}/skills"/*/; do
  name="$(basename "${dir}")"
  mkdir -p "${SKILLS_DIR}/${name}"
  cp -R "${dir}". "${SKILLS_DIR}/${name}/"
  echo "  installed ${name}"
done

echo ""
echo "Done. Restart Claude Code, connect Otto, then ask: \"weekly review\""
echo "Otto: https://ottowebmaster.com"
