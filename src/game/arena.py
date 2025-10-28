import pygame
from pygame.locals import K_1, K_2, K_ESCAPE, KEYDOWN, QUIT

from src.settings import COLOR_BLACK, COLOR_WHITE, FPS, WINDOW_HEIGHT, WINDOW_WIDTH
from src.game.snake.game import SnakeGame
from src.game.tictactoe.game import TicTacToeGame


class Arena:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("AI Algorithm Arena")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_large = pygame.font.Font(None, 64)
        self.font_small = pygame.font.Font(None, 28)
        self.menu_message = ""

    def main_menu(self) -> None:
        while self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    elif event.key == K_1:
                        SnakeGame(self.screen).run()
                    elif event.key == K_2:
                        self._launch_tictactoe()
            self._draw_menu()
            pygame.display.flip()
        pygame.quit()

    def _draw_menu(self) -> None:
        self.screen.fill(COLOR_BLACK)
        title = self.font_large.render("AI Algorithm Arena", True, COLOR_WHITE)
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, WINDOW_HEIGHT // 4))

        options = [
            "[1] Pathfinding Arena (Snake)",
            "[2] Tic-Tac-Toe Arena",
            "[ESC] Quit",
        ]
        for idx, text in enumerate(options):
            surface = self.font_small.render(text, True, COLOR_WHITE)
            self.screen.blit(
                surface,
                (WINDOW_WIDTH // 2 - surface.get_width() // 2, WINDOW_HEIGHT // 2 + idx * 40),
            )

        if self.menu_message:
            message_surface = self.font_small.render(self.menu_message, True, COLOR_WHITE)
            self.screen.blit(
                message_surface,
                (WINDOW_WIDTH // 2 - message_surface.get_width() // 2, WINDOW_HEIGHT - 80),
            )

    def _launch_tictactoe(self) -> None:
        self.menu_message = ""
        TicTacToeGame(self.screen).run()

    def quit(self) -> None:
        pygame.quit()


if __name__ == "__main__":
    arena = Arena()
    arena.main_menu()