import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# Set page layout to wide
st.set_page_config(layout="wide")

# --- Session State Initialization ---
if "money" not in st.session_state:
    st.session_state.money = 1000000  # Initial capital
    st.session_state.portfolio = {}
    st.session_state.stock_data = pd.DataFrame()
    st.session_state.message = ""

# --- Virtual Stock Data Generation ---
def generate_realtime_data(current_data, periods=1):
    if current_data.empty:
        start_price = np.random.uniform(50000, 100000)
        prices = start_price + np.cumsum(np.random.normal(0, 500, size=periods))
        dates = pd.date_range(end=pd.Timestamp.today(), periods=periods, freq='D')
    else:
        last_price = current_data['Close'].iloc[-1]
        prices = last_price + np.cumsum(np.random.normal(0, 500, size=periods))
        last_date = current_data.index[-1]
        dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=periods, freq='D')

    open_prices = prices + np.random.normal(0, 200, size=periods)
    close_prices = prices + np.random.normal(0, 200, size=periods)
    high_prices = np.maximum(open_prices, close_prices) + np.random.uniform(0, 500, size=periods)
    low_prices = np.minimum(open_prices, close_prices) - np.random.uniform(0, 500, size=periods)
    
    new_df = pd.DataFrame({
        'Open': open_prices,
        'High': high_prices,
        'Low': low_prices,
        'Close': close_prices
    }, index=dates)

    if current_data.empty:
        return new_df
    else:
        return pd.concat([current_data, new_df])

# --- UI Layout ---
st.title("실시간 주식 가상 투자 시뮬레이션")
st.markdown("---")

# Automatically add new data point and refresh every 3 seconds
if st.session_state.stock_data.empty:
    st.session_state.stock_data = generate_realtime_data(st.session_state.stock_data, periods=30)
else:
    st.session_state.stock_data = generate_realtime_data(st.session_state.stock_data, periods=1)

# Get current price from the last row of the generated data
current_price = st.session_state.stock_data['Close'].iloc[-1]
st.metric(label="현재가", value=f"{current_price:,.0f}원")

# --- Chart Display ---
fig = go.Figure(data=[go.Candlestick(x=st.session_state.stock_data.index,
                                    open=st.session_state.stock_data['Open'],
                                    high=st.session_state.stock_data['High'],
                                    low=st.session_state.stock_data['Low'],
                                    close=st.session_state.stock_data['Close'])])
fig.update_layout(title="실시간 가상 주가 차트", yaxis_title="주가 (원)")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# --- Trading Logic and UI ---
st.subheader("나의 투자 현황")
st.write(f"**총 자산:** {st.session_state.money:,.0f}원")

if "stocks" not in st.session_state.portfolio:
    st.session_state.portfolio["stocks"] = {'shares': 0, 'price': 0}

holding_price = st.session_state.portfolio["stocks"]['price']
holding_shares = st.session_state.portfolio["stocks"]['shares']
current_value = holding_shares * current_price
profit = current_value - (holding_shares * holding_price)

st.write(f"보유 수량: **{holding_shares}주**")
st.write(f"평가 금액: **{current_value:,.0f}원**")
st.write(f"수익/손실: **{profit:,.0f}원**")

st.markdown("---")
st.subheader("매매하기")
col1, col2 = st.columns(2)

with col1:
    buy_shares = st.number_input("매수 수량 (주)", min_value=1, step=1)
    if st.button("매수하기"):
        cost = buy_shares * current_price
        if st.session_state.money >= cost:
            st.session_state.money -= cost
            
            total_shares = st.session_state.portfolio["stocks"]['shares'] + buy_shares
            total_cost = (st.session_state.portfolio["stocks"]['shares'] * st.session_state.portfolio["stocks"]['price']) + cost
            
            st.session_state.portfolio["stocks"]['shares'] = total_shares
            st.session_state.portfolio["stocks"]['price'] = total_cost / total_shares
            
            st.success(f"{buy_shares}주를 매수했습니다!")
            time.sleep(1)
            st.experimental_rerun()
        else:
            st.error("잔액이 부족합니다.")

with col2:
    sell_shares = st.number_input("매도 수량 (주)", min_value=1, step=1)
    if st.button("매도하기"):
        if st.session_state.portfolio["stocks"]['shares'] >= sell_shares:
            st.session_state.portfolio["stocks"]['shares'] -= sell_shares
            st.session_state.money += sell_shares * current_price
            
            st.success(f"{sell_shares}주를 매도했습니다!")
            time.sleep(1)
            st.experimental_rerun()
        else:
            st.error("보유 수량이 부족합니다.")

# --- Auto Refresh Mechanism ---
st.info("자동으로 3초마다 차트가 업데이트됩니다.")
time.sleep(3)
st.experimental_rerun()
