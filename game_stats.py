class GameStats:
    """Отслеживание статистики для игры"""
    def __init__(self, fb_game):
        """Инициализирует статистику"""
        self.score = 0
        self.high_score = 0
        self.settings = fb_game.settings
        self.im_s = fb_game.im_s
        self.screen = fb_game.screen

    def update_score(self):
        """Обновляет текущий счёт после столкновения"""
        self.score = 0

    def show_score(self):
        """Выводит количество очков на экране цифрами в виде картинок"""
        digits = [int(x) for x in list(str(self.score))]
        digits_high = [int(x) for x in list(str(self.high_score))]
        width = 0
        for digit in digits:
            width += self.im_s.game_images['numbers'][digit].get_width()
        # Выводит текущий счёт попытки слева
        x_offset = (self.settings.screen_width - width) / 3

        self.screen.blit(self.im_s.game_images['score'], (x_offset, self.settings.screen_height * 0.04))
        for digit in digits:
            self.screen.blit(self.im_s.game_images['numbers'][digit], (x_offset, self.settings.screen_height * 0.12))
            x_offset += self.im_s.game_images['numbers'][digit].get_width()

        # Выводим лучший счёт справа
        x_offset = (self.settings.screen_width - width) / 3 * 2

        self.screen.blit(self.im_s.game_images['high_score'], (x_offset, self.settings.screen_height * 0.04))
        for digit in digits_high:
            self.screen.blit(self.im_s.game_images['numbers'][digit], (x_offset, self.settings.screen_height * 0.12))
            x_offset += self.im_s.game_images['numbers'][digit].get_width()

    def show_high_score(self):
        """Отображает рекорд за все сыгранные попытки"""

