import pygame
from random import choice, uniform, randint

# создание словарей с размерами, цветами, результатами, текстового файла
window_width, window_height = 1280, 720
size_menu = w, h = 1280, 720
sizes = {'paddle': (40, 100), 'ball': (70, 70)}
position = {'player': (window_width - 50, window_height / 2), 'opponent': (50, window_height / 2)}
speed = {'player': 600, 'opponent': 250, 'ball': 500}
colors = {
    'paddle': 'white',
    'ball': (255, 182, 193),
    'bg': 'white'
}
file = open('extra/file.txt', mode="w")
results = {'Игрок с правой стороны:': 0,
           'Игрок с левой стороны:': 0}

# создание главного окна
pygame.init()
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()


# основной класс игры
class Game:
    def __init__(self):
        self.running = True

        self.bg_wallpaper = pygame.image.load('extra/main_bg.jpg')
        self.bg_wallpaper = pygame.transform.scale(self.bg_wallpaper, (1280, 720))
        self.surf = pygame.Surface((1280, 720))
        self.surf.fill('white')
        self.surf.set_alpha(150)
        # создание групп спрайтов
        self.menu_sprites = pygame.sprite.Group()
        self.level_sprites = pygame.sprite.Group()
        self.button_sprites = pygame.sprite.Group()

        self.all_sprites = pygame.sprite.Group()
        self.paddle_sprites = pygame.sprite.Group()
        self.star = Star(self.all_sprites)

        self.ball = Ball(self.all_sprites, self.paddle_sprites, self.update_score, self.star)

        self.opponent = Opponent((), self.ball)
        self.player2 = Player2(())

        self.player = Player((self.all_sprites, self.paddle_sprites))
        self.score = {'player': 0, 'opponent': 0}
        self.font = pygame.font.Font(None, 160)

        self.screen = pygame.display.set_mode(size_menu)
        self.text_lose = pygame.font.Font(None, 70).render('You lose!', False, (255, 99, 219))
        self.text_win = pygame.font.Font(None, 70).render('You win!', False, (255, 99, 219))
        self.text_player_left = pygame.font.Font(None, 70).render('Left player win!', False, (255, 99, 219))
        self.text_player_right = pygame.font.Font(None, 70).render('Right player win!', False, (255, 99, 219))

        self.text_restart = pygame.font.Font(None, 70).render('Начать заново', False, (255, 99, 219))
        self.rect_restart = self.text_restart.get_rect(topleft=(window_width / 2 - 170, window_height / 2 + 20))

        self.menu_bg = pygame.image.load('extra/start_bg.jpg')

        self.level1_button = Button('1 игрок', 540, 350, 200, 50, (255, 99, 219), (0, 0, 150))
        self.level2_button = Button('2 игрока', 540, 450, 200, 50, (255, 99, 219), (0, 0, 150))

    # отображение очков на экране
    def display_score(self):
        player_sc = self.font.render(str(self.score['player']), True, colors['ball'])
        player_rect = player_sc.get_rect(center=(window_width / 2 + 100, window_height / 2))
        display_surface.blit(player_sc, player_rect)

        opponent_sc = self.font.render(str(self.score['opponent']), True, colors['ball'])
        player_rect = opponent_sc.get_rect(center=(window_width / 2 - 100, window_height / 2))
        display_surface.blit(opponent_sc, player_rect)

        pygame.draw.line(display_surface, colors['ball'], (window_width / 2, 0), (window_width / 2, window_height), 5)

    # изменение очков на экране
    def update_score(self, side):
        if side == 'player':
            self.score['player'] += 1
        else:
            self.score['opponent'] += 1

    # запуск игры
    def run(self):
        FPS = 60
        self.ball.side = 0
        font = pygame.font.Font(None, 74)
        pause_text = font.render('Paused. Press ENTER to continue', True, 'black')
        paused = True
        self.gameplay = True
        clock.tick(120)
        self.pole_1 = False
        self.pole_2 = False

        while self.running:
            # считывание выбранного режима (1 или 2 игрока)
            if self.level1_button.is_clicked():
                self.pole_1 = True
                self.opponent.add(self.all_sprites, self.paddle_sprites)
            if self.level2_button.is_clicked():
                self.pole_2 = True
                self.player2.add(self.all_sprites, self.paddle_sprites)

            if (not self.pole_1) and (not self.pole_2):
                display_surface.fill('white')
                self.bg = pygame.image.load('extra/start_bg.jpg')
                self.bg = pygame.transform.scale(self.bg, (window_width, window_height))
                display_surface.blit(self.bg, (0, 0))
                display_surface.blit(self.surf, (0, 0))

                self.level1_button.draw()
                self.level2_button.draw()
                text_surface = font.render(f'Выберите режим игры:', True, (255, 99, 219))
                text_rect = text_surface.get_rect(center=(window_width // 2, window_height // 2 - 170))
                display_surface.blit(text_surface, text_rect)

            pygame.display.flip()

            if self.gameplay:

                dt = clock.tick(FPS) / 1000
                for event in pygame.event.get():
                    # закрытие главного окна
                    if event.type == pygame.QUIT:
                        self.running = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            paused = not paused

                if self.score['opponent'] >= 7 or self.score['player'] >= 7:
                    self.gameplay = False
                    self.player2.kill()
                    self.opponent.kill()

                if self.pole_1 or self.pole_2:
                    # остановка игры на паузу, если нажата клавиша SPACE
                    if paused == False:
                        display_surface.blit(pause_text, (
                            window_width // 2 - pause_text.get_width() // 2,
                            window_height // 2 - pause_text.get_height() // 2))
                        display_surface.set_alpha(200)
                    else:
                        # запуск грыпп спрайтов
                        self.all_sprites.update(dt)
                        display_surface.fill(colors['bg'])
                        display_surface.blit(self.bg_wallpaper, (0, 0))
                        self.display_score()
                        self.all_sprites.draw(display_surface)
            else:
                display_surface.blit(self.bg, (0, 0))
                display_surface.blit(self.surf, (0, 0))
                # конец игры, если 1 из игроков пропустил мяч >= 7 раз
                if self.score['opponent'] > self.score['player']:
                    if self.pole_1:
                        display_surface.blit(self.text_lose, (window_width / 2 - 110, window_height / 2 - 80))
                    else:
                        display_surface.blit(self.text_player_left, (window_width / 2 - 175, window_height / 2 - 80))

                else:
                    if self.pole_1:
                        display_surface.blit(self.text_win, (window_width / 2 - 110, window_height / 2 - 80))
                    elif self.pole_2:
                        display_surface.blit(self.text_player_right, (window_width / 2 - 190, window_height / 2 - 80))

                display_surface.blit(self.text_restart, self.rect_restart)

                mouse = pygame.mouse.get_pos()
                # запуск игры в выбранном режиме заново, при нажатии на текст "начать заново"
                if self.rect_restart.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    self.gameplay = True
                    self.score['opponent'] = 0
                    self.score['player'] = 0
                    self.player.rect = pygame.Rect(0, 0, *sizes['paddle'])
                    self.player.rect.center = position['player']
                    if self.pole_1:
                        self.opponent.add(self.all_sprites, self.paddle_sprites)
                        self.opponent.rect = pygame.Rect(0, 0, *sizes['paddle'])
                        self.opponent.rect.center = position['opponent']
                    if self.pole_2:
                        self.player2.add(self.all_sprites, self.paddle_sprites)
                        self.player2.rect = pygame.Rect(0, 0, *sizes['paddle'])
                        self.player2.rect.center = position['opponent']
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

            pygame.display.update()
            pygame.display.flip()
        pygame.quit()


# главный класс платформ
class Paddle(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.image = pygame.Surface(sizes['paddle'], pygame.SRCALPHA)
        pygame.draw.rect(self.image, colors['paddle'], pygame.Rect((0, 0), sizes['paddle']), 0, 4)

        pd_image = pygame.image.load('extra/paddle_bg.jpg')
        pd_image = pygame.transform.scale(pd_image, sizes['paddle'])
        self.image.blit(pd_image, (0, 0))

        self.rect = self.image.get_rect(center=position['player'])
        self.old_rect = self.rect.copy()
        self.direction = [0, 0]
        self.speed = speed['player']

    # движение платформ, столкновение со стенками окна
    def move(self, dt):
        self.rect.centery += self.direction[1] * self.speed * dt
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > window_height:
            self.rect.bottom = window_height

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.get_direction()
        self.move(dt)


# класс правого игрока (движение клавишами K_DOWN и K_UP)
class Player(Paddle):
    def __init__(self, groups):
        super().__init__(groups)
        self.speed = speed['player']
        self.side = 1

    # движение правой платформы в зависимости от нажатой кнопки
    def get_direction(self):
        keys = pygame.key.get_pressed()
        self.direction[1] = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])


# класс левого игрока (движение клавишами K_z и K_a) при режиме "1 игрок"
class Player2(Paddle):
    def __init__(self, groups):
        super().__init__(groups)
        self.speed = speed['player']
        self.rect.center = position['opponent']
        self.side = 2

    # движение левой платформы в зависимости от нажатой кнопки
    def get_direction(self):
        keys = pygame.key.get_pressed()
        self.direction[1] = int(keys[pygame.K_z]) - int(keys[pygame.K_a])


# класс левой платформы-противника (при режиме "1 игрок")
class Opponent(Paddle):
    def __init__(self, groups, ball):
        super().__init__(groups)
        self.speed = speed['opponent']
        self.rect.center = position['opponent']
        self.ball = ball
        self.side = 2

    # движение вверх/вниз в зависимости от координат центра мячика
    def get_direction(self):
        if self.ball.rect.centery > self.rect.centery:
            self.direction[1] = 1
        else:
            self.direction[1] = -1


# класс кнопок для выбора режима
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color

    # отрисовка кнопок
    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(display_surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(display_surface, self.color, self.rect)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, 'white')
        text_rect = text_surface.get_rect(center=self.rect.center)
        display_surface.blit(text_surface, text_rect)

    # проверка, какая кнопка нажата
    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse_pos) and mouse_click[0]:
            return True
        return False


# класс мяча
class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, paddle_sprites, update_score, star):
        super().__init__(groups)
        self.paddle_sprites = paddle_sprites
        self.update_score = update_score
        self.star = star
        self.score_star_left = 0
        self.score_star_right = 0
        self.last_pud = 0

        self.collision_sound2 = pygame.mixer.Sound('extra/bonus_sound.mp3')
        self.collision_sound2.set_volume(100.0)

        self.image = pygame.Surface(sizes['ball'], pygame.SRCALPHA)
        pygame.draw.circle(self.image, colors['ball'], (sizes['ball'][0] / 2, sizes['ball'][1] / 2),
                           sizes['ball'][0] / 2)

        self.image = pygame.image.load('extra/donut.png')
        self.image = pygame.transform.scale(self.image, sizes['ball'])

        self.rect = self.image.get_rect(center=(window_width / 2, window_height / 2))
        self.mask = pygame.mask.from_surface(self.image)
        self.old_rect = self.rect.copy()
        self.direction = [choice((1, -1)), uniform(0.7, 0.8) * choice((-1, 1))]

        self.collision_sound = pygame.mixer.Sound('extra/collision_ball_sound.mp3')
        self.collision_sound.set_volume(100.0)

    # изменение движения мяча
    def move(self, dt):
        self.rect.x += self.direction[0] * speed['ball'] * dt
        self.collision('horizontal')
        self.rect.y += self.direction[1] * speed['ball'] * dt
        self.collision('vertical')

    # столкновение мяча с платформами
    def collision(self, direction):
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect):
                self.side = sprite.side
                # проигрывание звука при столкновении с платформой
                self.collision_sound.play(0, 0, 1000)
                # изменение направления движения при столкновении с платформой
                if direction == 'horizontal':
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.direction[0] *= -1
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.direction[0] *= -1
                else:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction[1] *= -1
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.direction[1] *= -1

    # столкновение мяча со стеной
    def wall_collision(self):
        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction[1] *= -1

        if self.rect.bottom >= window_height:
            self.rect.bottom = window_height
            self.direction[1] *= -1
        # изменение очков выигравшего игрока, при пропуске мяча
        if self.rect.right >= window_width or self.rect.left <= 0:
            if self.rect.x < window_width / 2:
                self.update_score('player')
            else:
                self.update_score('opponent')
            self.rect.center = (window_width / 2, window_height / 2)
            self.direction = [choice((1, -1)), uniform(0.7, 0.8) * choice((-1, 1))]

    # создание бонуса - звездочки, изменение баллов игроков
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.move(dt)
        self.wall_collision()
        if self.rect.colliderect(self.star.rect):
            self.star.rect = pygame.Rect(randint(20, window_width - 40), randint(20, window_height - 40), 40, 40)

            if self.side == 1:
                self.score_star_right += 25
                results['Игрок с правой стороны:'] += 25

            elif self.side == 2:
                self.score_star_left += 25
                results['Игрок с левой стороны:'] += 25
            # проигрывание звука при взятии бонуса
            self.collision_sound2.play(0, 0, 1000)


# класс звездочки (бонуса)
class Star(pygame.sprite.Sprite):
    def __init__(self, groups):
        from random import randint

        super().__init__(groups)

        self.size = 10
        self.rect = pygame.Rect(randint(50, window_width - 90), randint(50, window_height - 90), 40, 40)
        self.x = randint(self.size, window_width - self.size)
        self.y = randint(self.size, window_height - self.size)
        self.image = pygame.image.load('extra/star.png')
        self.image = pygame.transform.scale(self.image, (40, 40))

    # отрисовка бонуса
    def draw(self):
        pygame.draw.polygon(display_surface, 'yellow', [
            (self.x, self.y - self.size),
            (self.x - self.size, self.y + self.size),
            (self.x + self.size, self.y + self.size)
        ])


if __name__ == '__main__':
    game = Game()
    game.run()
# занесение результатов в текстовый файл
result1 = results['Игрок с правой стороны:']
result2 = results['Игрок с левой стороны:']
file.write(f'Баллы игрока с правой стороны: {result1}' + '\n' + f'Баллы игрока с левой стороны: {result2}')
file.close()
