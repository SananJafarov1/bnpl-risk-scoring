#!/bin/bash

echo "========================================"
echo "  BNPL Risk Scoring Engine - Startup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed"
        echo "Please install Python 3.11 or higher"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "[1/3] Checking Python installation..."
$PYTHON_CMD --version
echo ""

echo "[2/3] Navigating to backend folder..."
cd backend || exit 1
echo ""

echo "[3/3] Starting backend server..."
echo ""
echo "The dashboard will open automatically in your browser!"
echo "URL: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

$PYTHON_CMD main.py
