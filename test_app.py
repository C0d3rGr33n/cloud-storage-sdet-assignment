#!/usr/bin/env python3
"""
Test script to verify the stock predictor app works correctly
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Streamlit: {e}")
        return False
    
    try:
        import yfinance as yf
        print("✅ YFinance imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import YFinance: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Pandas: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import NumPy: {e}")
        return False
    
    try:
        import plotly.graph_objects as go
        import plotly.express as px
        print("✅ Plotly imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Plotly: {e}")
        return False
    
    try:
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.preprocessing import StandardScaler
        from sklearn.metrics import mean_absolute_error, mean_squared_error
        print("✅ Scikit-learn imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Scikit-learn: {e}")
        return False
    
    try:
        import ta
        print("✅ TA (Technical Analysis) imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import TA: {e}")
        return False
    
    return True

def test_yfinance_connection():
    """Test YFinance data fetching"""
    print("\nTesting YFinance connection...")
    
    try:
        import yfinance as yf
        # Test with Reliance Industries
        ticker = yf.Ticker("RELIANCE.NS")
        data = ticker.history(period="1d", interval="5m")
        
        if not data.empty:
            print(f"✅ Successfully fetched data for RELIANCE.NS")
            print(f"   Data points: {len(data)}")
            print(f"   Latest price: ₹{data['Close'].iloc[-1]:.2f}")
            return True
        else:
            print("❌ No data received from YFinance")
            return False
            
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return False

def test_ml_components():
    """Test ML model components"""
    print("\nTesting ML components...")
    
    try:
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.preprocessing import StandardScaler
        import numpy as np
        
        # Create dummy data
        X = np.random.rand(100, 5)
        y = np.random.rand(100)
        
        # Test scaler
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        print("✅ StandardScaler working correctly")
        
        # Test Random Forest
        model = RandomForestRegressor(n_estimators=10, random_state=42)
        model.fit(X_scaled, y)
        predictions = model.predict(X_scaled[:5])
        print("✅ RandomForestRegressor working correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing ML components: {e}")
        return False

def test_technical_indicators():
    """Test technical analysis indicators"""
    print("\nTesting technical indicators...")
    
    try:
        import pandas as pd
        import numpy as np
        import ta
        
        # Create dummy price data
        dates = pd.date_range('2024-01-01', periods=50, freq='5min')
        price_data = pd.DataFrame({
            'Open': np.random.uniform(100, 110, 50),
            'High': np.random.uniform(105, 115, 50),
            'Low': np.random.uniform(95, 105, 50),
            'Close': np.random.uniform(100, 110, 50),
            'Volume': np.random.uniform(1000, 10000, 50)
        }, index=dates)
        
        # Test indicators
        sma = ta.trend.sma_indicator(price_data['Close'], window=5)
        rsi = ta.momentum.rsi(price_data['Close'], window=14)
        macd = ta.trend.macd_diff(price_data['Close'])
        
        print("✅ SMA indicator working correctly")
        print("✅ RSI indicator working correctly") 
        print("✅ MACD indicator working correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing technical indicators: {e}")
        return False

def main():
    """Run all tests"""
    print("🇮🇳 Indian Stock Price Predictor - Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_yfinance_connection,
        test_ml_components,
        test_technical_indicators
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The app should work correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)