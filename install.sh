#!/usr/bin/env bash
#
# PTAF setup script
#
# This is a scaffolding stub. Fill in real setup steps as modules are
# implemented (see modules/ for offensive, defensive, and ai_analysis code).

set -euo pipefail

echo "==> Purple Team Automation Framework (PTAF) setup"

# 1. Verify Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "python3 is required but was not found. Please install Python 3.10+ and re-run." >&2
    exit 1
fi

# 2. Create a virtual environment (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate

# 3. Install Python dependencies
pip install --upgrade pip
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "No requirements.txt found yet -- skipping dependency install."
fi

echo "==> Setup complete. Activate the virtual environment with:"
echo "    source .venv/bin/activate"
