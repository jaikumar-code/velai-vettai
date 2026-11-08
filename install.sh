#!/bin/sh
set -e
SRC="$(cd "$(dirname "$0")" && pwd)/skills/velai-vettai"
case "$1" in
  --claude) DEST="$HOME/.claude/skills" ;;
  --codex)  DEST="$HOME/.agents/skills" ;;
  *) echo "Usage: ./install.sh --claude | --codex"; exit 1 ;;
esac
mkdir -p "$DEST" "$HOME/.velai-vettai"
rm -rf "$DEST/velai-vettai"
cp -R "$SRC" "$DEST/velai-vettai"
echo "Installed to $DEST/velai-vettai. Restart your agent, then say: setup job search"
