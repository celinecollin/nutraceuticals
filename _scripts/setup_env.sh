#!/bin/bash

# 1. Ensure directories exist
mkdir -p report/drafts report/sources report/data report/scripts report/figures report/env

# 2. Check for Pandoc (install if missing via Homebrew)
if ! command -v pandoc &> /dev/null; then
    echo "Pandoc not found. Installing via Homebrew..."
    brew install pandoc
else
    echo "Pandoc is already available."
fi

# 3. Create Python Virtual Environment
if [ ! -f "report/env/bin/activate" ]; then
    echo "Creating Python virtual environment in report/env..."
    python3 -m venv report/env
else
    echo "Virtual environment already exists."
fi

# 4. Install Dependencies
echo "Installing/Updating Python dependencies..."
source report/env/bin/activate
pip install --upgrade pip
pip install -r report/scripts/requirements.txt

echo ""
echo "======================================================="
echo "Setup Complete!"
echo "To use the environment, run: source report/env/bin/activate"
echo "======================================================="
