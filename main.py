from random import randint
import pygame
from math import cos, sin, pi
pygame.init()
pygame.font.init()
# импорт всего необходимого

myfont = pygame.font.SysFont('Comic Sans MS', 60)
# шрифт

running = True
size = width, height = 1500, 500 + 173
count_blocks = 50

block_width = width // count_blocks

screen = pygame.display.set_mode(size)
screen2 = pygame.Surface(screen.get_size())
screen2.fill((255, 255, 255))
# инициализация дисплея

clock = pygame.time.Clock()


# класс кнопки
class Button:
    def __init__(self, y, x, images):
        self.y = y
        self.x = x
        self.images = images
        self.first_image = True

    def click(self, x, y):
        # проверка на попадание по кнопке
        if self.x <= x <= self.rect[2] + self.x and self.y <= y <= self.rect[3] + self.y:
            return True
        return False


# класс ветки
class Branch:
    def __init__(self, length, angle, age, branchs):
        self.length = length
        self.angle = angle
        self.age = age
        self.branches = branchs
        # каждая ветка содержит последующие


# рекурсивная футкция роста дерева
def branch_growth(branch, tree_age):
    if type(branch) == Apple:
        return

    if randint(0, tree_age ** 2) < 200:# чем старше дерево тем оно медленнее растет
        if branch.age > 1 and randint(0, branch.age ** 2) < 8 and randint(0, len(branch.branches) ** 2) < 2\
                and randint(0, 1) > -1:
            branch.branches.append(Branch(2.5, branch.angle + randint(-35, 35), 1, []))
        if randint(0, branch.age) < 10:
            branch.length += 2.5
        if randint(0, branch.age) < 4:
            branch.age += 1
        for b in branch.branches:
            branch_growth(b, tree_age)


# рекурсивная функция отрисовки дерева
def tree_draw(last_branch_x, last_branch_y, branch, tree):
    if type(branch) == Apple:
        apple_draw(last_branch_x, last_branch_y, branch.age)
    else:
        new_cords = [last_branch_x + branch.length * cos(branch.angle / 180 * pi),
                     last_branch_y + branch.length * sin(branch.angle / 180 * pi)]
        if branch.age > 2:
            pygame.draw.line(screen2, (138, 83, 0), [last_branch_x, last_branch_y],
                             new_cords, branch.age)
        else:
            pygame.draw.line(screen2, (119, 230, 64), [last_branch_x, last_branch_y],
                             [last_branch_x - (last_branch_x - new_cords[0]) + (last_branch_x - new_cords[0]) * 3,
                              last_branch_y - (last_branch_y - new_cords[1]) + (last_branch_y - new_cords[1]) * 3], 10)
        for b in branch.branches:
            tree_draw(*new_cords, b, tree)


# функция отрисовки аблока
def apple_draw(x, y, age):
    global red_apples, bad_apples
    if age < 10:# цвет яблока меняется от его возраста
        color = (173, 249, 22)
        bad_apples.append([x, y])
    elif age < 13:
        color = (247, 68, 23)
        red_apples.append([x, y])
    else:
        color = (178, 150, 85)
        bad_apples.append([x, y])
    pygame.draw.circle(screen2, color, [x, y], 8)


# рекурсивная функция роста яблок
def apples_growth(last_branch_x, last_branch_y, branch, tree):
    if type(branch) == Apple:
        branch.age += 1
        return
    new_x = last_branch_x + branch.length * cos(branch.angle / 180 * pi)
    new_y = last_branch_y + branch.length * sin(branch.angle / 180 * pi)
    for i in range(len(branch.branches) - 1, -1, -1):
        if type(branch.branches[i]) == Apple:
            if branch.branches[i].age > 13:
                falling_apples.append(FallingApple(new_x, new_y,
                                                   new_x + randint(-230, 230), tree.y + randint(-15, 15),
                                                   branch.branches[i].age))
                del branch.branches[i]
    if randint(0, 10) * tree.age > 100 and randint(0, 1000) == 0:
        branch.branches.append(Apple())
    for b in branch.branches:
        apples_growth(new_x, new_y, b, tree)


# рекурсивная функция просчета заполнения "блоков энергии" деревом
def energy_generation(last_x, last_y, branch, tree):
    if type(branch) == Apple:
        return
    new_x = last_x + branch.length * cos(branch.angle / 180 * pi)
    new_y = last_y + branch.length * sin(branch.angle / 180 * pi)
    block_index = int(new_x) // block_width
    if not (0 < block_index < count_blocks):
        return
    if branch.age <= 2:
        if lights_blocks[block_index].tree != tree:
            if lights_blocks[block_index].max_height > new_y:
                lights_blocks[block_index].max_height = new_y
                lights_blocks[block_index].tree = tree
        if tree not in dirts_blocks[block_index].trees:
            dirts_blocks[block_index].trees.append(tree)

    for b in branch.branches:
        energy_generation(new_x, new_y, b, tree)


# функция упавших яблок
def fallen_apples_function():
    for i in range(len(fallen_apples) - 1, -1, -1):
        fallen_apples[i].age += 1
        if fallen_apples[i].age > 20:
            if randint(0, 20) == 0:
                if 0 < fallen_apples[i].x < width and 0 < fallen_apples[i].y < height:
                    create_tree(fallen_apples[i].x, fallen_apples[i].y)
            del fallen_apples[i]
            continue
        apple_draw(fallen_apples[i].x, fallen_apples[i].y, fallen_apples[i].age)


# функция отрисовки упавших яблок
def fallen_apples_draw():
    for i in range(len(fallen_apples)):
        apple_draw(fallen_apples[i].x, fallen_apples[i].y, fallen_apples[i].age)


# функция ПАДАНИЯ яблок
def falling_apples_function(draw=True):
    for i in range(len(falling_apples) - 1, -1, -1):
        falling_apples[i].fall()
        if draw:
            falling_apples[i].draw()
        if falling_apples[i].y_progress >= 1:
            fallen_apples.append(Apple(falling_apples[i].to_x, falling_apples[i].to_y))
            fallen_apples[-1].age = falling_apples[i].age
            del falling_apples[i]


# класс яблока
class Apple:
    def __init__(self, x=None, y=None):
        self.age = 1
        self.x = x
        self.y = y


# класс упавшего яблока
class FallingApple:
    def __init__(self, from_x, from_y, to_x, to_y, age):
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        self.age = age
        self.x_progress = 0
        self.y_progress = 0

    # функция пошагового падания яблока
    def fall(self):
        if self.x_progress >= 1:
            self.y_progress += 0.1
        else:
            self.x_progress += 0.2
            self.y_progress += 0.02

    # функция рисования падающего яблока
    def draw(self):
        x = self.from_x - (self.from_x - self.to_x) * self.y_progress
        y = self.from_y - (self.from_y - self.to_y) * self.x_progress
        if self.to_x > self.from_x:
            x = min((x, self.to_x))
        if self.to_y > self.from_y:
            y = min((y, self.to_y))
        if self.to_x < self.from_x:
            x = max((x, self.to_x))
        if self.to_y < self.from_y:
            y = max((y, self.to_y))
        apple_draw(x, y, self.age)


# класс дерева
class Tree:
    def __init__(self, x, y):
        self.age = 1
        self.x = x
        self.y = y
        self.branch = Branch(10, 270, 1, [])
        self.energy = 0

    def branch_growth(self):# костыль(немного стыдно)
        branch_growth(self.branch, self.age)

    def growth(self):# функция роста дерева
        apples_growth(self.x, self.y, self.branch, self)
        self.branch_growth()

        self.age += 1
        if self.energy < self.age / REQUIRED_ENERGY:# удаления дерева в случае нехватки энергии
            del trees[trees.index(tree)]


    def draw(self):# отрисовка дерева
        tree_draw(self.x, self.y, self.branch, self)


    def energy_generation(self):
        energy_generation(self.x, self.y, self.branch, self)# генерация энергии


# класс "блока света"
class LightBlock:
    def __init__(self):
        self.max_height = height
        self.tree = None


# класс "блока почвы"
class DirtBlock():
    def __init__(self):
        self.trees = []


# заполнения "энергетических блоков"
def filling_blocks():
    global lights_blocks, dirts_blocks
    lights_blocks = []
    dirts_blocks = []
    for _ in range(count_blocks):
        lights_blocks.append(LightBlock())
        dirts_blocks.append(DirtBlock())


# функция получения энергии из заполненых "энергетических блоков"
def getting_energy():
    for tree in trees:
        tree.energy = 0

    for light_block in lights_blocks:
        if light_block.tree:
            light_block.tree.energy += 1.2
    for dirt_block in dirts_blocks:
        for i in range(len(dirt_block.trees)):
            dirt_block.trees[i].energy += 0.8 / len(dirt_block.trees)


# функция собирания яблок по координатам
def picking_apples(x, y):
    for tree in trees:
        find_and_delete_apple(x, y, tree.x, tree.y, tree.branch)


# рекурсивная функция нахождения яблок попадающих по координатам
def find_and_delete_apple(x, y, last_branch_x, last_branch_y, branch):
    global apples
    if type(branch) == Apple:
        return
    new_x = last_branch_x + branch.length * cos(branch.angle / 180 * pi)
    new_y = last_branch_y + branch.length * sin(branch.angle / 180 * pi)
    for i in range(len(branch.branches) - 1, -1, -1):
        if type(branch.branches[i]) == Apple:
            if ((new_x - x) ** 2 + (new_y - y) ** 2) ** 0.5 <= 8:
                if 10 <= branch.branches[i].age < 13:
                    apples += 1
                del branch.branches[i]
    for b in branch.branches:
        find_and_delete_apple(x, y, new_x, new_y, b)


# заполнения хитбоксов
def filling_hit_blocks():
    global hit_blocks
    hit_blocks = []
    for i in range(10):
        hit_blocks.append([])
        for j in range(30):
            hit_blocks[i].append([])
    for tree in trees:
        filling_trees_hit_blocks(tree.x, tree.y, tree.branch, tree)


# рекурсивная функция заполнения хитбоксов дерева
def filling_trees_hit_blocks(last_branch_x, last_branch_y, branch, tree):
    if type(branch) == Apple:
        return

    new_cords = [last_branch_x + branch.length * cos(branch.angle / 180 * pi),
                 last_branch_y + branch.length * sin(branch.angle / 180 * pi)]
    if branch.age > 2:
        if -1 < last_branch_x < 1500 and -1 < last_branch_y < 500 and\
                tree not in hit_blocks[int(last_branch_y // hit_block_size)][int(last_branch_x // hit_block_size)]:
            hit_blocks[int(last_branch_y // hit_block_size)][int(last_branch_x // hit_block_size)].append(tree)

    for b in branch.branches:
        filling_trees_hit_blocks(*new_cords, b, tree)


# функция получения деревьев попадающих по координатам
def cords_to_trees(x, y):
    filling_hit_blocks()
    return hit_blocks[int(y // hit_block_size)][int(x // hit_block_size)]


# удобрения деревьев
def fertilize_trees(trees_):
    for tree in trees_:
        for i in range(5):
            tree.branch_growth()
        tree.age += 5


# удаление деревьев
def delete_trees(trees_):
    for tree in trees_:
        del trees[trees.index(tree)]


# создание дерева по координатам
def create_tree(x, y):
    if -1 < x < 1500 and 375 < y < 500:
        trees.append(Tree(x, y))


# функция отрисовки кнопок
def buttons_draw():
    global buttons
    store_image = pygame.image.load('data/store.png')
    screen2.blit(store_image, (0, 500))
    for button in buttons:
        image = pygame.image.load('data/' + button.images[0 if button.first_image else 1])
        button.rect = image.get_rect()
        screen2.blit(image, (button.x, button.y))


buttons = [Button(22 + 500, 486, ['add_classic.png', 'add_pressed.png']),
           Button(22 + 500, 837, ['delete_classic.png', 'delete_pressed.png']),
           Button(22 + 500, 1188, ['fertilize_classic.png', 'fertilize_pressed.png'])]
buttons_draw()
# импорт и настройка кнопок

hit_block_size = height / 10
pressed_button = -1
apples = 0
REQUIRED_ENERGY = 12
# всякие константы

red_apples = []# красные
bad_apples = []# не красные
# списки яблок

scene_age = 0
fallen_apples = []
falling_apples = []
trees = [Tree(780, 450)]# первое дерево

filling_blocks()
trees_event_pause = 30# количество тиков до начала игры
trees_event = 0

scene_age = 0
scene_start = 100

scene_surf = pygame.image.load('data/scene.png')
scene_rect = scene_surf.get_rect()

loading_image = pygame.image.load('data/loading.png')
loading_rect = loading_image.get_rect()

screen.blit(loading_image, (0, 0))
pygame.display.flip()

while running:

    screen2.blit(scene_surf, scene_rect)
    scene_age += 1
    falling_apples_function(draw=scene_age >= scene_start)# функция падения яблок

    trees_event += 1
    if trees_event >= trees_event_pause or scene_age < scene_start:# проверка на начало игры
        # и на то сейчас ли тик обновления деревьев

        trees_event = 0
        filling_blocks()
        for tree in trees:
            tree.energy_generation()
        getting_energy()
        # генерация и выдача энергии

        for tree in trees:
            tree.growth()
        # рост деревьев

        fallen_apples_function()
        # функция упавших яблок

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:

            if pressed_button == 0:# нажатая кнопка "создание дерева"
                if apples >= 20:# цена использовния кнопки
                    apples -= 20
                    create_tree(*event.pos)
            elif pressed_button == 1:# нажатая кнопка "удаление дерева"
                if apples >= 20:
                    apples -= 20
                    delete_trees(cords_to_trees(*event.pos))
            elif pressed_button == 2:# нажатая кнопка "удобрение дерева"
                if apples >= 10:
                    apples -= 10
                    fertilize_trees(cords_to_trees(*event.pos))

            picking_apples(*event.pos)# собирание яблок на координатах нажатия

            pressed_button = -1

            for button in buttons:
                button.first_image = True
                if button.click(*event.pos):
                    pressed_button = buttons.index(button)
                    button.first_image = not button.click(*event.pos)
            # выбор нажатой кнопки

    if scene_age >= scene_start:# проверка на начало игры
        fallen_apples_draw()
        for tree in trees:
            tree.draw()
        buttons_draw()
        textsurface = myfont.render(str(apples), False, (143, 75, 51))
        screen2.blit(textsurface, (94, 50 + 500))
        screen.blit(screen2, (0, 0))
        pygame.display.flip()
        clock.tick(1000)
        # отрисовка всего

pygame.quit()

