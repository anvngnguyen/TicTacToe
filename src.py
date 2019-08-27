import pygame
from typing import List, Tuple


# TODO:
# 1. Implement menu screen
# 2. Implement game-over screen
# 3. Add documentation
class TicTacToe:
    # Screen Variables
    WIDTH = 0
    HEIGHT = 0
    WINDOW = None
    SCREEN = None
    TRANSPARENT = None

    # Player Pieces Variables
    BLOCK_SIZE = 0
    FONT = None

    def __init__(self):
        # Screen Setup
        self.WIDTH = 630
        self.HEIGHT = 630
        self.WINDOW = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.SCREEN = pygame.display.get_surface()
        self.TRANSPARENT = pygame.Surface([self.WIDTH, self.HEIGHT])
        self.TRANSPARENT.set_alpha(255)
        self.TRANSPARENT.fill((255, 255, 255))

        # Player Pieces
        self.BLOCK_SIZE = 20
        pygame.font.init()
        self.FONT = pygame.font.SysFont("Arial", 15)

    def execute(self):
        done, grid, player, state = self.initialize_game()
        clock = pygame.time.Clock()
        while not done:
            done, player, state = self.run_game(done, grid, player, state)
            clock.tick(60)

    def initialize_game(self) -> Tuple[bool, List[List], int, str]:
        pygame.init()
        player = 0
        done = False
        state = "PLAYING"
        grid = self.initialize_grid()
        return done, grid, player, state

    def initialize_grid(self) -> List[List]:
        grid = []
        for x in range(30):
            grid.append([])
            for y in range(30):
                rect = pygame.Rect(x * (self.BLOCK_SIZE + 1), y * (self.BLOCK_SIZE + 1),
                                   self.BLOCK_SIZE, self.BLOCK_SIZE)
                grid[x].append([rect, None])
                pygame.draw.rect(self.SCREEN, (255, 255, 255), rect)
        return grid

    def run_game(self, done, grid, player, state):
        if state == "MENU":
            pass
        elif state == "PLAYING":
            done, player, state = self.play(done, grid, player, state)
        elif state == "GAME-OVER":
            done = self.game_over(player)
        pygame.display.flip()
        return done, player, state

    def play(self, done, grid, player, state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True, None, "GAME-OVER"
            if event.type == pygame.MOUSEBUTTONUP:
                player, state = self.make_move(grid, player, state)
        return done, player, state

    def make_move(self, grid, player, state):
        change_player = False
        symbol = "X" if player == 0 else "O"
        for i, _ in enumerate(grid):
            for j, _ in enumerate(grid[i]):
                mouse_position = pygame.mouse.get_pos()
                if grid[i][j][0].collidepoint(mouse_position[0], mouse_position[1]) and grid[i][j][1] is None:
                    change_player = True
                    self.draw_move(grid[i][j], symbol)
                    left_limit, top_limit, right_limit, bottom_limit = self.calculate_four_boundaries(i, j)
                    print(f"Check for {i}-{j}")
                    state = self.check_for_consecutive_move(grid, symbol, i, j, left_limit, right_limit, top_limit, bottom_limit)
        if change_player:
            player = 1 - player
        return player, state

    def draw_move(self, cell, symbol):
        self.SCREEN.blit(self.FONT.render(symbol, True, (255, 0, 0)), (cell[0][0] + 5, cell[0][1] + 1))
        cell[1] = symbol

    def check_for_consecutive_move(self, grid, symbol, i, j, left_limit, right_limit, top_limit, bottom_limit):
        if self.check_horizontal_line(0, grid, i, j, 4, 4, symbol, 0):
            return "GAME-OVER"

        if self.check_vertical_line(0, grid, i, j, 4, 4, symbol, 1):
            return "GAME-OVER"

        offset = zip(range(i - 4, i + 4 + 1), range(j - 4, j + 4 + 1))
        if self.check_diagonal_line(0, grid, symbol, 2, offset):
            return "GAME-OVER"

        offset = zip(range(i - 4, i + 4 + 1), range(j + 4, j - 4 - 1, -1))
        if self.check_diagonal_line(0, grid, symbol, 3, offset):
            return "GAME-OVER"

        return "PLAYING"

    def calculate_four_boundaries(self, i, j):
        top_limit, bottom_limit = self.calculate_pair_boundaries(j)
        left_limit, right_limit = self.calculate_pair_boundaries(i)
        return left_limit, top_limit, right_limit, bottom_limit

    @staticmethod
    def calculate_pair_boundaries(index):
        first = 4 if index + 1 > 4 else index
        second = 4 if 30 - (index + 1) > 4 else 30 - (index + 1)
        return first, second

    def check_horizontal_line(self, counter, grid, i, j, left_limit, right_limit, symbol, win_type):
        start, end = None, None
        for index in range(i - left_limit, i + right_limit + 1):
            if grid[index][j][1] == symbol:
                counter += 1
                if counter == 1:
                    start = (index, j)
                if counter == 5:
                    end = (index, j)
            else:
                counter = 0 if counter < 5 else counter
        return self.check_winning_condition(counter, grid, symbol, 0, start, end)

    def check_vertical_line(self, counter, grid, i, j, top_limit, bottom_limit, symbol, win_type):
        start, end = None, None
        for index in range(j - top_limit, j + bottom_limit + 1):
            if grid[i][index][1] == symbol:
                counter += 1
                if counter == 1:
                    start = (i, index)
                if counter == 5:
                    end = (i, index)
            else:
                counter = 0 if counter < 5 else counter
        return self.check_winning_condition(counter, grid, symbol, win_type, start, end)

    def check_diagonal_line(self, counter, grid, symbol, win_type, offset):
        start, end = None, None
        for i_offset, j_offset in offset:
            if grid[i_offset][j_offset][1] == symbol:
                counter += 1
                if counter == 1:
                    start = (i_offset, j_offset)
                if counter == 5:
                    end = (i_offset, j_offset)
            else:
                counter = 0 if counter < 5 else counter
        return self.check_winning_condition(counter, grid, symbol, win_type, start, end)

    @staticmethod
    def check_winning_condition(counter, grid, symbol, win_type, start, end):
        if counter == 5:
            if win_type == 0:
                print(f"Check win type {win_type}")
                left_cond = (start[0] - 1 >= 0 and grid[start[0] - 1][start[1]][1] is not None and
                             grid[start[0] - 1][start[1]][1] != symbol)
                right_cond = (end[0] + 1 < 30 and grid[end[0] + 1][end[1]][1] is not None and
                              grid[end[0] + 1][end[1]][1] != symbol)
                return not (left_cond and right_cond)
            if win_type == 1:
                print(f"Check win type {win_type}")
                top_cond = (start[1] - 1 >= 0 and grid[start[0]][start[1] - 1][1] is not None and
                            grid[start[0]][start[1] - 1][1] != symbol)
                bottom_cond = (end[1] + 1 < 30 and grid[end[0]][end[1] + 1][1] is not None and
                               grid[end[0]][end[1] + 1][1] != symbol)
                return not (top_cond and bottom_cond)
            if win_type == 2:
                print(f"Check win type {win_type}")
                top_left_cond = (start[0] - 1 >= 0 and start[1] - 1 >= 0 and
                                 grid[start[0] - 1][start[1] - 1][1] is not None and
                                 grid[start[0] - 1][start[1] - 1][1] != symbol)
                bottom_right_cond = (end[0] + 1 < 30 and end[1] + 1 < 30 and
                                     grid[end[0] + 1][end[1] + 1][1] is not None and
                                     grid[end[0] + 1][end[1] + 1][1] != symbol)
                return not (top_left_cond and bottom_right_cond)
            if win_type == 3:
                print(f"Check win type {win_type}")
                bottom_left_cond = (start[0] - 1 >= 0 and start[1] + 1 < 30 and
                                    grid[start[0] - 1][start[1] + 1][1] is not None and
                                    grid[start[0] - 1][start[1] + 1][1] != symbol)
                top_right_cond = (end[0] + 1 < 30 and end[1] - 1 >= 0 and
                                  grid[end[0] + 1][end[1] - 1][1] is not None and
                                  grid[end[0] + 1][end[1] - 1][1] != symbol)
                return not (bottom_left_cond and top_right_cond)
        return False

    @staticmethod
    def game_over(player):
        if player is not None:
            print(f"Player {1 - player + 1} wins")
        input()
        return True


game = TicTacToe()
game.execute()
