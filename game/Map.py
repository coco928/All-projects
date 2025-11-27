# -*- coding:utf-8 -*-
from Settings import *
import pygame
from random import randint,random
from Scene import *
from NPC import Boss,Monster

class Block(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

def gen_city_map():
    images = [pygame.image.load(tile) for tile in GamePath.cityTiles]
    images = [pygame.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight)) for image in images]

    mapObj = []
    for i in range(SceneSettings.tileXnum):
        tmp = []
        for j in range(SceneSettings.tileYnum):
            tmp.append(images[randint(0, len(images) - 1)])
        mapObj.append(tmp)

    return mapObj

def gen_wild_map():
    images = [pygame.image.load(tile) for tile in GamePath.groundTiles]
    images = [pygame.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight)) for image in images]

    mapObj = []
    for i in range(4*SceneSettings.tileXnum):
        tmp = []
        for j in range(4*SceneSettings.tileYnum):
            tmp.append(images[randint(0, len(images) - 1)])
        mapObj.append(tmp)
    
    return mapObj

def gen_home_map():
    bg = pygame.image.load(GamePath.home_bg)
    bg = pygame.transform.scale(bg, (HomeSettings.windowWidth,HomeSettings.windowHeight))
    return bg

def gen_obstacles():
    image = pygame.image.load(GamePath.tree) 

    obstacles = pygame.sprite.Group()
    # donot generate in the original position of player
    # 左上没生成障碍，因为没做npc和障碍的碰撞
    midx = SceneSettings.tileXnum//2
    midy = SceneSettings.tileYnum//2
    for i in range(SceneSettings.tileXnum):
        for j in range(SceneSettings.tileYnum):
            # 防止在出生点生成obstacle
            if random() < SceneSettings.obstacleDensity and not(i < midx and j < midy) and (i not in range(midx-3, midx+3)) and (j not in range(midy-3, midy+3)):
                obstacles.add(Block(image, SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
    return obstacles 

def get_monster(type):
    monster1 = pygame.sprite.Group()
    monster2 = pygame.sprite.Group()
    for i in range(-15, 35, 4):
        for j in range(-9, 16, 4):
            if (random() < SceneSettings.obstacleDensity and not (0 < i < 16 or i == 29) and
                    (j != 9 and j != 7 and j != 8)):
                monster1.add(Monster(SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
    if type == "monster":
        return monster1
    else:
        return monster2


def get_obstacles(day):
    image = pygame.image.load(GamePath.box)
    obstacles = pygame.sprite.Group()
    if day != 3:
        Matrix = [[4, 8]]
        for i in range(-17, 40, 1):
            Matrix.append([i, -10])
            Matrix.append([i, 18])
        for j in range(-10, 18, 1):
            Matrix.append([-17, j])
            Matrix.append([40, j])

        for i in range(-17, 30, 1):
            Matrix.append([i, 7])
        for j in range(-4, 7, 1):
            Matrix.append([30, j])
        for j in range(-10, 3, 1):
            Matrix.append([23, j])
        for j in range(-5, 8, 1):
            Matrix.append([16, j])

        for s in Matrix:
            x = s[0]
            y = s[1]
            obstacles.add(Block(image, SceneSettings.tileWidth * x, SceneSettings.tileHeight * y))
    else:
        obstacles.add(Block(image, SceneSettings.tileWidth * 40, SceneSettings.tileHeight * 18))
    return obstacles



      

