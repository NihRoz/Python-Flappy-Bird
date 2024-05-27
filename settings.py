class Settings:
    """Класс, хранящий настройки игры"""
    def __init__(self):
        """Инициализирует настройки игры"""
        self.fps = 60
        self.screen_width = 1200
        self.screen_height = 800
        self.ground_y = self.screen_height * 0.9

        # Назначаем скорости элементам
        # Скорость колонн по х
        self.pipeVelX = -4
        # Скорость птички игрока по у
        self.playerVelY = -9
        # Максимальная скорость движение птички по у
        self.playerMaxVelY = 10
        self.playerMinVelY = -8
        # Ускорение птички по у
        self.playerAccY = 1
        # Скорость падения птички без нажатия пробела или стрелочки вверх
        self.playerFlapVel = -8
        # Свойство, фиксирующее взмах (для воспроизведения звука взмаха)
        self.playerFlapped = False
