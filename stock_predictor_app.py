import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import ta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Indian Stock Price Predictor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .prediction-box {
        background-color: #e8f4fd;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #1f77b4;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

class StockPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def prepare_features(self, df):
        """Prepare technical indicators and features for ML model"""
        # Technical indicators
        df['SMA_5'] = ta.trend.sma_indicator(df['Close'], window=5)
        df['SMA_10'] = ta.trend.sma_indicator(df['Close'], window=10)
        df['EMA_5'] = ta.trend.ema_indicator(df['Close'], window=5)
        df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
        df['MACD'] = ta.trend.macd_diff(df['Close'])
        df['BB_upper'] = ta.volatility.bollinger_hband(df['Close'])
        df['BB_lower'] = ta.volatility.bollinger_lband(df['Close'])
        df['Volume_SMA'] = ta.trend.sma_indicator(df['Volume'], window=5)
        
        # Price-based features
        df['Price_Change'] = df['Close'].pct_change()
        df['High_Low_Ratio'] = df['High'] / df['Low']
        df['Volume_Price_Ratio'] = df['Volume'] / df['Close']
        
        # Time-based features
        df['Hour'] = df.index.hour
        df['Minute'] = df.index.minute
        df['DayOfWeek'] = df.index.dayofweek
        
        # Lag features
        for lag in [1, 2, 3, 5]:
            df[f'Close_Lag_{lag}'] = df['Close'].shift(lag)
            df[f'Volume_Lag_{lag}'] = df['Volume'].shift(lag)
        
        return df
    
    def train_model(self, df):
        """Train the prediction model"""
        # Prepare features
        df_features = self.prepare_features(df.copy())
        
        # Select feature columns
        feature_columns = [
            'Open', 'High', 'Low', 'Volume',
            'SMA_5', 'SMA_10', 'EMA_5', 'RSI', 'MACD',
            'BB_upper', 'BB_lower', 'Volume_SMA',
            'Price_Change', 'High_Low_Ratio', 'Volume_Price_Ratio',
            'Hour', 'Minute', 'DayOfWeek',
            'Close_Lag_1', 'Close_Lag_2', 'Close_Lag_3', 'Close_Lag_5',
            'Volume_Lag_1', 'Volume_Lag_2', 'Volume_Lag_3', 'Volume_Lag_5'
        ]
        
        # Remove NaN values
        df_clean = df_features.dropna()
        
        if len(df_clean) < 50:
            return False, "Insufficient data for training"
        
        # Prepare features and target
        X = df_clean[feature_columns]
        y = df_clean['Close']
        
        # Split data (use last 20% for validation)
        split_idx = int(len(X) * 0.8)
        X_train, X_val = X[:split_idx], X[split_idx:]
        y_train, y_val = y[:split_idx], y[split_idx:]
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        
        # Validate model
        y_pred = self.model.predict(X_val_scaled)
        mae = mean_absolute_error(y_val, y_pred)
        mse = mean_squared_error(y_val, y_pred)
        
        self.is_trained = True
        self.feature_columns = feature_columns
        
        return True, f"Model trained successfully. MAE: {mae:.2f}, RMSE: {np.sqrt(mse):.2f}"
    
    def predict_next_5min(self, df):
        """Predict stock price for next 5 minutes"""
        if not self.is_trained:
            return None, "Model not trained yet"
        
        # Prepare features for the latest data point
        df_features = self.prepare_features(df.copy())
        df_clean = df_features.dropna()
        
        if len(df_clean) == 0:
            return None, "No valid data for prediction"
        
        # Get the latest data point
        latest_data = df_clean[self.feature_columns].iloc[-1:].values
        latest_data_scaled = self.scaler.transform(latest_data)
        
        # Make prediction
        prediction = self.model.predict(latest_data_scaled)[0]
        current_price = df['Close'].iloc[-1]
        
        # Calculate prediction confidence (based on recent volatility)
        recent_volatility = df['Close'].pct_change().tail(20).std()
        confidence_interval = prediction * recent_volatility * 1.96  # 95% confidence
        
        return {
            'predicted_price': prediction,
            'current_price': current_price,
            'price_change': prediction - current_price,
            'percentage_change': ((prediction - current_price) / current_price) * 100,
            'confidence_lower': prediction - confidence_interval,
            'confidence_upper': prediction + confidence_interval,
            'confidence_interval': confidence_interval
        }, "Prediction successful"

# Indian stock symbols mapping
INDIAN_STOCKS = {
    'Reliance Industries': 'RELIANCE.NS',
    'Tata Consultancy Services': 'TCS.NS',
    'HDFC Bank': 'HDFCBANK.NS',
    'Infosys': 'INFY.NS',
    'ICICI Bank': 'ICICIBANK.NS',
    'Hindustan Unilever': 'HINDUNILVR.NS',
    'State Bank of India': 'SBIN.NS',
    'Bharti Airtel': 'BHARTIARTL.NS',
    'ITC': 'ITC.NS',
    'Kotak Mahindra Bank': 'KOTAKBANK.NS',
    'Larsen & Toubro': 'LT.NS',
    'Asian Paints': 'ASIANPAINT.NS',
    'Maruti Suzuki': 'MARUTI.NS',
    'Axis Bank': 'AXISBANK.NS',
    'Nestle India': 'NESTLEIND.NS'
}

@st.cache_data(ttl=60)  # Cache for 1 minute
def fetch_stock_data(symbol, period='5d', interval='5m'):
    """Fetch stock data from Yahoo Finance"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period, interval=interval)
        if data.empty:
            return None, "No data available for this stock"
        return data, "Data fetched successfully"
    except Exception as e:
        return None, f"Error fetching data: {str(e)}"

def main():
    # Header
    st.markdown('<h1 class="main-header">🇮🇳 Indian Stock Price Predictor</h1>', unsafe_allow_html=True)
    st.markdown("### Predict stock prices for the next 5 minutes using Machine Learning")
    
    # Sidebar
    st.sidebar.header("📊 Configuration")
    
    # Stock selection
    selected_stock_name = st.sidebar.selectbox(
        "Select Indian Stock:",
        list(INDIAN_STOCKS.keys()),
        index=0
    )
    selected_symbol = INDIAN_STOCKS[selected_stock_name]
    
    # Prediction settings
    st.sidebar.subheader("⚙️ Settings")
    auto_refresh = st.sidebar.checkbox("Auto-refresh data", value=True)
    refresh_interval = st.sidebar.slider("Refresh interval (seconds)", 30, 300, 60)
    
    # Data period selection
    data_period = st.sidebar.selectbox(
        "Historical data period:",
        ['1d', '2d', '5d', '1mo'],
        index=2
    )
    
    # Initialize session state
    if 'predictor' not in st.session_state:
        st.session_state.predictor = StockPredictor()
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"📈 {selected_stock_name} ({selected_symbol})")
        
        # Fetch data
        with st.spinner("Fetching latest stock data..."):
            data, message = fetch_stock_data(selected_symbol, period=data_period, interval='5m')
        
        if data is not None:
            # Display current stock info
            current_price = data['Close'].iloc[-1]
            prev_close = data['Close'].iloc[-2]
            price_change = current_price - prev_close
            price_change_pct = (price_change / prev_close) * 100
            
            # Current price metrics
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            
            with metric_col1:
                st.metric(
                    "Current Price", 
                    f"₹{current_price:.2f}",
                    f"{price_change:+.2f} ({price_change_pct:+.2f}%)"
                )
            
            with metric_col2:
                st.metric("Volume", f"{data['Volume'].iloc[-1]:,.0f}")
            
            with metric_col3:
                st.metric("High (Today)", f"₹{data['High'].max():.2f}")
            
            with metric_col4:
                st.metric("Low (Today)", f"₹{data['Low'].min():.2f}")
            
            # Train model button
            if st.button("🤖 Train Prediction Model", type="primary"):
                with st.spinner("Training machine learning model..."):
                    success, train_message = st.session_state.predictor.train_model(data)
                    if success:
                        st.success(train_message)
                    else:
                        st.error(train_message)
            
            # Stock price chart
            fig = go.Figure()
            
            # Candlestick chart
            fig.add_trace(go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Price'
            ))
            
            fig.update_layout(
                title=f"{selected_stock_name} Price Chart (5-minute intervals)",
                xaxis_title="Time",
                yaxis_title="Price (₹)",
                height=500,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Volume chart
            vol_fig = px.bar(
                x=data.index, 
                y=data['Volume'],
                title="Trading Volume",
                labels={'y': 'Volume', 'x': 'Time'}
            )
            vol_fig.update_layout(height=200, showlegend=False)
            st.plotly_chart(vol_fig, use_container_width=True)
            
        else:
            st.error(f"❌ {message}")
    
    with col2:
        st.subheader("🔮 Price Prediction")
        
        if data is not None and st.session_state.predictor.is_trained:
            # Make prediction
            prediction_result, pred_message = st.session_state.predictor.predict_next_5min(data)
            
            if prediction_result:
                # Prediction display
                st.markdown(f"""
                <div class="prediction-box">
                    <h3>Next 5-Min Prediction</h3>
                    <h2 style="color: {'green' if prediction_result['price_change'] > 0 else 'red'};">
                        ₹{prediction_result['predicted_price']:.2f}
                    </h2>
                    <p>Change: <strong style="color: {'green' if prediction_result['price_change'] > 0 else 'red'};">
                        {prediction_result['price_change']:+.2f} ({prediction_result['percentage_change']:+.2f}%)
                    </strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Confidence interval
                st.markdown("### 📊 Confidence Interval")
                st.write(f"**Lower bound:** ₹{prediction_result['confidence_lower']:.2f}")
                st.write(f"**Upper bound:** ₹{prediction_result['confidence_upper']:.2f}")
                
                # Prediction accuracy indicator
                accuracy_score = max(0, 100 - abs(prediction_result['percentage_change']) * 2)
                st.progress(accuracy_score / 100)
                st.write(f"**Confidence Score:** {accuracy_score:.1f}%")
                
                # Trading signal
                if prediction_result['percentage_change'] > 0.5:
                    st.success("🟢 **Signal: BUY**")
                elif prediction_result['percentage_change'] < -0.5:
                    st.error("🔴 **Signal: SELL**")
                else:
                    st.info("🟡 **Signal: HOLD**")
                
            else:
                st.error(f"❌ {pred_message}")
        
        elif data is not None:
            st.info("🤖 Please train the model first to get predictions")
        
        # Model status
        st.markdown("### 🧠 Model Status")
        if st.session_state.predictor.is_trained:
            st.success("✅ Model trained and ready")
        else:
            st.warning("⚠️ Model not trained yet")
        
        # Last update time
        st.markdown("### ⏰ Last Update")
        st.write(f"{datetime.now().strftime('%H:%M:%S')}")
        
        # Disclaimer
        st.markdown("### ⚠️ Disclaimer")
        st.caption("""
        This is for educational purposes only. 
        Stock predictions are not guaranteed. 
        Always do your own research before investing.
        """)
    
    # Auto-refresh functionality
    if auto_refresh and data is not None:
        time.sleep(refresh_interval)
        st.rerun()

if __name__ == "__main__":
    main()