#!/usr/bin/env bash
# Install Otto Content Skills for Claude Code or another Agent Skills app.
#
#   ./install.sh                     install every skill
#   ./install.sh weekly-social-review reel-diagnosis   install only these
#   ./install.sh --list              show the skills in this pack
#   ./install.sh --remove            remove every skill in this pack from the target
#   ./install.sh --remove hook-writer   remove only these
#
# Skills go to ~/.claude/skills (override with OTTO_SKILLS_DIR=/some/path).
set -eu

pack="$(cd "$(dirname "$0")" && pwd)/skills"
target="${OTTO_SKILLS_DIR:-$HOME/.claude/skills}"

if [ ! -d "$pack" ]; then
  echo "Can't find the skills folder next to this script. Run it from the cloned repo." >&2
  exit 1
fi

available() { for d in "$pack"/*/; do [ -f "$d/SKILL.md" ] && basename "$d"; done; }

case "${1:-}" in
  --list)
    available
    exit 0 ;;
  --remove)
    shift
    if [ "$#" -gt 0 ]; then names="$*"; else names="$(available)"; fi
    n=0
    for s in $names; do
      [ -f "$pack/$s/SKILL.md" ] || { echo "  skipped $s (not in this pack)"; continue; }
      if [ -d "$target/$s" ]; then rm -rf "${target:?}/$s"; n=$((n + 1)); fi
    done
    echo "Removed $n Otto skill(s) from $target"
    exit 0 ;;
esac

if [ "$#" -gt 0 ]; then wanted="$*"; else wanted="$(available)"; fi

mkdir -p "$target"
count=0
for s in $wanted; do
  if [ ! -f "$pack/$s/SKILL.md" ]; then
    echo "  skipped $s (not in this pack; see ./install.sh --list)"
    continue
  fi
  if [ -d "$target/$s" ]; then
    echo "  replaced existing $target/$s"
    rm -rf "${target:?}/$s"
  fi
  cp -R "$pack/$s" "$target/$s"
  count=$((count + 1))
done

echo "Installed $count Otto skill(s) into $target"
echo "Next: connect Otto (https://ottowebmaster.com/introduction/mcp/claude), restart Claude Code or your AI app, then ask \"set up my brand brain\"."
