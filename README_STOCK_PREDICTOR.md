# 🇮🇳 Indian Stock Price Predictor

A sophisticated Streamlit web application that predicts Indian stock prices for the next 5 minutes using machine learning and real-time data from Yahoo Finance.

## ✨ Features

### 🎯 Core Functionality
- **Real-time Data**: Fetches live stock data from NSE (National Stock Exchange) via Yahoo Finance
- **5-Minute Predictions**: Uses machine learning to predict stock prices for the next 5 minutes
- **15 Popular Indian Stocks**: Pre-configured with major Indian stocks like Reliance, TCS, HDFC Bank, etc.
- **Interactive Charts**: Beautiful candlestick charts and volume indicators
- **Trading Signals**: Automated BUY/SELL/HOLD recommendations

### 🧠 Machine Learning Features
- **Random Forest Regressor**: Advanced ensemble learning algorithm
- **Technical Indicators**: RSI, MACD, Bollinger Bands, SMA, EMA
- **Feature Engineering**: 25+ engineered features including lag features and time-based patterns
- **Confidence Intervals**: Statistical confidence bounds for predictions
- **Model Validation**: Built-in validation with MAE and RMSE metrics

### 🎨 User Interface
- **Modern Design**: Clean, professional interface with custom CSS styling
- **Real-time Updates**: Auto-refresh functionality with configurable intervals
- **Responsive Layout**: Two-column layout optimized for different screen sizes
- **Interactive Sidebar**: Easy stock selection and configuration options

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Internet connection for real-time data fetching

### Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   streamlit run stock_predictor_app.py
   ```

3. **Access the App**:
   Open your browser and navigate to `http://localhost:8501`

## 📊 Available Stocks

The app includes 15 popular Indian stocks:

| Stock Name | Symbol | Sector |
|------------|--------|---------|
| Reliance Industries | RELIANCE.NS | Oil & Gas |
| Tata Consultancy Services | TCS.NS | IT Services |
| HDFC Bank | HDFCBANK.NS | Banking |
| Infosys | INFY.NS | IT Services |
| ICICI Bank | ICICIBANK.NS | Banking |
| Hindustan Unilever | HINDUNILVR.NS | FMCG |
| State Bank of India | SBIN.NS | Banking |
| Bharti Airtel | BHARTIARTL.NS | Telecom |
| ITC | ITC.NS | FMCG |
| Kotak Mahindra Bank | KOTAKBANK.NS | Banking |
| Larsen & Toubro | LT.NS | Engineering |
| Asian Paints | ASIANPAINT.NS | Paints |
| Maruti Suzuki | MARUTI.NS | Automotive |
| Axis Bank | AXISBANK.NS | Banking |
| Nestle India | NESTLEIND.NS | FMCG |

## 🔧 How to Use

### Step 1: Select Stock
- Use the sidebar to choose from 15 popular Indian stocks
- The app will automatically fetch the latest data

### Step 2: Configure Settings
- **Auto-refresh**: Enable/disable automatic data updates
- **Refresh Interval**: Set update frequency (30-300 seconds)
- **Historical Period**: Choose data period (1d, 2d, 5d, 1mo)

### Step 3: Train the Model
- Click the "🤖 Train Prediction Model" button
- The model will train on historical data and show validation metrics
- Training typically takes 10-30 seconds

### Step 4: Get Predictions
- Once trained, the model will automatically predict the next 5-minute price
- View predictions with confidence intervals and trading signals
- Monitor real-time updates if auto-refresh is enabled

## 🧮 Technical Details

### Machine Learning Pipeline

1. **Data Preprocessing**:
   - Fetches 5-minute interval data
   - Handles missing values and outliers
   - Normalizes features using StandardScaler

2. **Feature Engineering** (25+ features):
   - **Technical Indicators**: SMA, EMA, RSI, MACD, Bollinger Bands
   - **Price Features**: Price change, High/Low ratio, Volume/Price ratio
   - **Time Features**: Hour, Minute, Day of week
   - **Lag Features**: Previous 1, 2, 3, and 5 period values

3. **Model Training**:
   - Random Forest with 100 estimators
   - 80/20 train/validation split
   - Feature scaling and validation metrics

4. **Prediction**:
   - Uses latest data point for prediction
   - Calculates confidence intervals based on recent volatility
   - Provides trading signals based on predicted price movement

### Data Sources
- **Primary**: Yahoo Finance API via yfinance library
- **Symbols**: NSE-listed stocks with .NS suffix
- **Intervals**: 5-minute real-time data
- **Caching**: 1-minute TTL to balance performance and freshness

## ⚠️ Important Disclaimers

### Investment Warning
- **This app is for educational and research purposes only**
- **Not financial advice**: Do not use predictions for actual trading without proper research
- **Market risks**: Stock prices are highly volatile and unpredictable
- **Past performance**: Historical data doesn't guarantee future results

### Technical Limitations
- **5-minute predictions**: Very short-term predictions are inherently uncertain
- **Market hours**: Data available only during NSE trading hours (9:15 AM - 3:30 PM IST)
- **Data dependency**: Predictions depend on Yahoo Finance data availability
- **Model accuracy**: ML models can't account for all market factors

## 🛠️ Customization

### Adding New Stocks
To add more Indian stocks, modify the `INDIAN_STOCKS` dictionary in the code:

```python
INDIAN_STOCKS = {
    'Your Stock Name': 'SYMBOL.NS',
    # Add more stocks here
}
```

### Adjusting Model Parameters
Modify the `StockPredictor` class to experiment with different algorithms:

```python
# In the __init__ method
self.model = RandomForestRegressor(
    n_estimators=200,  # Increase for better accuracy
    max_depth=10,      # Control overfitting
    random_state=42
)
```

### Custom Features
Add your own technical indicators in the `prepare_features` method:

```python
# Example: Add Williams %R indicator
df['Williams_R'] = ta.momentum.williams_r(df['High'], df['Low'], df['Close'])
```

## 🐛 Troubleshooting

### Common Issues

1. **"No data available"**:
   - Check internet connection
   - Verify stock symbol is correct
   - Try during NSE trading hours

2. **Model training fails**:
   - Ensure sufficient historical data (at least 50 data points)
   - Try a longer historical period

3. **App runs slowly**:
   - Reduce refresh frequency
   - Disable auto-refresh during heavy usage
   - Check system resources

### Performance Tips
- Use 5d or 1mo historical periods for better model training
- Set refresh interval to 60+ seconds to avoid rate limiting
- Close other resource-intensive applications

## 📈 Future Enhancements

Potential improvements for the app:
- Support for more Indian exchanges (BSE, MCX)
- Advanced ML models (LSTM, Prophet)
- Portfolio tracking and management
- Technical analysis tools
- News sentiment integration
- Mobile-responsive design improvements

## 🤝 Contributing

Feel free to contribute by:
- Adding more Indian stocks
- Implementing new ML algorithms
- Improving the UI/UX
- Adding more technical indicators
- Enhancing error handling

## 📄 License

This project is for educational purposes. Please ensure compliance with data provider terms of service and local regulations when using financial data.

---

**Happy Trading! 📈 (But remember, invest wisely! 🧠)**