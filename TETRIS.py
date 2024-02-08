import pygame
import os
import sys
import random
import time


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def points_render():  # отображение очков
    font = pygame.font.Font(None, 60)
    string_rendered = font.render(points_text, True, pygame.Color('yellow'))
    screen.blit(string_rendered, (857, 10))
    string_rendered = font.render(str(points), True, pygame.Color('yellow'))
    screen.blit(string_rendered, (857, 60))


def start_screen():  # отображение экрана при запуске
    intro_text = "Нажмите пробел, чтобы начать"

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    string_rendered = font.render(intro_text, 1, pygame.Color('white'))
    screen.blit(string_rendered, (260, 450))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        pygame.display.flip()
        clock.tick(FPS)


class Tetromino():

    def __init__(self):
        self.tetromino_active = list()  # доп. список, используется для перемещения вниз
        self.tetro_tiles = [[0] * 17 for _ in range(11)]  # игровое поле
        self.rot = 0  # поворот тетромино (от 0 до 3)
        self.tetromino_type = int  # тип тетромино. Бужет генерироваться рандомн

    def tetromino_spawn(self):  # появление нового тетромино
        lose_check()
        self.tetromino_type = random.randint(0, 4)  # рандомная генерация вида тетромино
        self.rot = 0  # т.к. тетрмино новое, то поворот = 0
        if self.tetromino_type == 0:  # длинная палка
            self.tetro_tiles[0][8] = 1
            self.tetro_tiles[1][8] = 1
            self.tetro_tiles[2][8] = 1
            self.tetro_tiles[3][8] = 1
        elif self.tetromino_type == 1:  # палка загнутая
            self.tetro_tiles[0][8] = 1
            self.tetro_tiles[1][8] = 1
            self.tetro_tiles[2][8] = 1
            self.tetro_tiles[2][7] = 1
        elif self.tetromino_type == 2:  # молния
            self.tetro_tiles[0][8] = 1
            self.tetro_tiles[1][8] = 1
            self.tetro_tiles[1][9] = 1
            self.tetro_tiles[2][9] = 1

        elif self.tetromino_type == 3:  # буква Т
            self.tetro_tiles[0][8] = 1
            self.tetro_tiles[1][8] = 1
            self.tetro_tiles[2][8] = 1
            self.tetro_tiles[1][9] = 1
        elif self.tetromino_type == 4:  # кубик
            self.tetro_tiles[0][8] = 1
            self.tetro_tiles[1][8] = 1
            self.tetro_tiles[0][9] = 1
            self.tetro_tiles[1][9] = 1

    def rotation(self):  # поворот тетромино
        if self.tetromino_type == 0:  # для кадого вида тетро свой метод поворота
            self.rotation_0()  # вращение тетромино с кодом генерации 0 (прямая палка)
        elif self.tetromino_type == 1:
            self.rotation_1()  # вращение тетромино с кодом генерации 1 (загнутая палка)
        elif self.tetromino_type == 2:
            self.rotation_2()  # вращение тетромино с кодом генерации 2 (молния)
        elif self.tetromino_type == 3:
            self.rotation_3()  # вращение тетромино с кодом генерации 3 (буква Т)

    def rotation_0(self):  # вращение однго из видов тетрамино(число - номер генерации из tetromino_spawn)
        a = 0
        tiles = list()
        for i in range(len(self.tetro_tiles)):
            for j in range(len(self.tetro_tiles[i])):
                if self.tetro_tiles[i][j] == 1 and self.rot % 2 == 0 and 0 < j < 15 and i > 0:
                    a += 1
                    tiles.append((i, j))
                if self.tetro_tiles[i][j] == 1 and self.rot % 2 == 1 and i < 10:
                    a += 1
                    tiles.append((i, j))
        if a > 3:
            if self.rot % 2 == 0:
                if self.tetro_tiles[tiles[0][0] + 2][tiles[0][1] + 2] == 0 and \
                        self.tetro_tiles[tiles[1][0] + 1][tiles[1][1] + 1] == 0 and \
                        self.tetro_tiles[tiles[3][0] - 1][tiles[3][1] - 1] == 0:
                    self.tetro_tiles[tiles[0][0]][tiles[0][1]] = 0
                    self.tetro_tiles[tiles[0][0] + 2][tiles[0][1] + 2] = 1

                    self.tetro_tiles[tiles[1][0]][tiles[1][1]] = 0
                    self.tetro_tiles[tiles[1][0] + 1][tiles[1][1] + 1] = 1

                    self.tetro_tiles[tiles[3][0]][tiles[3][1]] = 0
                    self.tetro_tiles[tiles[3][0] - 1][tiles[3][1] - 1] = 1
            else:
                if self.tetro_tiles[tiles[0][0] + 1][tiles[0][1] + 1] == 0 and \
                        self.tetro_tiles[tiles[2][0] - 1][tiles[2][1] - 1] == 0 and \
                        self.tetro_tiles[tiles[3][0] - 2][tiles[3][1] - 2] == 0:
                    self.tetro_tiles[tiles[0][0]][tiles[0][1]] = 0
                    self.tetro_tiles[tiles[0][0] + 1][tiles[0][1] + 1] = 1

                    self.tetro_tiles[tiles[2][0]][tiles[2][1]] = 0
                    self.tetro_tiles[tiles[2][0] - 1][tiles[2][1] - 1] = 1

                    self.tetro_tiles[tiles[3][0]][tiles[3][1]] = 0
                    self.tetro_tiles[tiles[3][0] - 2][tiles[3][1] - 2] = 1

            self.rot += 1
            self.rot %= 4

    def rotation_1(self):  # вращение тетрамино(число - номер генерации из tetromino_spawn) - загнутая палка
        a = 0
        tiles = list()
        for i in range(len(self.tetro_tiles)):
            for j in range(len(self.tetro_tiles[i])):
                if self.tetro_tiles[i][j] == 1 and self.rot == 0 and j < 16:
                    a += 1
                    tiles.append((i, j))
                if self.tetro_tiles[i][j] == 1 and self.rot == 1 and i < 10:
                    a += 1
                    tiles.append((i, j))
                if self.tetro_tiles[i][j] == 1 and self.rot == 2 and j > 0:
                    a += 1
                    tiles.append((i, j))
                if self.tetro_tiles[i][j] == 1 and self.rot == 3:
                    a += 1
                    tiles.append((i, j))
        if a > 3:
            if self.rot == 0:
                if self.tetro_tiles[tiles[0][0] + 1][tiles[0][1] + 1] == 0 and \
                        self.tetro_tiles[tiles[3][0] - 1][tiles[3][1] - 1] == 0 and \
                        self.tetro_tiles[tiles[2][0] - 2][tiles[2][1]] == 0:
                    self.tetro_tiles[tiles[0][0]][tiles[0][1]] = 0
                    self.tetro_tiles[tiles[0][0] + 1][tiles[0][1] + 1] = 1

                    self.tetro_tiles[tiles[3][0]][tiles[3][1]] = 0
                    self.tetro_tiles[tiles[3][0] - 1][tiles[3][1] - 1] = 1

                    self.tetro_tiles[tiles[2][0]][tiles[2][1]] = 0
                    self.tetro_tiles[tiles[2][0] - 2][tiles[2][1]] = 1

            elif self.rot == 1:
                if self.tetro_tiles[tiles[0][0]][tiles[0][1] + 2] == 0 and \
                        self.tetro_tiles[tiles[1][0] - 1][tiles[1][1] + 1] == 0 and \
                        self.tetro_tiles[tiles[3][0] + 1][tiles[3][1] - 1] == 0:
                    self.tetro_tiles[tiles[0][0]][tiles[0][1]] = 0
                    self.tetro_tiles[tiles[0][0]][tiles[0][1] + 2] = 1

                    self.tetro_tiles[tiles[1][0]][tiles[1][1]] = 0
                    self.tetro_tiles[tiles[1][0] - 1][tiles[1][1] + 1] = 1

                    self.tetro_tiles[tiles[3][0]][tiles[3][1]] = 0
                    self.tetro_tiles[tiles[3][0] + 1][tiles[3][1] - 1] = 1

            elif self.rot == 2:
                if self.tetro_tiles[tiles[0][0] + 1][tiles[0][1] + 1] == 0 and \
                        self.tetro_tiles[tiles[1][0] + 2][tiles[1][1]] == 0 and \
                        self.tetro_tiles[tiles[3][0] - 1][tiles[3][1] - 1] == 0:
                    self.tetro_tiles[tiles[0][0]][tiles[0][1]] = 0
                    self.tetro_tiles[tiles[0][0] + 1][tiles[0][1] + 1] = 1

                    self.tetro_tiles[tiles[1][0]][tiles[1][1]] = 0
                    self.tetro_tiles[tiles[1][0] + 2][tiles[1][1]] = 1

                    self.tetro_tiles[tiles[3][0]][tiles[3][1]] = 0
                    self.tetro_tiles[tiles[3][0] - 1][tiles[3][1] - 1] = 1

            elif self.rot == 3:
                if self.tetro_tiles[tiles[0][0] - 1][tiles[0][1] + 1] == 0 and \
                        self.tetro_tiles[tiles[2][0] + 1][tiles[2][1] - 1] == 0 and \
                        self.tetro_tiles[tiles[3][0]][tiles[3][1] - 2] == 0:
                    self.tetro_tiles[tiles[0][0]][tiles[0][1]] = 0
                    self.tetro_tiles[tiles[0][0] - 1][tiles[0][1] + 1] = 1

                    self.tetro_tiles[tiles[2][0]][tiles[2][1]] = 0
                    self.tetro_tiles[tiles[2][0] + 1][tiles[2][1] - 1] = 1

                    self.tetro_tiles[tiles[3][0]][tiles[3][1]] = 0
                    self.tetro_tiles[tiles[3][0]][tiles[3][1] - 2] = 1
            self.rot += 1
            self.rot %= 4

    def rotation_2(self):  # вращение однго из видов тетрамино(число - номер генерации из tetromino_spawn)
        a = 0
        tiles = list()
        for i in range(len(self.tetro_tiles)):
            for j in range(len(self.tetro_tiles[i])):
                if self.tetro_tiles[i][j] == 1 and self.rot == 0 and j > 0:
                    a += 1
                    tiles.append((i, j))
                if self.tetro_tiles[i][j] == 1 and self.rot == 1 and i < 16:
                    a += 1
                    tiles.append((i, j))
                if self.tetro_tiles[i][j] == 1 and self.rot == 2:
                    a += 1
                    tiles.append((i, j))
                if self.tetro_tiles[i][j] == 1 and self.rot == 3:
                    a += 1
                    tiles.append((i, j))
        if a > 3:
            if self.rot == 0:
                if self.tetro_tiles[tiles[2][0] + 1][tiles[2][1] - 1] == 0 and \
                        self.tetro_tiles[tiles[3][0]][tiles[3][1] - 2] == 0:
                    self.tetro_tiles[tiles[2][0]][tiles[2][1]] = 0
                    self.tetro_tiles[tiles[2][0] + 1][tiles[2][1] - 1] = 1

                    self.tetro_tiles[tiles[0][0]][tiles[0][1]] = 0
                    self.tetro_tiles[tiles[0][0] + 1][tiles[0][1] + 1] = 1

                    self.tetro_tiles[tiles[3][0]][tiles[3][1]] = 0
                    self.tetro_tiles[tiles[3][0]][tiles[3][1] - 2] = 1
            elif self.rot == 1:
                if self.tetro_tiles[tiles[2][0] - 2][tiles[2][1]] == 0 and \
                        self.tetro_tiles[tiles[3][0] - 1][tiles[3][1] - 1] == 0:
                    self.tetro_tiles[tiles[2][0]][tiles[2][1]] = 0
                    self.tetro_tiles[tiles[2][0] - 2][tiles[2][1]] = 1

                    self.tetro_tiles[tiles[3][0]][tiles[3][1]] = 0
                    self.tetro_tiles[tiles[3][0] - 1][tiles[3][1] - 1] = 1

                    self.tetro_tiles[tiles[1][0]][tiles[1][1]] = 0
                    self.tetro_tiles[tiles[1][0] + 1][tiles[1][1] - 1] = 1

            elif self.rot == 2:
                if self.tetro_tiles[tiles[1][0] - 1][tiles[1][1] + 1] == 0 and \
                        self.tetro_tiles[tiles[0][0]][tiles[0][1] + 2] == 0:
                    self.tetro_tiles[tiles[1][0]][tiles[1][1]] = 0
                    self.tetro_tiles[tiles[1][0] - 1][tiles[1][1] + 1] = 1

                    self.tetro_tiles[tiles[0][0]][tiles[0][1]] = 0
                    self.tetro_tiles[tiles[0][0]][tiles[0][1] + 2] = 1

                    self.tetro_tiles[tiles[3][0]][tiles[3][1]] = 0
                    self.tetro_tiles[tiles[3][0] - 1][tiles[3][1] - 1] = 1

            elif self.rot == 3:
                if self.tetro_tiles[tiles[1][0] + 2][tiles[1][1]] == 0 and \
                        self.tetro_tiles[tiles[0][0] + 1][tiles[0][1] + 1] == 0:
                    self.tetro_tiles[tiles[1][0]][tiles[1][1]] = 0
                    self.tetro_tiles[tiles[1][0] + 2][tiles[1][1]] = 1

                    self.tetro_tiles[tiles[0][0]][tiles[0][1]] = 0
                    self.tetro_tiles[tiles[0][0] + 1][tiles[0][1] + 1] = 1

                    self.tetro_tiles[tiles[2][0]][tiles[2][1]] = 0
                    self.tetro_tiles[tiles[2][0] - 1][tiles[2][1] + 1] = 1
            self.rot += 1
            self.rot %= 4

    def rotation_3(self):  # вращение однго из видов тетрамино(число - номер генерации из tetromino_spawn)
        a = 0
        tiles = list()
        for i in range(len(self.tetro_tiles)):
            for j in range(len(self.tetro_tiles[i])):
                if self.tetro_tiles[i][j] == 1 and self.rot == 0 and j > 0:
                    a += 1
                    tiles.append((i, j))
                if self.tetro_tiles[i][j] == 1 and self.rot == 1:
                    a += 1
                    tiles.append((i, j))
                if self.tetro_tiles[i][j] == 1 and self.rot == 2 and j < 16:
                    a += 1
                    tiles.append((i, j))
                if self.tetro_tiles[i][j] == 1 and self.rot == 3 and i < 10:
                    a += 1
                    tiles.append((i, j))
        if a > 3:
            if self.rot == 0:
                if self.tetro_tiles[tiles[0][0] + 1][tiles[0][1] - 1] == 0:
                    self.tetro_tiles[tiles[0][0]][tiles[0][1]] = 0
                    self.tetro_tiles[tiles[0][0] + 1][tiles[0][1] - 1] = 1
            elif self.rot == 1:
                if self.tetro_tiles[tiles[2][0] - 1][tiles[2][1] - 1] == 0:
                    self.tetro_tiles[tiles[2][0]][tiles[2][1]] = 0
                    self.tetro_tiles[tiles[2][0] - 1][tiles[2][1] - 1] = 1
            elif self.rot == 2:
                if self.tetro_tiles[tiles[3][0] - 1][tiles[3][1] + 1] == 0:
                    self.tetro_tiles[tiles[3][0]][tiles[3][1]] = 0
                    self.tetro_tiles[tiles[3][0] - 1][tiles[3][1] + 1] = 1
            elif self.rot == 3:
                if self.tetro_tiles[tiles[1][0] + 1][tiles[1][1] + 1] == 0:
                    self.tetro_tiles[tiles[1][0]][tiles[1][1]] = 0
                    self.tetro_tiles[tiles[1][0] + 1][tiles[1][1] + 1] = 1
            self.rot += 1
            self.rot %= 4

    def tetro_render(self):  # рэндер активного тетромино
        for i in range(len(self.tetro_tiles)):
            for j in range(len(self.tetro_tiles[i])):
                if self.tetro_tiles[i][j] == 1:
                    pygame.draw.rect(screen, pygame.Color("blue"), (j * 50, i * 50, 50, 50), 0)

    def gravity(self):  # смещение активного тетромино вниз
        global tetromino_spawn
        can_fall = 0  # сколько клеток активного тетромино могут сместиться вниз. Если все - то тетромино смещается
        tiles_transform = list()
        self.tetromino_active = list()
        for i in range(len(self.tetro_tiles) - 2, -1, -1):
            for j in range(len(self.tetro_tiles[i]) - 1, -1, -1):
                if self.tetro_tiles[i + 1][j] != 5 and self.tetro_tiles[i][j] == 1:
                    # если клетка не в самом низу и под ней нет препятствия - она может упасть
                    can_fall += 1
                    tiles_transform.append((i, j))  # создается список для передаче в Board,
                    # чтобы игровое поле в классе Board тоже изменилось
        if can_fall == 4:  # если все клетки тетрамино могут сместиться вниз - смещается
            for i in tiles_transform:
                self.tetro_tiles[i[0]][i[1]] = 0
                self.tetro_tiles[i[0] + 1][i[1]] = 1
        else:  # иначе тетрамино считается упавшим, нужно, чтобы появилось новое
            tetromino_spawn = True
            return self.tetromino_change()  # значение передастся в класс Board, чтобы затем отрендерится.
            # Что это объясняется в следующем методе
        return 0

    def tetromino_change(self):  # тетрамино делается неактивным (чтобы его нельзя было двигать, вращать и т.д.)
        global points
        for i in range(len(self.tetro_tiles) - 1, -1, -1):
            for j in range(len(self.tetro_tiles[i]) - 1, -1, -1):
                if self.tetro_tiles[i][j] == 1:  # 1 - клетка активного тетромино
                    self.tetromino_active.append((i, j))
                    self.tetro_tiles[i][j] = 5
        points += 10
        return self.tetromino_active  # значение передастся в класс Board, чтобы затем отрендерится.

    def full_line_check(self):  # чек, заполнена ли какая-либо линия полностью
        global points
        disappeared_rows = list()
        for i in range(1, len(self.tetro_tiles)):
            if 0 not in self.tetro_tiles[i]:  # если нашлась линия в которой неn свободного пространства
                points += 100
                disappeared_rows.append(i)
        return disappeared_rows

    def line_disappear(self, rows):  # линии над исчезнувшей должны "упасть" на место исчезнувшей линии
        for disappeared_row in rows:
            for i in range(disappeared_row - 1, 0, -1):
                self.tetro_tiles[i + 1] = self.tetro_tiles[i].copy()

    def move(self, move_side):  # движение влево - вправо
        tile_can_move = 0
        if move_side == 1:  # Если движение вправ
            for i in range(len(self.tetro_tiles) - 1, -1, -1):
                for j in range(len(self.tetro_tiles[i]) - 2, -1, -1):
                    if self.tetro_tiles[i][j + move_side] != 5 and self.tetro_tiles[i][j] == 1:
                        tile_can_move += 1
            if tile_can_move > 3:
                for i in range(len(self.tetro_tiles) - 1, -1, -1):
                    for j in range(len(self.tetro_tiles[i]) - 1, -1, -1):
                        if self.tetro_tiles[i][j] == 1:
                            self.tetro_tiles[i][j] = 0
                            self.tetro_tiles[i][j + move_side] = -1
        else:
            for i in range(len(self.tetro_tiles) - 1, -1, -1):
                for j in range(len(self.tetro_tiles[i]) - 1, 0, -1):
                    if self.tetro_tiles[i][j + move_side] != 5 and self.tetro_tiles[i][j] == 1:
                        tile_can_move += 1
            if tile_can_move > 3:
                for i in range(len(self.tetro_tiles)):
                    for j in range(len(self.tetro_tiles[i])):
                        if self.tetro_tiles[i][j] == 1:
                            self.tetro_tiles[i][j] = 0
                            self.tetro_tiles[i][j + move_side] = -1
        for i in range(len(self.tetro_tiles) - 1, -1, -1):
            for j in range(len(self.tetro_tiles[i]) - 1, -1, -1):
                if self.tetro_tiles[i][j] == -1:
                    self.tetro_tiles[i][j] = 1


class Board:
    # создание поля
    def __init__(self):
        self.board = [[0] * 17 for _ in range(11)]

    def full_tile_add(self, tiles):
        for i in tiles:
            self.board[i[0]][i[1]] = 1

    def line_dissapear(self, rows):  # тоже падение линий вниз, но уже в этом классе для рэндера
        for disappeared_row in rows:
            for i in range(disappeared_row - 1, 0, -1):
                self.board[i + 1] = self.board[i].copy()

    def tile_render(self, screen):  # рэндер всего, кроме падающего тетромино
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:  # если пустое поле
                    pygame.draw.rect(screen, pygame.Color("black"), (j * 50, i * 50, 50, 50), 1)
                elif self.board[i][j] == 1:  # если поле занято
                    pygame.draw.rect(screen, pygame.Color("blue"), (j * 50, i * 50, 50, 50), 0)
                    pygame.draw.rect(screen, pygame.Color("black"), (j * 50, i * 50, 50, 50), 1)


def lose_check():  # при проигрыше сброс всех переменных
    global game_tiles, tetro_tiles, time1
    if 5 in tetr.tetro_tiles[0]:
        start_screen()
        tetr.tetro_tiles = [[0] * 17 for _ in range(11)]
        time1 = time.time()
        points = 0


def screen_update():
    screen.fill((50, 50, 50))
    tetr.tetro_render()
    board.tile_render(screen)
    points_render()


pygame.init()
tetromino_spawn = True
size = width, height = 1024, 550
screen = pygame.display.set_mode(size)
FPS = 30
points = 0
points_text = "POINTS"
clock = pygame.time.Clock()

time1 = time.time()  # повторять после проигрыша
board = Board()
tetr = Tetromino()

spawn_speed = 0.35
speed_count = 1
start_screen()
manual_fall = False
while True:
    screen_update()
    if points >= speed_count * 500:
        spawn_speed *= 0.8
        speed_count += 1
    if tetromino_spawn:
        tetromino_spawn = False  # исчезновение (и вообще его чек) происходит перед спавном тетрамино нового
        disapp_rows = tetr.full_line_check()
        if len(disapp_rows) > 0:
            tetr.line_disappear(disapp_rows)
            board.line_dissapear(disapp_rows)
        tetr.tetromino_spawn()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                tetr.move(-1)
            elif event.key == pygame.K_RIGHT:
                tetr.move(1)
            elif event.key == pygame.K_SPACE:
                tetr.rotation()
            elif event.key == pygame.K_DOWN:
                manual_fall = True

    if time.time() - time1 >= spawn_speed or manual_fall:  # тетромино падает каждые spawn_speed секунд
        manual_fall = False
        time1 = time.time()
        tetro_change = tetr.gravity()
        if tetro_change != 0:
            board.full_tile_add(tetro_change)
    lose_check()
    clock.tick(FPS)
    pygame.display.flip()
