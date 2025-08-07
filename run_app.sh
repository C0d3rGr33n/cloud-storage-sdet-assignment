#!/bin/bash

# Indian Stock Price Predictor - Startup Script
echo "🇮🇳 Starting Indian Stock Price Predictor..."
echo "================================================"

# Check if virtual environment exists
if [ ! -d "stock_env" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   python3 -m venv stock_env"
    echo "   source stock_env/bin/activate"
    echo "   pip install -r requirements_minimal.txt"
    exit 1
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source stock_env/bin/activate

# Check if required packages are installed
echo "🔍 Checking dependencies..."
python -c "import streamlit, yfinance, pandas, numpy, plotly, sklearn, ta" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies. Installing..."
    pip install -r requirements_minimal.txt
fi

echo "✅ Dependencies verified!"
echo ""
echo "🚀 Starting Streamlit app..."
echo "📱 The app will be available at: http://localhost:8501"
echo "🛑 Press Ctrl+C to stop the app"
echo ""

# Start the Streamlit app
streamlit run stock_predictor_app.py --server.port 8501 --server.address 0.0.0.0