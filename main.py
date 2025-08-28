import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

# --- 세션 상태 초기화 ---
if "money" not in st.session_state:
    st.session_state.money = 1000000  # 초기 자본금 100만 원
    st.session_state.portfolio = {}  # 보유 주식
    st.session_state.stock_data = pd.DataFrame() # 주가 데이터
    st.session_state.message = ""

# --- 함수 정의 ---
@st.cache_data(ttl=3600)
def load_stock_data(ticker):
    try:
        data = yf.download(ticker, period="1y")
        return data
    except Exception as e:
        st.session_state.message = f"주가 데이터를 불러오는 데 실패했습니다: {e}"
        return pd.DataFrame()

def get_current_price(ticker):
    try:
        data = yf.Ticker(ticker)
        return data.history(period="1d")['Close'].iloc[0]
    except Exception as e:
        st.session_state.message = f"현재가를 불러오는 데 실패했습니다: {e}"
        return None

# --- UI 레이아웃 ---
st.set_page_config(layout="wide")
st.title("주식 가상 투자 시뮬레이션")
st.markdown("---")

# --- 주식 정보 및 현재가 섹션 ---
col1, col2 = st.columns([1, 2])

with col1:
    TICKER = st.text_input("종목 코드 입력", value="005930.KS")
    current_price = get_current_price(TICKER)
    if current_price:
        st.metric(label=f"현재가", value=f"{current_price:,.0f}원")
    else:
        st.warning("유효하지 않은 종목 코드입니다.")

with col2:
    st.session_state.stock_data = load_stock_data(TICKER)
    if not st.session_state.stock_data.empty:
        fig = go.Figure(data=[go.Candlestick(x=st.session_state.stock_data.index,
                                            open=st.session_state.stock_data['Open'],
                                            high=st.session_state.stock_data['High'],
                                            low=st.session_state.stock_data['Low'],
                                            close=st.session_state.stock_data['Close'])])
        fig.update_layout(title="지난 1년간 주가 차트", yaxis_title="주가 (원)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("주가 데이터를 찾을 수 없습니다. 종목 코드를 확인하거나 잠시 후 다시 시도해주세요.")

st.markdown("---")

# --- 투자 현황 및 매수/매도 섹션 ---
st.subheader("나의 투자 현황")
st.write(f"**총 자산:** {st.session_state.money:,.0f}원")

portfolio_df = pd.DataFrame(st.session_state.portfolio).T
if not portfolio_df.empty:
    portfolio_df.index.name = '종목 코드'
    portfolio_df['현재가'] = current_price
    portfolio_df['평가 금액'] = portfolio_df['shares'] * portfolio_df['현재가']
    portfolio_df['매입 총액'] = portfolio_df['shares'] * portfolio_df['price']
    portfolio_df['수익/손실'] = portfolio_df['평가 금액'] - portfolio_df['매입 총액']
    portfolio_df['수익률 (%)'] = (portfolio_df['수익/손실'] / portfolio_df['매입 총액']) * 100
    st.table(portfolio_df[['shares', 'price', '현재가', '평가 금액', '수익/손실', '수익률 (%)']].style.format({
        'price': '{:,.0f}원'.format,
        '현재가': '{:,.0f}원'.format,
        '평가 금액': '{:,.0f}원'.format,
        '수익/손실': '{:,.0f}원'.format,
        '수익률 (%)': '{:,.2f}%'.format
    }))
else:
    st.write("보유하고 있는 주식이 없습니다.")

st.markdown("---")
st.subheader("매매하기")
col3, col4 = st.columns(2)

if current_price:
    with col3:
        buy_shares = st.number_input("매수 수량 (주)", min_value=1, step=1)
        if st.button("매수하기"):
            cost = buy_shares * current_price
            if st.session_state.money >= cost:
                st.session_state.money -= cost
                
                # 매입 단가 업데이트
                if TICKER not in st.session_state.portfolio:
                    st.session_state.portfolio[TICKER] = {'shares': 0, 'price': 0}
                
                total_shares = st.session_state.portfolio[TICKER]['shares'] + buy_shares
                total_cost = (st.session_state.portfolio[TICKER]['shares'] * st.session_state.portfolio[TICKER]['price']) + cost
                st.session_state.portfolio[TICKER]['shares'] = total_shares
                st.session_state.portfolio[TICKER]['price'] = total_cost / total_shares
                
                st.success(f"{buy_shares}주를 매수했습니다!")
                time.sleep(1) # 메시지 확인 시간
                st.experimental_rerun()
            else:
                st.error("잔액이 부족합니다.")

    with col4:
        sell_shares = st.number_input("매도 수량 (주)", min_value=1, step=1)
        if st.button("매도하기"):
            if TICKER in st.session_state.portfolio and st.session_state.portfolio[TICKER]['shares'] >= sell_shares:
                st.session_state.portfolio[TICKER]['shares'] -= sell_shares
                st.session_state.money += sell_shares * current_price
                
                if st.session_state.portfolio[TICKER]['shares'] == 0:
                    del st.session_state.portfolio[TICKER]
                
                st.success(f"{sell_shares}주를 매도했습니다!")
                time.sleep(1) # 메시지 확인 시간
                st.experimental_rerun()
            else:
                st.error("보유 수량이 부족합니다.")
else:
    st.info("유효한 종목 코드를 입력하여 거래를 시작하세요.")

# --- 앱 초기화 ---
st.markdown("---")
if st.button("시뮬레이션 초기화"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()
