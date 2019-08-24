import pygame


# TODO:
# 1. Implement menu screen
# 2. Implement game-over screen
# 3. Implement sandwich rule: if 5 pieces of one player are sandwiched between 2 pieces of the other player, those 5
# pieces won't count as a win
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
        """

        """
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
        """

        :return: None
        """
        done, grid, player, state = self.initialize_game()
        clock = pygame.time.Clock()
        while not done:
            done, player, state = self.run_game(done, grid, player, state)
            clock.tick(60)

    def initialize_game(self):
        """

        :return:
        """
        pygame.init()
        player = 0
        done = False
        state = "PLAYING"
        grid = self.initialize_grid()
        return done, grid, player, state

    def initialize_grid(self):
        """

        :return:
        """
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
        """

        :param done:
        :param grid:
        :param player:
        :param state:
        :return:
        """
        if state == "MENU":
            pass
        elif state == "PLAYING":
            done, player, state = self.play(done, grid, player, state)
        elif state == "GAME-OVER":
            done = self.game_over(player)
        pygame.display.flip()
        return done, player, state

    def play(self, done, grid, player, state):
        """

        :param done:
        :param grid:
        :param player:
        :param state:
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True, None, "GAME-OVER"
            if event.type == pygame.MOUSEBUTTONUP:
                player, state = self.make_move(grid, player, state)
        return done, player, state

    def make_move(self, grid, player, state):
        """

        :param grid:
        :param player:
        :param state:
        :return:
        """
        change_player = False
        symbol = "X" if player == 0 else "O"
        for i, _ in enumerate(grid):
            for j, _ in enumerate(grid[i]):
                mouse_position = pygame.mouse.get_pos()
                if grid[i][j][0].collidepoint(mouse_position[0], mouse_position[1]) and grid[i][j][1] is None:
                    change_player = True
                    self.draw_move(grid[i][j], symbol)
                    left_limit, top_limit, right_limit, bottom_limit = self.calculate_four_boundaries(i, j)
                    state = self.method_name(grid, symbol, i, j, left_limit, right_limit, top_limit, bottom_limit)

        if change_player:
            player = 1 - player
        return player, state

    def method_name(self, grid, symbol, i, j, left_limit, right_limit, top_limit, bottom_limit):
        if self.check_horizontal_line(0, grid, i, j, left_limit, right_limit, symbol):
            return "GAME-OVER"

        if self.check_vertical_line(0, grid, i, j, top_limit, bottom_limit, symbol):
            return "GAME-OVER"

        offset = zip(range(i - left_limit, i + right_limit + 1), range(j - top_limit, j + bottom_limit + 1))
        if self.check_diagonal_line(0, grid, offset, symbol):
            return "GAME-OVER"

        offset = zip(range(i - left_limit, i + right_limit + 1), reversed(range(j - top_limit, j + bottom_limit + 1)))
        if self.check_diagonal_line(0, grid, offset, symbol):
            return "GAME-OVER"

        return "PLAYING"

    def draw_move(self, cell, symbol):
        """

        :param cell:
        :param symbol:
        :return: None
        """
        self.SCREEN.blit(self.FONT.render(symbol, True, (255, 0, 0)), (cell[0][0] + 5, cell[0][1] + 1))
        cell[1] = symbol

    def calculate_four_boundaries(self, i, j):
        """

        :param i:
        :param j:
        :return:
        """
        top_limit, bottom_limit = self.calculate_pair_boundaries(j)
        left_limit, right_limit = self.calculate_pair_boundaries(i)
        return left_limit, top_limit, right_limit, bottom_limit

    @staticmethod
    def calculate_pair_boundaries(j):
        first = 4 if j + 1 > 4 else j
        second = 4 if 30 - (j + 1) > 4 else 30 - (j + 1)
        return first, second

    @staticmethod
    def check_horizontal_line(counter, grid, i, j, left_limit, right_limit, symbol):
        for index in range(i - left_limit, i + right_limit + 1):
            if grid[index][j][1] == symbol:
                counter += 1
            else:
                counter = 0 if counter < 5 else counter
        if counter == 5:
            return True
        return False

    @staticmethod
    def check_vertical_line(counter, grid, i, j, top_limit, bottom_limit, symbol):
        for index in range(j - top_limit, j + bottom_limit + 1):
            if grid[i][index][1] == symbol:
                counter += 1
            else:
                counter = 0 if counter < 5 else counter
        if counter == 5:
            return True
        return False

    @staticmethod
    def check_diagonal_line(counter, grid, offset, symbol):
        for i_offset, j_offset in offset:
            if grid[i_offset][j_offset][1] == symbol:
                counter += 1
            else:
                counter = 0 if counter < 5 else counter
        if counter == 5:
            return True
        return False

    @staticmethod
    def game_over(player):
        if player is not None:
            print(f"Player {1 - player + 1} wins")
        input()
        return True


game = TicTacToe()
game.execute()
