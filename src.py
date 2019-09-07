import math
import pygame
from tkinter import messagebox, Tk
from typing import List, Tuple


# TODO:
# 1. Implement menu screen
# 2. Add documentation
class TicTacToe:
    def __init__(self):
        # Player Pieces
        pygame.font.init()
        self.FONT = pygame.font.SysFont("Arial", 15)

        # Screen Setup
        self.MAX_PIECE = 30
        self.BLOCK_SIZE = 20
        self.WIDTH = self.MAX_PIECE * self.BLOCK_SIZE + self.MAX_PIECE
        self.HEIGHT = self.MAX_PIECE * self.BLOCK_SIZE + self.MAX_PIECE
        self.WINDOW = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.SCREEN = pygame.display.get_surface()
        self.TRANSPARENT = pygame.Surface([self.WIDTH, self.HEIGHT])
        self.TRANSPARENT.set_alpha(255)
        self.TRANSPARENT.fill((255, 255, 255))

    def execute(self):
        done, replay, grid, player, piece_count, state = self.initialize_game()
        while not done:
            done, replay, player, piece_count, state = self.run_game(done, grid, player, piece_count, state)
        if replay:
            self.execute()

    def initialize_game(self) -> Tuple[bool, bool, List[List], int, int, str]:
        pygame.init()
        player = 0
        piece_count = 0
        done, replay = False, False
        state = "PLAYING"
        grid = self.initialize_grid()
        return done, replay, grid, player, piece_count, state

    def initialize_grid(self) -> List[List]:
        grid = []
        for x in range(self.MAX_PIECE):
            grid.append([])
            for y in range(self.MAX_PIECE):
                rect = pygame.Rect(x * (self.BLOCK_SIZE + 1), y * (self.BLOCK_SIZE + 1),
                                   self.BLOCK_SIZE, self.BLOCK_SIZE)
                grid[x].append([rect, None])
                pygame.draw.rect(self.SCREEN, (255, 255, 255), rect)
        return grid

    def run_game(self, done, grid, player, piece_count, state):
        replay = False
        if state == "MENU":
            pass
        elif state == "PLAYING":
            player, piece_count, state = self.play(grid, player, piece_count, state)
        elif state == "GAME-OVER":
            done, replay = self.game_over(player, piece_count)
        pygame.display.flip()
        return done, replay, player, piece_count, state

    def play(self, grid, player, piece_count, state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quit")
                return None, piece_count, "GAME-OVER"
            if event.type == pygame.MOUSEBUTTONUP:
                player, piece_count, state = self.make_move(grid, player, piece_count, state)
        if piece_count == 25:
            state = "GAME-OVER"
        return player, piece_count, state

    def make_move(self, grid, player, piece_count, state):
        symbol = "X" if player == 0 else "O"
        i, j = math.floor(pygame.mouse.get_pos()[0] / 21), math.floor(pygame.mouse.get_pos()[1] / 21)
        if grid[i][j][1] is None:
            self.draw(grid[i][j], symbol)
            state = self.check_if_won(grid, symbol, i, j)
            piece_count += 1
            player = 1 - player
        return player, piece_count, state

    def draw(self, cell, symbol):
        self.SCREEN.blit(self.FONT.render(symbol, True, (255, 0, 0)), (cell[0][0] + 5, cell[0][1] + 1))
        cell[1] = symbol

    def check_if_won(self, grid, symbol, i, j):
        if self.count_horizontally(0, grid, i, j, 4, 4, symbol, 0):
            return "GAME-OVER"

        if self.count_vertically(0, grid, i, j, 4, 4, symbol, 1):
            return "GAME-OVER"

        offset = zip(range(i - 4, i + 4 + 1), range(j - 4, j + 4 + 1))
        if self.count_diagonally(0, grid, symbol, 2, offset):
            return "GAME-OVER"

        offset = zip(range(i - 4, i + 4 + 1), range(j + 4, j - 4 - 1, -1))
        if self.count_diagonally(0, grid, symbol, 3, offset):
            return "GAME-OVER"

        return "PLAYING"

    def count_horizontally(self, counter, grid, i, j, left_limit, right_limit, symbol, win_type):
        start, end = None, None
        for index in range(i - left_limit, i + right_limit + 1):
            if index in range(0, self.MAX_PIECE) and grid[index][j][1] == symbol:
                counter, start, end = self.count_symbol(counter, index, j, start, end)
            else:
                counter = 0 if counter < 5 else counter
        return self.check_winning_condition(counter, grid, symbol, win_type, start, end)

    def count_vertically(self, counter, grid, i, j, top_limit, bottom_limit, symbol, win_type):
        start, end = None, None
        for index in range(j - top_limit, j + bottom_limit + 1):
            if index in range(0, self.MAX_PIECE) and grid[i][index][1] == symbol:
                counter, start, end = self.count_symbol(counter, i, index, start, end)
            else:
                counter = 0 if counter < 5 else counter
        return self.check_winning_condition(counter, grid, symbol, win_type, start, end)

    def count_diagonally(self, counter, grid, symbol, win_type, offset):
        start, end = None, None
        for i_offset, j_offset in offset:
            if i_offset in range(0, self.MAX_PIECE) and j_offset in range(0, self.MAX_PIECE) and \
                    grid[i_offset][j_offset][1] == symbol:
                counter, start, end = self.count_symbol(counter, i_offset, j_offset, start, end)
            else:
                counter = 0 if counter < 5 else counter
        return self.check_winning_condition(counter, grid, symbol, win_type, start, end)

    @staticmethod
    def count_symbol(counter, i, j, start, end):
        counter += 1
        if counter == 1:
            start = (i, j)
        if counter == 5:
            end = (i, j)
        return counter, start, end

    def check_winning_condition(self, counter, grid, symbol, win_type, start, end):
        if counter == 5:
            if win_type == 0:
                return not self.check_horizontally(grid, start[0] - 1, start[1], end[0] + 1, end[1], symbol)
            if win_type == 1:
                return not self.check_vertically(grid, start[0], start[1] - 1, end[0], end[1] + 1, symbol)
            if win_type == 2:
                return not self.check_diagonally(grid, start[0] - 1, start[1] - 1, end[0] + 1, end[1] + 1, symbol)
            if win_type == 3:
                return not self.check_diagonally(grid, start[0] - 1, start[1] + 1, end[0] + 1, end[1] - 1, symbol)
        return False

    def check_horizontally(self, grid, start_i, start_j, end_i, end_j, symbol):
        left = start_i >= 0 and grid[start_i][start_j][1] is not None and grid[start_i][start_j][1] != symbol
        right = end_i < self.MAX_PIECE and grid[end_i][end_j][1] is not None and grid[end_i][end_j][1] != symbol
        return left and right

    def check_vertically(self, grid, start_i, start_j, end_i, end_j, symbol):
        top = start_j >= 0 and grid[start_i][start_j][1] is not None and grid[start_i][start_j][1] != symbol
        bottom = end_j < self.MAX_PIECE and grid[end_i][end_j][1] is not None and grid[end_i][end_j][1] != symbol
        return top and bottom

    def check_diagonally(self, grid, start_i, start_j, end_i, end_j, symbol):
        first = (start_i in range(0, self.MAX_PIECE) and start_j in range(0, self.MAX_PIECE) and
                 grid[start_i][start_j][1] is not None and grid[start_i][start_j][1] != symbol)
        second = (end_i < self.MAX_PIECE and end_j < self.MAX_PIECE and
                  grid[end_i][end_j][1] is not None and grid[end_i][end_j][1] != symbol)
        return first and second

    @staticmethod
    def game_over(player, piece_count):
        screen = Screen()
        winner = 2 - player if player is not None else None
        replay = screen.show_game_over_screen(winner, piece_count)
        return True, replay


class Screen:
    screen = None

    def __init__(self):
        self.screen = Tk()
        self.screen.wm_withdraw()

    @staticmethod
    def show_game_over_screen(winner, piece_count):
        if piece_count == 25:
            msg_box = messagebox.askquestion("Game Over", f"Draw. Play Again?")
        elif winner is None:
            return False
        else:
            msg_box = messagebox.askquestion("Game Over", f"Player {winner} won. Play Again?")
        if msg_box == "yes":
            return True
        else:
            return False


game = TicTacToe()
game.execute()
