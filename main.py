import pygame

def run_game(level):
    pygame.init()

    # 화면 설정
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("미로 게임")

    # 색상
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)

    # 미로 맵 (예시)
    maze = [
        "################",
        "#P#   ## #     #",
        "# # # ## # ### #",
        "# # # ## # # # #",
        "#   #    # # # #",
        "### #### ### # #",
        "# # ## #   #   #",
        "# #    ## #### #",
        "# ######       #",
        "################"
    ]
    
    # 플레이어 설정
    player_size = 20
    player_pos = [0, 0]
    for r, row in enumerate(maze):
        if 'P' in row:
            player_pos = [r, row.index('P')]
            maze[r] = maze[r].replace('P', ' ')

    # 게임 루프
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # 키 입력 처리
            if event.type == pygame.KEYDOWN:
                old_pos = list(player_pos)
                if event.key == pygame.K_LEFT:
                    player_pos[1] -= 1
                if event.key == pygame.K_RIGHT:
                    player_pos[1] += 1
                if event.key == pygame.K_UP:
                    player_pos[0] -= 1
                if event.key == pygame.K_DOWN:
                    player_pos[0] += 1
                
                # 벽 충돌 체크
                if maze[player_pos[0]][player_pos[1]] == '#':
                    player_pos = old_pos

        # 화면 그리기
        screen.fill(black)
        
        # 미로 그리기
        cell_size = 50
        for r, row in enumerate(maze):
            for c, char in enumerate(row):
                if char == '#':
                    pygame.draw.rect(screen, blue, (c * cell_size, r * cell_size, cell_size, cell_size))
        
        # 플레이어 그리기
        pygame.draw.rect(screen, red, (player_pos[1] * cell_size, player_pos[0] * cell_size, player_size, player_size))
        
        pygame.display.flip()

    pygame.quit()
    return "Game Over"

if __name__ == '__main__':
    result = run_game(1)
    print(result)
