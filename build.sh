#!/bin/bash
source venv/bin/activate
mkdir -p downloads

echo "Building Linux Binary..."
pyinstaller --noconfirm --onefile --windowed --name "WebOptimizer_Linux" \
    --add-data "utils.py:." \
    --hidden-import "PIL._tkinter_finder" \
    desktop_app.py

echo "Moving binary to downloads folder..."
mv dist/WebOptimizer_Linux downloads/

echo "Done!"
