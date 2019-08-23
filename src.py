import pygame


class TicTacToe:
    # Screen Setup
    WIDTH = 0
    HEIGHT = 0
    WINDOW = None
    SCREEN = None
    TRANSPARENT = None

    # Player Pieces
    BLOCK_SIZE = 20
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
            done, player, state = self.play_game(done, grid, player, state)
            clock.tick(60)

    def initialize_game(self):
        pygame.init()
        player = 0
        done = False
        state = "PLAYING"
        grid = self.initialize_grid()
        return done, grid, player, state

    def initialize_grid(self):
        grid = []
        for x in range(30):
            grid.append([])
            for y in range(30):
                rect = pygame.Rect(x * (self.BLOCK_SIZE + 1), y * (self.BLOCK_SIZE + 1),
                                   self.BLOCK_SIZE, self.BLOCK_SIZE)
                grid[x].append([rect, None])
                pygame.draw.rect(self.SCREEN, (255, 255, 255), rect)
        return grid

    def play_game(self, done, grid, player, state):
        if state == "MENU":
            pass
        elif state == "PLAYING":
            done, player, state = self.play(done, grid, player, state)
        elif state == "GAME-OVER":
            done = self.game_over(done, player)
        pygame.display.flip()
        return done, player, state

    def play(self, done, grid, player, state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONUP:
                player, state = self.make_move(grid, player, state)
        return done, player, state

    def make_move(self, grid, player, state):
        change_player = False
        symbol = "X" if player == 0 else "O"
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                print(cell[1])
                if cell[0].collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and cell[1] is None:
                    change_player = True
                    self.draw_move(cell, symbol)

                    left_bound, lower_bound, right_bound, upper_bound = self.calculate_boundary(i, j)
                    # Check for horizontal line
                    state = self.check_horizontal_line(0, grid, i, j, left_bound, right_bound, state, symbol)
                    # Check for vertical line
                    state = self.check_vertical_line(0, grid, i, j, lower_bound, upper_bound, state, symbol)
                    # Check for diagonal line
                    offset = zip(range(i - left_bound, i + right_bound + 1), range(j - upper_bound, j + lower_bound + 1))
                    state = self.check_diagonal_line(0, grid, offset, state, symbol)
                    # Check for diagonal line (from bottom-left to top-right)
                    offset = zip(range(i - left_bound, i + right_bound + 1), reversed(range(j - upper_bound, j + lower_bound + 1)))
                    state = self.check_diagonal_line(0, grid, offset, state, symbol)

        if change_player:
            player = 1 - player
        return player, state

    def draw_move(self, cell, symbol):
        self.SCREEN.blit(self.FONT.render(symbol, True, (255, 0, 0)), (cell[0][0] + 5, cell[0][1] + 1))
        cell[1] = symbol

    def calculate_boundary(self, i, j):
        upper_bound = 4 if j + 1 > 4 else j
        lower_bound = 4 if 30 - (j + 1) > 4 else 30 - (j + 1)
        left_bound = 4 if i + 1 > 4 else i
        right_bound = 4 if 30 - (i + 1) > 4 else 30 - (i + 1)
        return left_bound, lower_bound, right_bound, upper_bound

    def check_horizontal_line(self, counter, grid, i, j, left_bound, right_bound, state, symbol):
        for index in range(i - left_bound, i + right_bound + 1):
            counter, state = self.check_if_won(counter, grid, index, j, state, symbol)
        return state

    def check_vertical_line(self, counter, grid, i, j, lower_bound, upper_bound, state, symbol):
        for index in range(j - upper_bound, j + lower_bound + 1):
            counter, state = self.check_if_won(counter, grid, i, index, state, symbol)
        return state

    def check_diagonal_line(self, counter, grid, offset, state, symbol):
        for i_offset, j_offset in offset:
            counter, state = self.check_if_won(counter, grid, i_offset, j_offset, state, symbol)
        return state

    def check_if_won(self, counter, grid, index, j, state, symbol):
        if grid[index][j][1] == symbol:
            counter += 1
        else:
            counter = 0
        if counter == 5:
            state = "GAME-OVER"
        return counter, state

    def game_over(self, done, player):
        print(f"Player {1 - player + 1} wins")
        input()
        done = True
        return done


game = TicTacToe()
game.execute()
