#!/usr/bin/env bash
# Install all erzhe-skills into ~/.claude/skills/

set -e

SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installing erzhe-skills to $SKILLS_DIR ..."

for skill_dir in "$REPO_DIR"/*/; do
  [ -d "$skill_dir" ] || continue
  skill_name="$(basename "$skill_dir")"
  # Only install directories that contain a SKILL.md
  [ -f "$skill_dir/SKILL.md" ] || continue

  dest="$SKILLS_DIR/$skill_name"
  if [ -d "$dest" ]; then
    echo "  Updating $skill_name"
    rm -rf "$dest"
  else
    echo "  Installing $skill_name"
  fi
  cp -r "$skill_dir" "$dest"
done

echo "Done. Skills available:"
ls "$SKILLS_DIR"
