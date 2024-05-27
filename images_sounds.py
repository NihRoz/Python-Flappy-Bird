import pygame


class ImageSounds:
    """Класс, хранящий картинки и музыку из игры"""
    def __init__(self):
        """Загружает в словари картинки и звуковые эффекты"""
        self.game_images = {}
        self.game_sounds = {}

        # Game Images
        self.player = 'gallery/images/bird.png'
        self.background = 'gallery/images/background.png'
        self.pipe = 'gallery/images/pipe600_200_green_ok.png'
        self.title = 'gallery/images/title.png'

        self.game_images['numbers'] = (
            pygame.image.load('gallery/images/0.png').convert_alpha(),
            pygame.image.load('gallery/images/1.png').convert_alpha(),
            pygame.image.load('gallery/images/2.png').convert_alpha(),
            pygame.image.load('gallery/images/3.png').convert_alpha(),
            pygame.image.load('gallery/images/4.png').convert_alpha(),
            pygame.image.load('gallery/images/5.png').convert_alpha(),
            pygame.image.load('gallery/images/6.png').convert_alpha(),
            pygame.image.load('gallery/images/7.png').convert_alpha(),
            pygame.image.load('gallery/images/8.png').convert_alpha(),
            pygame.image.load('gallery/images/9.png').convert_alpha()
        )

        self.game_images['message'] = pygame.image.load('gallery/images/message.png').convert_alpha()
        self.game_images['pipe'] = (
            pygame.transform.rotate(pygame.image.load(self.pipe).convert_alpha(), 180),
            pygame.image.load(self.pipe).convert_alpha()
        )

        self.game_images['background'] = pygame.image.load(self.background).convert_alpha()
        self.game_images['player'] = pygame.image.load(self.player).convert_alpha()
        self.game_images['title'] = pygame.image.load(self.title).convert_alpha()
        # Рекорд и текущий счёт
        self.game_images['score'] = pygame.image.load('gallery/images/score (1).png').convert_alpha()
        self.game_images['high_score'] = pygame.image.load('gallery/images/high_score (1).png').convert_alpha()

        # Game Sounds
        self.game_sounds['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
        self.game_sounds['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
        self.game_sounds['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
        self.game_sounds['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
        self.game_sounds['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')