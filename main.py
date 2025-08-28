import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# --- 세션 상태 초기화 ---
if "money" not in st.session_state:
    st.session_state.money = 1000000  # 초기 자본금 100만 원
    st.session_state.portfolio = {}  # 보유 주식
    st.session_state.stock_data = pd.DataFrame() # 주가 데이터

st.title("주식 가상 투자 시뮬레이션")
st.markdown("---")

# --- 종목 코드 및 현재가 조회 ---
TICKER = "005930.KS"  # 삼성전자 주식 코드
data = yf.Ticker(TICKER)
info = data.info

st.subheader(f"종목: {info.get('longName', TICKER)}")
today_price = data.history(period="1d")['Close'].iloc[0]
st.metric(label="현재가", value=f"{today_price:.2f}원")

# --- 과거 주가 데이터 시각화 ---
@st.cache_data
def load_stock_data(ticker):
    return yf.download(ticker, period="1y")

st.session_state.stock_data = load_stock_data(TICKER)
fig = go.Figure(data=[go.Candlestick(x=st.session_state.stock_data.index,
                                     open=st.session_state.stock_data['Open'],
                                     high=st.session_state.stock_data['High'],
                                     low=st.session_state.stock_data['Low'],
                                     close=st.session_state.stock_data['Close'])])
fig.update_layout(title="지난 1년간 주가 차트", yaxis_title="주가 (원)")
st.plotly_chart(fig)

# --- 투자 현황 및 매수/매도 UI ---
st.markdown("---")
st.subheader("나의 투자 현황")
st.write(f"총 자산: **{st.session_state.money:.0f}원**")

# 보유 주식 정보
if TICKER in st.session_state.portfolio:
    holding_price = st.session_state.portfolio[TICKER]['price']
    holding_shares = st.session_state.portfolio[TICKER]['shares']
    profit = (today_price - holding_price) * holding_shares
    st.write(f"보유 수량: **{holding_shares}주**")
    st.write(f"평가 금액: **{today_price * holding_shares:.0f}원**")
    st.write(f"수익/손실: **{profit:.0f}원**")
else:
    st.write("보유하고 있는 주식이 없습니다.")

# 매수/매도 버튼
col1, col2 = st.columns(2)
with col1:
    buy_shares = st.number_input("매수 수량 (주)", min_value=1, step=1)
    if st.button("매수하기"):
        cost = buy_shares * today_price
        if st.session_state.money >= cost:
            st.session_state.money -= cost
            if TICKER not in st.session_state.portfolio:
                st.session_state.portfolio[TICKER] = {'shares': 0, 'price': 0}
            
            total_shares = st.session_state.portfolio[TICKER]['shares'] + buy_shares
            total_cost = (st.session_state.portfolio[TICKER]['shares'] * st.session_state.portfolio[TICKER]['price']) + cost
            st.session_state.portfolio[TICKER]['shares'] = total_shares
            st.session_state.portfolio[TICKER]['price'] = total_cost / total_shares
            st.success(f"{buy_shares}주를 매수했습니다!")
            st.experimental_rerun()
        else:
            st.error("잔액이 부족합니다.")

with col2:
    sell_shares = st.number_input("매도 수량 (주)", min_value=1, step=1)
    if st.button("매도하기"):
        if TICKER in st.session_state.portfolio and st.session_state.portfolio[TICKER]['shares'] >= sell_shares:
            st.session_state.portfolio[TICKER]['shares'] -= sell_shares
            st.session_state.money += sell_shares * today_price
            st.success(f"{sell_shares}주를 매도했습니다!")
            if st.session_state.portfolio[TICKER]['shares'] == 0:
                del st.session_state.portfolio[TICKER]
            st.experimental_rerun()
        else:
            st.error("보유 수량이 부족합니다.")

# --- 앱 초기화 ---
st.markdown("---")
if st.button("시뮬레이션 초기화"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()
