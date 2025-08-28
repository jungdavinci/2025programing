import streamlit as st
import random

# 세션 상태(Session State) 초기화
if "game_state" not in st.session_state:
    st.session_state.game_state = "playing"
    st.session_state.money = 0
    st.session_state.materials = 0
    st.session_state.factories = 0
    st.session_state.goal = 1000

st.title("타이쿤 게임: 공장을 건설하고 돈을 벌어보세요!")
st.markdown("---")

# 게임 오버/승리 상태 체크
if st.session_state.game_state == "win":
    st.balloons()
    st.success(f"축하합니다! 목표 금액 ${st.session_state.goal}을 달성했습니다!")
    st.write("게임을 다시 시작하려면 아래 버튼을 눌러주세요.")
    if st.button("다시 시작하기"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()
elif st.session_state.game_state == "playing":
    # 현재 상태 표시
    st.subheader(f"현재 자산: ${st.session_state.money}")
    st.write(f"보유 재료: {st.session_state.materials}개")
    st.write(f"공장 수: {st.session_state.factories}개")
    st.write(f"목표 금액: ${st.session_state.goal}")
    st.markdown("---")

    # 버튼 레이아웃
    col1, col2, col3 = st.columns(3)

    # 재료 수집 버튼
    with col1:
        if st.button("재료 수집"):
            acquired_materials = random.randint(3, 8)
            st.session_state.materials += acquired_materials
            st.success(f"재료 {acquired_materials}개를 획득했습니다!")
    
    # 공장 건설 버튼
    with col2:
        if st.button("공장 건설 (재료 10개 소모)"):
            if st.session_state.materials >= 10:
                st.session_state.materials -= 10
                st.session_state.factories += 1
                st.info("공장을 건설했습니다!")
            else:
                st.warning("재료가 부족합니다. 재료를 더 모아주세요.")

    # 생산 및 판매 버튼
    with col3:
        if st.button("생산 및 판매"):
            if st.session_state.factories > 0:
                # 공장 1개당 10~20원 수익
                profit = st.session_state.factories * random.randint(10, 20)
                st.session_state.money += profit
                st.success(f"생산 및 판매를 완료하여 ${profit}을 벌었습니다!")
            else:
                st.warning("공장이 없습니다. 먼저 공장을 건설하세요.")

    # 승리 조건 체크
    if st.session_state.money >= st.session_state.goal:
        st.session_state.game_state = "win"
        st.experimental_rerun()
