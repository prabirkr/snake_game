def update_snake_and_display(self):
        self.lead_x += self.change_pixels_of_x
        self.lead_y += self.change_pixels_of_y

        self.gameDisplay.fill(self.white)

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

        if self.lead_x >= self.randomAppleX and self.lead_x <= self.randomAppleX + AppleThickness:
            if self.lead_y >= self.randomAppleY and self.lead_y <= self.randomAppleY + AppleThickness:
                # Play bite sound effect
                self.bite_sound.play()

                self.randomAppleX = round(random.randrange(0, self.window_width - self.blockSize) / 10.0) * 10.0
                self.randomAppleY = round(random.randrange(0, self.window_height - self.blockSize) / 10.0) * 10.0
