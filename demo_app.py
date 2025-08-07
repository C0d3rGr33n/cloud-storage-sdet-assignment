#!/usr/bin/env python3
"""
Demo script for the Indian Stock Price Predictor
This demonstrates the functionality with sample data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our StockPredictor class
from stock_predictor_app import StockPredictor

def generate_sample_data(days=5):
    """Generate sample stock data for demonstration"""
    # Create date range with 5-minute intervals
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Generate timestamps for market hours (9:15 AM to 3:30 PM IST)
    timestamps = []
    current_date = start_date.date()
    
    while current_date <= end_date.date():
        # Skip weekends
        if current_date.weekday() < 5:  # Monday=0, Sunday=6
            market_start = datetime.combine(current_date, datetime.min.time().replace(hour=9, minute=15))
            market_end = datetime.combine(current_date, datetime.min.time().replace(hour=15, minute=30))
            
            current_time = market_start
            while current_time <= market_end:
                timestamps.append(current_time)
                current_time += timedelta(minutes=5)
        
        current_date += timedelta(days=1)
    
    # Generate realistic stock price data
    n_points = len(timestamps)
    
    # Starting price around 2500 (similar to Reliance)
    base_price = 2500
    
    # Generate price movements with some trend and volatility
    price_changes = np.random.normal(0, 0.002, n_points)  # 0.2% average volatility
    
    # Add some trend
    trend = np.linspace(-0.01, 0.01, n_points)  # Small overall trend
    price_changes += trend
    
    # Calculate prices
    prices = [base_price]
    for i in range(1, n_points):
        new_price = prices[-1] * (1 + price_changes[i])
        prices.append(max(new_price, base_price * 0.9))  # Prevent price from going too low
    
    # Generate OHLC data
    data = []
    for i, (timestamp, close_price) in enumerate(zip(timestamps, prices)):
        # Generate realistic OHLC based on close price
        volatility = close_price * 0.005  # 0.5% intraday volatility
        
        high = close_price + np.random.uniform(0, volatility)
        low = close_price - np.random.uniform(0, volatility)
        
        if i == 0:
            open_price = close_price
        else:
            open_price = prices[i-1] + np.random.uniform(-volatility/2, volatility/2)
        
        volume = np.random.uniform(50000, 200000)  # Random volume
        
        data.append({
            'Open': open_price,
            'High': max(open_price, high, close_price),
            'Low': min(open_price, low, close_price),
            'Close': close_price,
            'Volume': int(volume)
        })
    
    df = pd.DataFrame(data, index=timestamps)
    return df

def demo_prediction():
    """Demonstrate the prediction functionality"""
    print("🇮🇳 Indian Stock Price Predictor - Demo")
    print("=" * 50)
    
    # Generate sample data
    print("📊 Generating sample stock data...")
    sample_data = generate_sample_data(days=5)
    
    print(f"   Generated {len(sample_data)} data points")
    print(f"   Date range: {sample_data.index[0]} to {sample_data.index[-1]}")
    print(f"   Current price: ₹{sample_data['Close'].iloc[-1]:.2f}")
    print(f"   Daily change: ₹{sample_data['Close'].iloc[-1] - sample_data['Close'].iloc[-75]:.2f}")
    
    # Initialize predictor
    print("\n🤖 Initializing ML model...")
    predictor = StockPredictor()
    
    # Train the model
    print("🔄 Training prediction model...")
    success, message = predictor.train_model(sample_data)
    
    if success:
        print(f"✅ {message}")
        
        # Make prediction
        print("\n🔮 Making 5-minute price prediction...")
        prediction_result, pred_message = predictor.predict_next_5min(sample_data)
        
        if prediction_result:
            current_price = prediction_result['current_price']
            predicted_price = prediction_result['predicted_price']
            price_change = prediction_result['price_change']
            percentage_change = prediction_result['percentage_change']
            
            print(f"📈 Prediction Results:")
            print(f"   Current Price: ₹{current_price:.2f}")
            print(f"   Predicted Price (5 min): ₹{predicted_price:.2f}")
            print(f"   Expected Change: ₹{price_change:+.2f} ({percentage_change:+.2f}%)")
            print(f"   Confidence Range: ₹{prediction_result['confidence_lower']:.2f} - ₹{prediction_result['confidence_upper']:.2f}")
            
            # Trading signal
            if percentage_change > 0.5:
                print("   🟢 Trading Signal: BUY")
            elif percentage_change < -0.5:
                print("   🔴 Trading Signal: SELL")
            else:
                print("   🟡 Trading Signal: HOLD")
                
        else:
            print(f"❌ Prediction failed: {pred_message}")
            
    else:
        print(f"❌ Training failed: {message}")
    
    # Show some data statistics
    print(f"\n📊 Data Statistics:")
    print(f"   Price Range: ₹{sample_data['Close'].min():.2f} - ₹{sample_data['Close'].max():.2f}")
    print(f"   Average Volume: {sample_data['Volume'].mean():,.0f}")
    print(f"   Volatility (std): {sample_data['Close'].std():.2f}")
    
    print("\n" + "=" * 50)
    print("✨ Demo completed successfully!")
    print("\n💡 To run the full Streamlit app:")
    print("   streamlit run stock_predictor_app.py")

if __name__ == "__main__":
    demo_prediction()