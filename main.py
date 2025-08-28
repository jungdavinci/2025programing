import streamlit as st
import random
import time

# --- 게임 초기화 ---
if "game_state" not in st.session_state:
    st.session_state.game_state = "playing"
    st.session_state.player_pos = [8, 5]  # [y, x]
    st.session_state.enemies = [[1, random.randint(0, 9)], [2, random.randint(0, 9)]]
    st.session_state.missiles = []
    st.session_state.score = 0
    st.session_state.game_board = [["" for _ in range(10)] for _ in range(10)]

def draw_board():
    board_str = ""
    for r, row in enumerate(st.session_state.game_board):
        for c, cell in enumerate(row):
            if cell == "":
                board_str += "⬜"
            else:
                board_str += cell
        board_str += "\n"
    st.text(board_str)

def update_game_state():
    # 게임 보드 초기화
    st.session_state.game_board = [["" for _ in range(10)] for _ in range(10)]
    
    # 미사일 이동 및 충돌 체크
    new_missiles = []
    for m_pos in st.session_state.missiles:
        m_pos[0] -= 1  # 위로 이동
        if m_pos[0] >= 0:
            new_missiles.append(m_pos)
            
            # 적기 충돌 체크
            hit = False
            for e_pos in st.session_state.enemies:
                if m_pos == e_pos:
                    st.session_state.enemies.remove(e_pos)
                    st.session_state.score += 10
                    hit = True
                    break
            if not hit:
                st.session_state.game_board[m_pos[0]][m_pos[1]] = "🚀"
    st.session_state.missiles = new_missiles
    
    # 적기 이동 및 충돌 체크
    for e_pos in st.session_state.enemies:
        e_pos[0] += 1  # 아래로 이동
        if st.session_state.player_pos == e_pos:
            st.session_state.game_state = "game over"
            return
        if e_pos[0] > 9:
            st.session_state.enemies.remove(e_pos)
            
    # 일정 턴마다 새로운 적기 생성
    if random.random() < 0.2 + (st.session_state.score / 200):  # 점수에 따라 확률 증가
        st.session_state.enemies.append([0, random.randint(0, 9)])
        
    # 게임 보드에 적기 그리기
    for e_pos in st.session_state.enemies:
        if 0 <= e_pos[0] < 10 and 0 <= e_pos[1] < 10:
            st.session_state.game_board[e_pos[0]][e_pos[1]] = "🚁"

    # 게임 보드에 플레이어 그리기
    if 0 <= st.session_state.player_pos[0] < 10 and 0 <= st.session_state.player_pos[1] < 10:
        st.session_state.game_board[st.session_state.player_pos[0]][st.session_state.player_pos[1]] = "✈️"
    else:
        st.session_state.game_state = "game over"

# --- UI 및 게임 로직 ---
st.title("2D 비행기 격추 게임")
st.markdown("---")

if st.session_state.game_state == "playing":
    st.sidebar.subheader("조작")
    
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        if st.button("⬅️"):
            st.session_state.player_pos[1] -= 1
    with col2:
        if st.button("⬆️"):
            st.session_state.player_pos[0] -= 1
    with col3:
        if st.button("➡️"):
            st.session_state.player_pos[1] += 1
            
    if st.sidebar.button("미사일 발사"):
        st.session_state.missiles.append([st.session_state.player_pos[0] - 1, st.session_state.player_pos[1]])
        
    update_game_state()
    draw_board()
    st.subheader(f"점수: {st.session_state.score}점")

elif st.session_state.game_state == "game over":
    st.error("게임 오버! 💥")
    st.subheader(f"최종 점수: {st.session_state.score}점")
    if st.button("다시 시작"):
        # 초기화
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()
