class ScoreBoard:
    """Класс вывода игровой информации"""
    def __init__(self, fb_game):
        """Инициализирует атрибуты подсчёта"""
        self.message_x = self.message_y = self.title_x = self.title_y = None
        self.settings = fb_game.settings
        self.im_s = fb_game.im_s
        self.game = fb_game

    def set_welcome_objects(self):
        """Отображает объекты на экране заставки: птичку, название игры, надпись перед началом игры"""
        # Располагаем значок птички на экране
        self.game.player_x = int(self.settings.screen_width / 8)
        self.game.player_y = int((self.settings.screen_height - self.im_s.game_images['player'].get_height()) / 2)
        # Располагаем приветственный фон с надписью игры
        self.message_x = int((self.settings.screen_width - self.im_s.game_images['message'].get_width()) / 2)
        self.message_y = int(self.settings.screen_height * 0.2)
        # Располагаем название игры в верхней части экрана на заставке
        self.title_x = int((self.settings.screen_width - self.im_s.game_images['message'].get_width()) / 2)
        self.title_y = int(self.settings.screen_height * 0.04)
