#!/usr/bin/env bash
# Download obra/superpowers skills into .claude/skills/ and .agents/skills/
# Usage: ./scripts/setup-superpowers.sh
# To remove: ./scripts/setup-superpowers.sh --remove

set -euo pipefail

REPO="obra/superpowers"
SKILLS=(
  brainstorming
  dispatching-parallel-agents
  executing-plans
  subagent-driven-development
  systematic-debugging
  test-driven-development
  using-superpowers
  verification-before-completion
  writing-plans
)

CLAUDE_DIR=".claude/skills/superpowers"
AGENTS_DIR=".agents/skills/superpowers"

if [[ "${1:-}" == "--remove" ]]; then
  echo "Removing superpowers skills..."
  rm -rf "$CLAUDE_DIR" "$AGENTS_DIR"
  # Clean up empty parent dirs
  rmdir .claude/skills .claude 2>/dev/null || true
  rmdir .agents/skills .agents 2>/dev/null || true
  echo "Done."
  exit 0
fi

echo "Downloading superpowers skills from $REPO..."
mkdir -p "$CLAUDE_DIR" "$AGENTS_DIR"

for skill in "${SKILLS[@]}"; do
  echo "  $skill"
  gh api "repos/$REPO/contents/skills/$skill/SKILL.md" --jq '.content' | base64 -d > "$CLAUDE_DIR/$skill.md"
  cp "$CLAUDE_DIR/$skill.md" "$AGENTS_DIR/$skill.md"
done

echo ""
echo "Installed ${#SKILLS[@]} skills to:"
echo "  $CLAUDE_DIR  (Claude Code)"
echo "  $AGENTS_DIR  (other agent harnesses)"
echo ""
echo "To remove: $0 --remove"
