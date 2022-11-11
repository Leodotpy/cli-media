#!/bin/bash
set -e
if [ ! -f .venv/bin/activate ]; then
    echo "VENV does nto exist, attempting to create."
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt
python3 run.py
