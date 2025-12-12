#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Run Streamlit app
echo "Starting University Analytics Dashboard..."
echo "Dashboard akan berjalan di: http://localhost:8501"
echo ""
echo "Tekan Ctrl+C untuk menghentikan..."

streamlit run src/dashboard/app.py
