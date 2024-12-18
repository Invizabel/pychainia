import os
import pygame
import random
import sys
import textwrap
import time
from kivy.utils import platform
from pygame.locals import *

def pychainia():
    pygame.init()

    pygame.mixer.init()
    
    pygame.display.set_caption("Pychainia")
    display = pygame.display.set_mode((128, 64),pygame.FULLSCREEN | pygame.SCALED)

    try:
        from kivy.resources import resource_find
        peashooter_img = pygame.image.load(resource_find("assets/peashooter.png")).convert_alpha()
        sunflower_img = pygame.image.load(resource_find("assets/sunflower.png")).convert_alpha()
        cherrybomb_img = pygame.image.load(resource_find("assets/cherrybomb.png")).convert_alpha()
        walnut_img = pygame.image.load(resource_find("assets/walnut.png")).convert_alpha()
        potatomine_img = pygame.image.load(resource_find("assets/potatomine.png")).convert_alpha()
        pygame.mixer.music.load(resource_find("assets/Grasswalk.mp3"))
        pygame.mixer.music.play(-1)


    except Exception as error:
        new_error = "\n".join(textwrap.wrap(str(error), 12))
        # if we can't find the files, display an error message! :)
        my_font = pygame.font.SysFont("calibri", 12)
        while True:
            display.fill("RED")
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            error_font = my_font.render(f"DEBUG: {new_error}", False, "BLACK")
            display.blit(error_font, (0, 0))
            pygame.display.update()
    
    my_font = pygame.font.SysFont("calibri", 8)
    cooldown_font = pygame.font.SysFont("calibri", 20)
    pygame.mouse.set_visible(True)

    clock = pygame.time.Clock()

    cursor_x = 6
    cursor_y = 6
    cursor_color = "BLACK"

    pea_progress = 0
    player_choice = None
    ticks = 0
    sun = 50
    
    
    choices = [peashooter_img,sunflower_img,cherrybomb_img,walnut_img,potatomine_img]
    cooldown_key = [8,8,50,30,30]
    new_cooldown_key = cooldown_key[:]

    board = [[None,None,None,None,None,None,None,None,None],
             [None,None,None,None,None,None,None,None,None],
             [None,None,None,None,None,None,None,None,None],
             [None,None,None,None,None,None,None,None,None]]

    explode_bool = [[False,False,False,False,False,False,False,False,False],
                    [False,False,False,False,False,False,False,False,False],
                    [False,False,False,False,False,False,False,False,False],
                    [False,False,False,False,False,False,False,False,False]]

    explode_timer = [[5,5,5,5,5,5,5,5,5],
                     [5,5,5,5,5,5,5,5,5],
                     [5,5,5,5,5,5,5,5,5],
                     [5,5,5,5,5,5,5,5,5]]

    while True:
        time.sleep(0.1)
        display.fill("ORANGE")
        ticks += 1
        if ticks == 10:
            ticks = 0

            for j,x in enumerate(board):
                for i,y in enumerate(x):
                    if explode_bool[j][i] and explode_timer[j][i] >= 0:
                        explode_timer[j][i] -= 1

                    elif explode_timer[j][i] < 0:
                        explode_timer[j][i] = 5
                        explode_bool[j][i] = False
                        board[j][i] = None

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.FINGERDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                dx, dy = pygame.mouse.get_pos()
                grid_x = (dx // 12) * 12
                grid_y = (dy // 12) * 12

                if grid_x + 12 // 2 < 114 and grid_y + 12 // 2 < 54:
                    cursor_x, cursor_y = grid_x + 12 // 2, grid_y + 12 // 2

                if grid_x + 16 // 2 < 114 and grid_y + 16 // 2 > 52 and grid_y + 16 // 2 < 58:
                    cursor_x, cursor_y = grid_x + 12 // 2, 58

                if cursor_y == 58:
                    for i,j in enumerate(choices):
                        if i * 12 + 6 == cursor_x:
                            player_choice = j

                elif cursor_y < 58:
                    for j,x in enumerate(board):
                        for i,y in enumerate(x):
                            if i == int(cursor_x / 12) and j == int(cursor_y / 12):
                                if sun >= 100 and player_choice == peashooter_img and board[j][i] == None and new_cooldown_key[0] == 0:
                                    board[j][i] = peashooter_img
                                    sun -= 100
                                    new_cooldown_key[0] = cooldown_key[0]
                                    player_choice = None

                                if sun >= 50 and player_choice == sunflower_img and board[j][i] == None and new_cooldown_key[1] == 0:
                                    board[j][i] = sunflower_img
                                    sun -= 50
                                    new_cooldown_key[1] = cooldown_key[1]
                                    player_choice = None

                                if sun >= 150 and player_choice == cherrybomb_img and board[j][i] == None and new_cooldown_key[2] == 0:
                                    if explode_timer[j][i] > 0:
                                        explode_bool[j][i] = True
                                        board[j][i] = cherrybomb_img
                                        sun -= 150
                                        new_cooldown_key[2] = cooldown_key[2]
                                        player_choice = None

                                if sun >= 50 and player_choice == walnut_img and board[j][i] == None and new_cooldown_key[3] == 0:
                                    board[j][i] = walnut_img
                                    sun -= 50
                                    new_cooldown_key[3] = cooldown_key[3]
                                    player_choice = None

                                if sun >= 25 and player_choice == potatomine_img and board[j][i] == None and new_cooldown_key[4] == 0:
                                    board[j][i] = potatomine_img
                                    sun -= 25
                                    new_cooldown_key[4] = cooldown_key[4]
                                    player_choice = None

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == K_SPACE:
                    if cursor_y == 58:
                        for i,j in enumerate(choices):
                            if i * 12 + 6 == cursor_x:
                                player_choice = j

                    if cursor_y < 58:
                        for j,x in enumerate(board):
                            for i,y in enumerate(x):
                                if i == int(cursor_x / 12) and j == int(cursor_y / 12):
                                    if sun >= 100 and player_choice == peashooter_img and board[j][i] == None and new_cooldown_key[0] == 0:
                                        board[j][i] = peashooter_img
                                        sun -= 100
                                        new_cooldown_key[0] = cooldown_key[0]
                                        player_choice = None

                                    if sun >= 50 and player_choice == sunflower_img and board[j][i] == None and new_cooldown_key[1] == 0:
                                        board[j][i] = sunflower_img
                                        sun -= 50
                                        new_cooldown_key[1] = cooldown_key[1]
                                        player_choice = None

                                    if sun >= 150 and player_choice == cherrybomb_img and board[j][i] == None and new_cooldown_key[2] == 0:
                                        if explode_timer[j][i] > 0:
                                            explode_bool[j][i] = True
                                            board[j][i] = cherrybomb_img
                                            sun -= 150
                                            new_cooldown_key[2] = cooldown_key[2]
                                            player_choice = None

                                    if sun >= 50 and player_choice == walnut_img and board[j][i] == None and new_cooldown_key[3] == 0:
                                        board[j][i] = walnut_img
                                        sun -= 50
                                        new_cooldown_key[3] = cooldown_key[3]
                                        player_choice = None

                                    if sun >= 25 and player_choice == potatomine_img and board[j][i] == None and new_cooldown_key[4] == 0:
                                        board[j][i] = potatomine_img
                                        sun -= 25
                                        new_cooldown_key[4] = cooldown_key[4]
                                        player_choice = None
                                            
                if event.key == K_UP or event.key == K_w:
                    if cursor_y < 58 and cursor_y > 6:
                        cursor_y -= 12

                    elif cursor_y == 58:
                        cursor_y -= 16

                if event.key == K_DOWN or event.key == K_s:
                    if cursor_y < 42:
                        cursor_y += 12

                    elif cursor_y == 42:
                        cursor_y += 16

                if event.key == K_LEFT or event.key == K_a:
                    if cursor_x > 6:
                        cursor_x -= 12

                if event.key == K_RIGHT or event.key == K_d:
                    if cursor_x < 102:
                        cursor_x += 12

        # draw tiles
        for i in range(0,108, 12):
            pygame.draw.rect(display, "black", [i, 0, 12, 12], 1)
            pygame.draw.rect(display, "black", [i, 12, 12, 12], 1)
            pygame.draw.rect(display, "black", [i, 24, 12, 12], 1)
            pygame.draw.rect(display, "black", [i, 36, 12, 12], 1)
            pygame.draw.rect(display, "black", [i, 52, 12, 12], 1)

        # draw plant choices
        for i,j in enumerate(choices):
            display.blit(j, ((i * 6) * 2 + 2, 54))

        # draw plants on board
        for i,x in enumerate(board):
            for j,y in enumerate(x):
                if y != None:
                    display.blit(y, ((j * 6) * 2 + 2, (i * 6) * 2 + 2))

        # calculate sun
        sunflower_count = 0
        for i in board:
            sunflower_count += i.count(sunflower_img)

        # sun from sunflowers
        for i in range(0,sunflower_count):
            my_rand = random.randint(1,240)
            if my_rand == 1:
                if sun + 25 < 1000:
                    sun += 25

                else:
                    sun = 9999

        # sun from sky
        my_rand = random.randint(1,100)
        if my_rand == 1:
            if sun + 25 < 1000:
                sun += 25

            else:
                sun = 999
        

        # draw ammo
        pea_bool = True
        for i,x in enumerate(board):
            for j,y in enumerate(x):
                if y == peashooter_img:
                    if pea_bool:
                        pea_progress += 4
                        pea_bool = False

                    if pea_progress + (j * 6) * 2 + 12 <= 108:
                        pygame.draw.circle(display, "black", [pea_progress + (j * 6) * 2 + 8, (i * 6) * 2 + 4], 2, 0)

                    if pea_progress == 108:
                        pea_progress = 0

        # draw cursor
        pygame.draw.circle(display, "BLACK", [cursor_x, cursor_y], 6, 1)

        # draw sun text
        new_sun = ""
        for i in str(sun):
            new_sun += i + " "

        sun_font = my_font.render(new_sun, False, "BLACK")
        display.blit(sun_font, (110, 0))

        # draw cooldown text
        if ticks == 9:
            for i,j in enumerate(choices):
                if  new_cooldown_key[i] - 1 >= 0:
                    new_cooldown_key[i] -= 1

        for i,j in enumerate(choices):
            if new_cooldown_key[i] != 0:
                new_cooldown_font = cooldown_font.render("X", False, "BLACK")
                display.blit(new_cooldown_font, ((i * 12) + 1, 50))

        # refresh
        pygame.display.update()

if __name__ == "__main__":
    pychainia()
