# 🚀 Quick Start Guide - Indian Stock Price Predictor

## 📦 What You Get

A complete Streamlit web application that predicts Indian stock prices for the next 5 minutes using machine learning.

### ✨ Features
- **15 Popular Indian Stocks** (Reliance, TCS, HDFC Bank, etc.)
- **Real-time Data** from Yahoo Finance
- **ML Predictions** using Random Forest with 25+ technical indicators
- **Beautiful UI** with interactive charts and trading signals
- **Auto-refresh** functionality

## 🏃‍♂️ Quick Setup (30 seconds)

### Option 1: One-Command Setup
```bash
chmod +x run_app.sh && ./run_app.sh
```

### Option 2: Manual Setup
```bash
# 1. Create virtual environment
python3 -m venv stock_env

# 2. Activate environment
source stock_env/bin/activate

# 3. Install dependencies
pip install streamlit yfinance pandas numpy scikit-learn plotly matplotlib seaborn ta

# 4. Run the app
streamlit run stock_predictor_app.py
```

## 🌐 Access the App

Open your browser and go to: **http://localhost:8501**

## 🎮 How to Use

1. **Select Stock**: Choose from 15 popular Indian stocks in the sidebar
2. **Configure Settings**: Set auto-refresh and data period preferences
3. **Train Model**: Click "🤖 Train Prediction Model" button
4. **Get Predictions**: View 5-minute price predictions with confidence intervals
5. **Trading Signals**: See automated BUY/SELL/HOLD recommendations

## 🧪 Test the Components

```bash
# Run demo with sample data
python demo_app.py

# Run component tests
python test_app.py
```

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `stock_predictor_app.py` | Main Streamlit application |
| `demo_app.py` | Demo script with sample data |
| `test_app.py` | Component testing script |
| `run_app.sh` | One-click startup script |
| `requirements.txt` | Python dependencies |
| `README_STOCK_PREDICTOR.md` | Detailed documentation |

## ⚠️ Important Notes

- **Educational Purpose**: This app is for learning and research only
- **Market Hours**: Best results during NSE trading hours (9:15 AM - 3:30 PM IST)
- **Internet Required**: Needs connection for real-time data fetching
- **Disclaimer**: Not financial advice - always do your own research!

## 🐛 Troubleshooting

**App won't start?**
- Ensure Python 3.8+ is installed
- Check internet connection
- Try manual setup steps

**No data available?**
- Markets might be closed
- Try different stocks or time periods
- Use the demo script for testing

**Model training fails?**
- Ensure sufficient historical data
- Try longer time periods (5d or 1mo)

## 🎯 Next Steps

- Explore different stocks and time periods
- Experiment with model parameters
- Add your own technical indicators
- Try different ML algorithms

---

**Happy Trading! 📈 (But invest wisely! 🧠)**