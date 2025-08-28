import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- UI 레이아웃 ---
st.set_page_config(layout="wide")
st.title("랜덤 주가 차트 생성기")
st.markdown("---")

# --- 가상 주가 데이터 생성 함수 ---
@st.cache_data
def generate_stock_data(length=365):
    dates = pd.date_range(end=pd.Timestamp.today(), periods=length, freq='D')
    
    # 랜덤한 시초가와 종가 생성
    start_price = np.random.uniform(50000, 100000)
    prices = start_price + np.cumsum(np.random.normal(0, 500, size=length))
    
    # 캔들스틱 데이터 생성
    open_prices = prices + np.random.normal(0, 200, size=length)
    close_prices = prices + np.random.normal(0, 200, size=length)
    high_prices = np.maximum(open_prices, close_prices) + np.random.uniform(0, 500, size=length)
    low_prices = np.minimum(open_prices, close_prices) - np.random.uniform(0, 500, size=length)
    
    df = pd.DataFrame({
        'Date': dates,
        'Open': open_prices,
        'High': high_prices,
        'Low': low_prices,
        'Close': close_prices
    })
    df.set_index('Date', inplace=True)
    return df

# --- 차트 그리기 ---
if st.button("새로운 차트 생성"):
    st.session_state.chart_data = generate_stock_data()

# 세션 상태에 데이터가 없으면 초기 생성
if 'chart_data' not in st.session_state:
    st.session_state.chart_data = generate_stock_data()

# 데이터 확인 및 차트 그리기
if not st.session_state.chart_data.empty:
    fig = go.Figure(data=[go.Candlestick(x=st.session_state.chart_data.index,
                                        open=st.session_state.chart_data['Open'],
                                        high=st.session_state.chart_data['High'],
                                        low=st.session_state.chart_data['Low'],
                                        close=st.session_state.chart_data['Close'])])
    fig.update_layout(title="가상 주가 차트", yaxis_title="주가 (원)")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("생성된 데이터 (일부)")
    st.write(st.session_state.chart_data.head())
else:
    st.error("차트 데이터를 생성하는 데 실패했습니다.")
