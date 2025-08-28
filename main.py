import streamlit as st
import random

# 세션 상태(Session State) 초기화
# 앱이 재실행되어도 변수 값을 유지하기 위해 사용합니다.
if "level" not in st.session_state:
    st.session_state.level = 1
    st.session_state.materials = 0

st.title("아이템 업그레이드 게임")
st.markdown("---")

# 현재 상태 표시
st.subheader(f"현재 아이템 레벨: {st.session_state.level}")
st.write(f"보유 재료: {st.session_state.materials}개")

# 재료 수집 버튼
if st.button("재료 수집"):
    st.session_state.materials += random.randint(1, 5)  # 1~5개 랜덤 획득
    st.success("재료를 획득했습니다!")
    
st.markdown("---")

# 업그레이드 버튼
# 재료가 충분할 때만 버튼이 활성화됩니다.
if st.session_state.materials >= 5:
    if st.button("업그레이드 (재료 5개 소모)"):
        st.session_state.materials -= 5
        
        # 업그레이드 확률
        success_rate = 100 / (st.session_state.level * 2)
        if random.uniform(0, 100) < success_rate:
            st.session_state.level += 1
            st.balloons() # 성공 시 풍선 효과
            st.success("업그레이드 성공! 🎉")
        else:
            st.error("업그레이드 실패 😭")
else:
    st.warning("재료가 부족합니다. 재료를 수집하세요.")

# 게임 리셋 버튼
st.markdown("---")
if st.button("게임 리셋"):
    st.session_state.level = 1
    st.session_state.materials = 0
    st.experimental_rerun() # 앱을 처음부터 다시 실행
