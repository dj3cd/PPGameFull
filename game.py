# графическая библиотека
from tkinter import *
import time
import random
import pygame
import shelve

pygame.init()

display_width = 800
display_height = 600

pygame.mixer.init()

jump_sound = pygame.mixer.Sound("kick.wav")
fail_sound = pygame.mixer.Sound("collabs.wav")
lose_sound = pygame.mixer.Sound('fail.wav')  # конец хп
hp_get_sound = pygame.mixer.Sound('hpget.wav')  # подбор хп
button_sound = pygame.mixer.Sound("button.wav")

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('PP_Game')

icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

block_img = [pygame.image.load('block0.png'), pygame.image.load('block1.png'),
             pygame.image.load('block2.png')]  # 0 - некрасивая леши | 1- коробка мирэа | 2 - красивая леши
block_options = [20, 430, 50, 450, 25, 420]

down_image = [pygame.image.load('down0.png'), pygame.image.load('down1.png')]
up_image = [pygame.image.load('rock0.png'), pygame.image.load('rock1.png')]

hp_img = pygame.image.load("heart.png")
hp_img = pygame.transform.scale(hp_img, (35, 35))  # размер сердец

img_counter = 0
hp = 2




class Object:
    def __init__(self, x, y, widht, image, speed):
        self.x = x
        self.y = y
        self.width = widht
        self.image = image
        self.speed = speed

    # функция передвижения кактуса
    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            # pygame.draw.rect(display, (224, 121, 39), (self.x, self.y, self.width, self.height))
            self.x -= self.speed
            return True
        else:
            return False

    def return_self(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))


class Button:
    def __init__(self, widht, height):
        self.widht = widht
        self.height = height
        self.inactive = (67, 33, 94)
        self.active_color = (118, 109, 190)

    def draw(self, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.widht and y < mouse[1] < y + self.height:
            pygame.draw.rect(display, self.active_color, (x, y, self.widht, self.height))

            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(100)
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()
        else:
            pygame.draw.rect(display, self.inactive, (x, y, self.widht, self.height))

        print_text(message=message, x=x + 10, y=y + 10, font_size=font_size)


# песронаж
user_width = 55
user_height = 75
usr_x = display_width // 3
usr_y = display_height - user_height - 110

# преграды

block_width = 20
block_height = 70
block_x = display_width - 50
block_y = display_height - block_height - 100

clock = pygame.time.Clock()

make_jump = False
jump_counter = 30

scores = 0
max_scores = 0
max_above = 0


def show_menu():
    menu_background = pygame.image.load("menu.png")

    pygame.mixer.music.load("mainmenu.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    #start_btn = Button(300, 70)
    quit_btn = Button(180, 60)
    lvl_btn1 = Button(200, 60)
    lvl_btn2 = Button(200, 60)
    pers_btn1 = Button(200, 60)
    pers_btn2 = Button(200, 60)
    terr_btn1 = Button(200, 60)
    terr_btn2 = Button(200, 60)
    sound_btn = Button(70, 40)
    sound_btn1 = Button(95, 40)
    show = True

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        display.blit(menu_background, (0, 0))
        #start_btn.draw(250, 200, "Start game", 40)
        quit_btn.draw(310, 500, "Quit", quit, 20)
        lvl_btn1.draw(25, 300, "Cosmic", choose_lvl1, 20)
        lvl_btn2.draw(25, 200, "Forest", choose_lvl2, 20)
        pers_btn1.draw(310, 200, "Common outfit", choose_pers1, 20)
        pers_btn2.draw(310, 300, "Custom outfit", choose_pers2, 20)
        terr_btn1.draw(575, 300, "Cosmic blocks", choose_terr1, 20)
        terr_btn2.draw(575, 200, "Forest blocks", choose_terr2, 20)
        sound_btn.draw(25, 540, "Mute", mute, 20 )
        sound_btn1.draw(100, 540, "Unmute", unmute, 20)

        pygame.display.update()
        clock.tick(60)

land = 0

pers_img = [pygame.image.load('anticrash.png'), pygame.image.load('anticrash.png'),
                pygame.image.load('anticrash.png')]

checkprob = 1

checkprob2 = 1

def mute():

    pygame.mixer.music.set_volume(0)

def unmute():

    pygame.mixer.music.set_volume(0.7)

def escpm():

    show_menu()

def choose_lvl1():

    global land, pers_img, block_img, block_options, down_image, up_image, checkprob, checkprob2
    land = pygame.image.load('land.png')

    if checkprob == 1:
        return
    if checkprob2 == 1:
        return
    if checkprob2 <= 0 and checkprob <= 0:
        while game_cycle():
            pass


def choose_pers1():

    global land, pers_img, block_img, block_options, down_image, up_image, checkprob, checkprob2

    pers_img = [pygame.image.load('pers0_b.png'), pygame.image.load('pers1_b.png'),
                pygame.image.load('pers2_b.png')]
    checkprob = checkprob - 1

    return

def choose_terr1():

    global land, pers_img, block_img, block_options, down_image, up_image, checkprob, checkprob2

    block_img = [pygame.image.load('block0.png'), pygame.image.load('block1.png'),
                 pygame.image.load('block2.png')]  # 0 - некрасивая леши | 1- коробка мирэа | 2 - красивая леши
    block_options = [20, 430, 50, 450, 25, 420]

    down_image = [pygame.image.load('down0.png'), pygame.image.load('down1.png')]

    up_image = [pygame.image.load('rock0.png'), pygame.image.load('rock1.png')]
    checkprob2 = checkprob2 - 1

    return

def choose_lvl2():

    global land, pers_img, block_img, block_options, down_image, up_image, checkprob, checkprob2
    land = pygame.image.load('land2.png')

    if checkprob == 1:
        return
    if checkprob2 == 1:
        return
    if checkprob2 <= 0 and checkprob <= 0:
        while game_cycle():
            pass

def choose_pers2():
    global land, pers_img, block_img, block_options, down_image, up_image, checkprob, checkprob2

    pers_img = [pygame.image.load('pers0_z.png'), pygame.image.load('pers1_z.png'),
                pygame.image.load('pers2_z.png')]
    checkprob = checkprob - 1

    return


def choose_terr2():
    global land, pers_img, block_img, block_options, down_image, up_image, checkprob, checkprob2

    block_img = [pygame.image.load('block0_z.png'), pygame.image.load('block1_z.png'),
                 pygame.image.load('block2_z.png')]  # 0 - некрасивая леши | 1- коробка мирэа | 2 - красивая леши
    block_options = [20, 430, 50, 450, 25, 420]

    down_image = [pygame.image.load('down0_z.png'), pygame.image.load('down1_z.png')]

    up_image = [pygame.image.load('up0_z.png'), pygame.image.load('up1_z.png')]

    checkprob2 = checkprob2 - 1

    return



def game_cycle():
    global scores, make_jump, jump_counter, usr_y, hp, land, Button

    game = True
    block_arr = []
    create_block_arr(block_arr)
    #land = pygame.image.load('land1.png')

    up, down = open_random_objects()

    heart = Object(display_width, 200, 35, hp_img, 6)

    button1 = Button(70, 40)
    button2 = Button(95, 40)
    button3 = Button(75, 30)

    scores = 0
    make_jump = False
    jump_counter = 30
    usr_y = display_height - user_height - 110
    hp = 2

    pygame.mixer.music.load("background.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)


    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            make_jump = True
        if keys[pygame.K_ESCAPE]:
            pause()

        if make_jump:
            jump()

        count_scores(block_arr)

        display.blit(land, (0, 0))

        print_text('Scores: ' + str(scores), 600, 10)
        button1.draw(25, 540, "Mute", mute, 20)
        button2.draw(100, 540, "Unmute", unmute, 20)
        button3.draw(730, 5, "Menu", escpm, 20)


        draw_array(block_arr)
        move_objects(down, up)

        # pygame.draw.rect(display, (165, 20, 52), (usr_x, usr_y, user_width, user_height) ) # персонаж - прямоугольник

        draw_pers()
        # show_health()
        heart.move()
        heart_plus(heart)

        if check_collision(block_arr):
            pygame.mixer.music.stop()
            # pygame.mixer.Sound.play(collabs_sound)
            # if not check_hp():

            game = False

        show_health()

        pygame.display.update()
        clock.tick(60)  # один кадр продолжается 60мс


    return game_over()


def jump():
    global usr_y, jump_counter, make_jump
    if jump_counter >= -30:
        if jump_counter == 30:
            pygame.mixer.Sound.play(jump_sound)
        if jump_counter == -25:
            pygame.mixer.Sound.play(jump_sound)

        usr_y -= jump_counter / 2
        jump_counter -= 1
    else:
        jump_counter = 30
        make_jump = False


def create_block_arr(array):
    choice = random.randrange(0, 3)
    img = block_img[choice]
    width = block_options[choice * 2]
    height = block_options[choice * 2 + 1]
    array.append(Object(display_width + 20, height, width, img, 3))

    choice = random.randrange(0, 3)
    img = block_img[choice]
    width = block_options[choice * 2]
    height = block_options[choice * 2 + 1]
    array.append(Object(display_width + 300, height, width, img, 3))

    choice = random.randrange(0, 3)
    img = block_img[choice]
    width = block_options[choice * 2]
    height = block_options[choice * 2 + 1]
    array.append(Object(display_width + 600, height, width, img, 3))


def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)

    if maximum < display_width:

        radius = display_width
        if radius - maximum < 50:
            radius += 250
    else:
        radius = maximum

    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(250, 400)

    return radius


def draw_array(array):
    for block in array:
        check = block.move()
        if not check:
            object_return(array, block)

            '''radius = find_radius(array)

            choice = random.randrange(0, 3)
            img = block_img[choice]
            width = block_options[choice * 2]
            height = block_options[choice * 2 + 1]

            block.return_self(radius, height, width, img)'''


def object_return(objects, obj):
    radius = find_radius(objects)

    choice = random.randrange(0, 3)
    img = block_img[choice]
    width = block_options[choice * 2]
    height = block_options[choice * 2 + 1]

    obj.return_self(radius, height, width, img)


def open_random_objects():
    choice = random.randrange(0, 2)
    img_of_down = down_image[choice]

    choice = random.randrange(0, 2)
    img_of_up = up_image[choice]

    down = Object(display_width, display_height - 80, 10, img_of_down, 10)
    up = Object(display_width, 10, 70, img_of_up, 14)

    return up, down


# облака камни и их траектория

def move_objects(down, up):
    check = down.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_down = down_image[choice]
        down.return_self(display_width, 500 + random.randrange(10, 80), down.width, img_of_down)

    check = up.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_up = up_image[choice]
        up.return_self(display_width, random.randrange(10, 100), up.width, img_of_up)  # высота камней


def draw_pers():
    global img_counter
    if img_counter == 9:
        img_counter = 0

    display.blit(pers_img[img_counter // 3], (usr_x, usr_y))
    img_counter += 1


def print_text(message, x, y, font_color = (252, 3, 190), font_type="abc.ttf", font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause():
    paused = True

    pygame.mixer.music.pause()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text("Paused ! Press enter to continue !", 100, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        clock.tick(15)

    pygame.mixer.music.unpause()


def check_collision(barriers):
    for barrier in barriers:

        if usr_y + user_height >= barrier.y:
            if barrier.x <= usr_x <= barrier.x + barrier.width:
                if check_hp():
                    object_return(barriers, barrier)
                    return False
                else:
                    return True
            elif barrier.x <= usr_x + user_width <= barrier.x + barrier.width:
                if check_hp():
                    object_return(barriers, barrier)
                    return False
                else:
                    return True

    return False


def count_scores(barriers):
    global scores, max_above
    above_block = 0

    if -20 <= jump_counter < 25:
        for barrier in barriers:
            if usr_y + user_height - 5 <= barrier.y:

                if barrier.x <= usr_x <= barrier.x + barrier.width:
                    above_block += 1

                elif barrier.x <= usr_x + user_width <= barrier.x + barrier.width:
                    above_block += 1

        max_above = max(max_above, above_block)
    else:
        if jump_counter == -30:
            scores += max_above
            max_above = 0


def game_over():
    global scores, max_scores

    if scores > max_scores:
        max_scores = scores
    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text("G a m e    o v e r ! ", 250, 560)
        print_text("Press ESC to exit to main menu", 160, 300)
        print_text("Press ENTER to restart the game", 140, 60)
        # print_text('Max scores: ' +str(max_scores), 300, 400)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            pygame.mixer.music.load("mainmenu.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            return False

        pygame.display.update()
        clock.tick(15)


def show_health():
    global hp
    show = 0
    x = 20
    while show != hp:
        display.blit(hp_img, (x, 20))
        x += 40
        show += 1


def check_hp():
    global hp
    hp -= 1
    if hp == 0:
        pygame.mixer.Sound.play(lose_sound)
        return False

    else:
        pygame.mixer.Sound.play(fail_sound)
        return True


def heart_plus(heart):
    global hp, usr_x, usr_y, user_width, user_height

    if heart.x <= -heart.width:
        radius = display_width + random.randrange(500, 2000)
        heart.return_self(radius, heart.y, heart.width, hp_img)

    if usr_x <= heart.x <= usr_x + user_width:
        if usr_y <= heart.y <= usr_y + user_height:
            pygame.mixer.Sound.play(hp_get_sound)
            if hp < 5:
                hp += 1

            radius = display_width + random.randrange(500, 1700)
            heart.return_self(radius, heart.y, heart.width, hp_img)


show_menu()
pygame.quit()
quit()
