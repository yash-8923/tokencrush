#!/bin/sh
set -e
echo "Installing tokencrush..."

# Install uv if missing
if ! command -v uv >/dev/null 2>&1; then
  echo "Installing uv..."
  pip install uv --quiet
fi

uv pip install git+https://github.com/yash-8923/tokencrush.git --system --quiet
python3 -m tokencrush init --global

echo ""
echo "Done! Auto-runs in every Claude Code session."
echo "Run 'tokencrush run' to test now."
