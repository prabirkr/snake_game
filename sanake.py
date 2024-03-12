import pygame
import sys
import time
import random

class SnakeGame:
    def __init__(self):
        pygame.init()

        # Colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)  # New color for snake

        # Window settings
        self.window_width = 800
        self.window_height = 600

        self.gameDisplay = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('snake')
        self.font = pygame.font.SysFont(None, 25, bold=True)
        pygame.mixer.init()

        # Load background music
        pygame.mixer.music.load(".\Bac.mp3")

        # Load bite sound effect
        self.bite_sound = pygame.mixer.Sound("bite.wav")

        # Game variables
        self.clock = pygame.time.Clock()
        self.FPS = 10 # Increased FPS for faster apple displacement
        self.blockSize = 20
        self.noPixel = 0

        # Snake variables
        self.lead_x = self.window_width / 2
        self.lead_y = self.window_height / 2
        self.change_pixels_of_x = 0
        self.change_pixels_of_y = 0
        self.snakelist = []
        self.snakeLength = 1

        # Apple variables
        self.randomAppleX = round(random.randrange(0, self.window_width - self.blockSize) / 10.0) * 10.0
        self.randomAppleY = round(random.randrange(0, self.window_height - self.blockSize) / 10.0) * 10.0

        # Timer variables
        self.last_apple_move = pygame.time.get_ticks()  # Initialize timer

        # Start playing background music
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely

    def myquit(self):
        pygame.quit()
        sys.exit(0)

    def drawGrid(self):
        sizeGrd = self.window_width // self.blockSize
        for x in range(0, self.window_width, self.blockSize):
            pygame.draw.line(self.gameDisplay, self.black, (x, 0), (x, self.window_height))
        for y in range(0, self.window_height, self.blockSize):
            pygame.draw.line(self.gameDisplay, self.black, (0, y), (self.window_width, y))

    def snake(self):
        for size in self.snakelist:
            pygame.draw.rect(self.gameDisplay, self.green, [size[0] + 5, size[1], self.blockSize, self.blockSize])  # Use green color for snake

    def message_to_screen(self, msg, color):
        screen_text = self.font.render(msg, True, color)
        self.gameDisplay.blit(screen_text, [self.window_width / 2, self.window_height / 2])

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameExit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.myquit()
                elif event.key == pygame.K_LEFT:
                    self.change_pixels_of_x = -self.blockSize
                    self.change_pixels_of_y = self.noPixel
                elif event.key == pygame.K_RIGHT:
                    self.change_pixels_of_x = self.blockSize
                    self.change_pixels_of_y = self.noPixel
                elif event.key == pygame.K_UP:
                    self.change_pixels_of_y = -self.blockSize
                    self.change_pixels_of_x = self.noPixel
                elif event.key == pygame.K_DOWN:
                    self.change_pixels_of_y = self.blockSize
                    self.change_pixels_of_x = self.noPixel

    def check_collision(self):
        if (
            self.lead_x >= self.window_width
            or self.lead_x < 0
            or self.lead_y >= self.window_height
            or self.lead_y < 0
        ):
            self.gameOver = True

    def update_snake_and_display(self):
        self.lead_x += self.change_pixels_of_x
        self.lead_y += self.change_pixels_of_y

        self.gameDisplay.fill(self.black)  # Fill background with black color

        AppleThickness = 20

        pygame.draw.rect(
            self.gameDisplay, self.red, [self.randomAppleX, self.randomAppleY, AppleThickness, AppleThickness]
        )

        allspriteslist = [self.lead_x, self.lead_y]
        self.snakelist.append(allspriteslist)

        if len(self.snakelist) > self.snakeLength:
            del self.snakelist[0]

        for eachSegment in self.snakelist[:-1]:
            if eachSegment == allspriteslist:
                self.gameOver = True

        self.snake()
        pygame.display.update()

        current_time = pygame.time.get_ticks()
        if current_time - self.last_apple_move > 2500:  # Move apple every 2.5 seconds
            self.last_apple_move = current_time
            self.randomAppleX = round(random.randrange(0, self.window_width - self.blockSize) / 10.0) * 10.0
            self.randomAppleY = round(random.randrange(0, self.window_height - self.blockSize) / 10.0) * 10.0

    def game_loop(self):
        self.gameExit = False
        self.gameOver = False

        while not self.gameExit:
            while self.gameOver:
                self.gameDisplay.fill(self.green)
                self.message_to_screen("Game over", self.red)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.gameOver = False
                        self.gameExit = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.gameExit = True
                            self.gameOver = False
                        if event.key == pygame.K_c:
                            self.game_loop()

            self.handle_events()
            self.check_collision()
            self.update_snake_and_display()

            self.clock.tick(self.FPS)

        # Stop playing background music when the game is over
        pygame.mixer.music.stop()
        self.myquit()

if __name__ == "__main__":
    game = SnakeGame()
    game.game_loop()
