import random
import sys
import pygame
from pygame.locals import *
from settings import Settings
from images_sounds import ImageSounds
from game_stats import GameStats
from scoreboard import ScoreBoard


def exit_game(event):
    """Проверяет, были ли нажаты Esc или крестик, и завершает работу игры, если да"""
    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
        pygame.quit()
        sys.exit()


class FlappyBird:
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру, создаёт игровые ресурсы и получает настройки"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.im_s = ImageSounds()
        self.game_stats = GameStats(self)
        self.scoreboard = ScoreBoard(self)
        pygame.display.set_caption('Flappy Bird')
        self.fps_clock = pygame.time.Clock()
        self.player_x = self.player_y = self.upper_pipes = self.lower_pipes = None

    def welcome_screen(self):
        """Показывает пользователю приветственный экран игры с заставкой"""
        self.scoreboard.set_welcome_objects()

        while True:
            for event in pygame.event.get():
                # Если была нажата клавиша Esc или крестик окна, то игра закрывается и завершается
                exit_game(event)
                # Если нажали пробел или кнопку вверх, то игра начинается
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    return
                # Если ничего не нажали или нажали кнопки без действий, экран просто обновляется
                else:
                    self.screen.blit(self.im_s.game_images['background'], (0, 0))
                    self.screen.blit(self.im_s.game_images['message'], (self.scoreboard.message_x,
                                                                        self.scoreboard.message_y))
                    self.screen.blit(self.im_s.game_images['player'], (self.player_x, self.player_y))
                    self.screen.blit(self.im_s.game_images['title'], (self.scoreboard.title_x, self.scoreboard.title_y))
                    pygame.display.update()
                    self.fps_clock.tick(self.settings.fps)

    def run_game(self):
        """Основной метод игры"""
        # Обнуляем текущий счёт при первом запуске или рестарте игры
        self.game_stats.update_score()
        # Располагаем птичку игрока посередине слева в экране
        self.player_x = int(self.settings.screen_width / 8)
        self.player_y = int(self.settings.screen_height / 2)
        # Генерируем первые колонны и разбиваем их части по спискам отдельно для верхних и отдельно для нижних колонн
        self.generate_first_pipes()

        # Проверяем на события во время игры
        while True:
            for event in pygame.event.get():
                # Если во время игры нажали Esc или крестик, то игра завершается
                exit_game(event)
                # Если во время игры нажали пробел или стрелочку вверх, то
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    # Если птичка не выше верхней границы окна, то
                    if self.player_y > 0:
                        # игрок перемещается по оси оу и воспроизводится звук взмаха крыльями
                        self.settings.playerVelY = self.settings.playerFlapVel
                        self.settings.playerFlapped = True
                        self.im_s.game_sounds['wing'].play()

            # Во время движения птицы и колонн происходит проверка на коллизии (взаимодействовали ли птичка и колонна)
            # Если мы врезались или взлетели слишком высоко, игра начинается заново с приветственного экрана
            if self.check_collision():
                return

            # Определяем, проходит ли птичка между верхней и нижней колоннами
            player_mid_position = self.player_x + self.im_s.game_images['player'].get_width() / 2
            for pipe in self.upper_pipes:
                pipe_mid_position = pipe['x'] + self.im_s.game_images['pipe'][0].get_width() / 2
                # Если птичка проходит, то увеличиваем текущий счёт на 1 и воспроизводим звук преодоления препятствия
                if pipe_mid_position <= player_mid_position < pipe_mid_position + 4:
                    self.game_stats.score += 1
                    if self.game_stats.score > self.game_stats.high_score:
                        self.game_stats.high_score += 1
                    print(f"Your Score is {self.game_stats.score}")
                    self.im_s.game_sounds['point'].play()

            # Если птичка не в самом низу и игрок не взлетает, то птичка падает вниз
            if self.settings.playerVelY < self.settings.playerMaxVelY and not self.settings.playerFlapped:
                self.settings.playerVelY += self.settings.playerAccY
            # Если игрок взмахнул крыльями и звук воспроизвёлся, то перед следующим обновлением свойство становится
            # False, т.к. птица ещё не взмахнула крыльями
            if self.settings.playerFlapped:
                self.settings.playerFlapped = False
            # Изменяем позицию птички по оси оу
            player_height = self.im_s.game_images['player'].get_height()
            self.player_y = self.player_y + min(self.settings.playerVelY, self.settings.ground_y -
                                                self.player_y - player_height)

            # После передвижения птички и проверки на коллизии обновляем положение колонн, которые двигаются влево
            for upperPipe, lowerPipe in zip(self.upper_pipes, self.lower_pipes):
                upperPipe['x'] += self.settings.pipeVelX
                lowerPipe['x'] += self.settings.pipeVelX

            # Удаляем из списков верхние и нижние колонны ушедшие за границу экрана влево колонны и добавляем новые
            self.add_pop_pipes()
            # Обновляем отображённые на экране объекты и выводим текущий счёт
            self.screen_update()

    def add_pop_pipes(self):
        """Проверяем местоположение колонн, удаляем ушедшие, добавляем новые в списки верхних и нижних колонн"""
        # Если количество колонн не 0 и больше 5, то в список добавляется новая колонна
        if 0 < self.upper_pipes[0]['x'] < 5:
            new_pipe = self.get_random_pipe()
            self.upper_pipes.append(new_pipe[0])
            self.lower_pipes.append(new_pipe[1])

        # Если колонна уехала влево за край экрана, её верхняя и нижняя части удаляются из списков верхних и нижних
        if self.upper_pipes[0]['x'] < -self.im_s.game_images['pipe'][0].get_width():
            self.upper_pipes.pop(0)
            self.lower_pipes.pop(0)

    def screen_update(self):
        """Обновляет отображённые на экране объекты и выводит текущий счёт"""
        # Обновляем картинку на заднем фоне
        self.screen.blit(self.im_s.game_images['background'], (0, 0))
        # Обновляем картинки колонн, ещё оставшихся на экране
        for upperPipe, lowerPipe in zip(self.upper_pipes, self.lower_pipes):
            self.screen.blit(self.im_s.game_images['pipe'][0], (upperPipe['x'], upperPipe['y']))
            self.screen.blit(self.im_s.game_images['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        # Обновляем положение игрока на экране
        self.screen.blit(self.im_s.game_images['player'], (self.player_x, self.player_y))
        # Выводим счёт на экране
        self.game_stats.show_score()
        # Обновляем элементы и их позиции на экране игры
        pygame.display.update()
        self.fps_clock.tick(self.settings.fps)

    def generate_first_pipes(self):
        """Генерирует первые две колонны и добавляет отдельно 2 верхние и 2 нижние в список словарей"""
        # Формируем колонны, между которыми игрок должен будет пролететь
        new_pipe1 = self.get_random_pipe()
        new_pipe2 = self.get_random_pipe()

        # Создаём два списка, хранящих по две колонны: верхний список хранит 2 верхние колонны, нижний - 2 нижние
        self.upper_pipes = [
            {'x': self.settings.screen_width + 200, 'y': new_pipe1[0]['y']},
            {'x': self.settings.screen_width + 200 + (self.settings.screen_width / 2), 'y': new_pipe2[0]['y']}
        ]
        self.lower_pipes = [
            {'x': self.settings.screen_width + 200, 'y': new_pipe1[1]['y']},
            {'x': self.settings.screen_width + 200 + (self.settings.screen_width / 2), 'y': new_pipe2[1]['y']}
        ]

    def check_collision(self):
        """Проверяет, произошли ли столкновения птички с верхом экрана или колонной"""
        # Если птичка взлетела слишком высоко или провалилась вниз, то засчитывается столкновение
        if self.player_y > self.settings.ground_y - 25 or self.player_y < 0:
            self.im_s.game_sounds['hit'].play()
            return True

        # Проверяются все верхние колонны
        for pipe in self.upper_pipes:
            pipe_height = self.im_s.game_images['pipe'][0].get_height()
            if (self.player_y < pipe_height + pipe['y']) and (
                    abs(self.player_x - pipe['x']) < self.im_s.game_images['pipe'][0].get_width() - 150):
                self.im_s.game_sounds['hit'].play()
                return True

        # Проверяются все нижние колонны
        for pipe in self.lower_pipes:
            if (self.player_y + self.im_s.game_images['player'].get_height() > pipe['y']) and (
                    abs(self.player_x - pipe['x']) < self.im_s.game_images['pipe'][0].get_width() - 150):
                self.im_s.game_sounds['hit'].play()
                return True

        return False

    def get_random_pipe(self):
        """Метод, создающий колонну в случайном месте"""
        # Высота колонны равна высоте картинки колонны
        pipe_height = self.im_s.game_images['pipe'][0].get_height()
        # Расстояние между верхней и нижней колонной, где должна пролететь птичка
        offset = self.settings.screen_height / 3

        # Определяем координату верхней колонны по у, как расстояние между колоннами + число до 0.6 от высоты окна игры
        y2 = offset + random.randrange(0, int(self.settings.screen_height - 1.2 * offset))
        # Общая координата колонн по х
        x = self.settings.screen_width + 10
        # Координата нижней колонны по у
        y1 = pipe_height - y2 + offset
        # Упаковываем описание колонны в список словарей, хранящих координаты верхней и нижней колонн
        pipe = [
            {'x': x, 'y': -y1},
            {'x': x, 'y': y2}
        ]
        # Возвращаем комплект из верхней и нижней колонн
        return pipe


if __name__ == "__main__":
    # Создание экземпляра и запуск игры
    fb = FlappyBird()

    while True:
        fb.welcome_screen()
        fb.run_game()
