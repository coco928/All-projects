# -*- coding:utf-8 -*-

from Settings import *
import pygame
from Player import*
from Map import *
from Settings import *
from random import randint
from Map import *


# 设置 NPC
class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(GamePath.npc)
        self.image = pygame.transform.scale(self.image, (NPCSettings.npcWidth, NPCSettings.npcHeight))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.initialPosition = x  # 记录初始位置
        self.speed = NPCSettings.npcSpeed
        self.direction = 1
        self.patrollingRange = 70  # 巡逻范围
        self.talkCD = 0 # cooldown of talk
        self.talking = False


    def update(self):
        if not self.talking:
            self.rect.x += self.speed * self.direction
            if abs(self.rect.x - self.initialPosition) > self.patrollingRange:
                self.direction *= -1  # 反转方向
                self.image = pygame.transform.flip(self.image, True, False)
            if self.talkCD > 0:
                self.talkCD -= 1

    
    def reset_talk_CD(self):
        self.talkCD = NPCSettings.talkCD 

    def can_talk(self):
        return self.talkCD == 0




class Desk(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(GamePath.desk)
        self.image = pygame.transform.scale(self.image,
                            (ShopSettings.deskWidth, ShopSettings.deskHeight))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.talking = False
        self.talkCD = 0 # cooldown of talk        

    
    def draw(self, window, dx=0, dy=0):
        window.blit(self.image, self.rect)

    def reset_talk_CD(self):
        self.talkCD = NPCSettings.talkCD 

    def can_talk(self):
        return self.talkCD == 0        


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y,speed,type,a,b):
        super().__init__()
        if type == 1:
            self.image = pygame.image.load(GamePath.food)
            self.image = pygame.transform.scale(self.image, (30,30))
        else:
            self.image = pygame.image.load(GamePath.food1)
            self.image = pygame.transform.scale(self.image, (45,30))
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.a = a
        self.b = b
    
    def update(self):
        if self.rect.y >= 560:
            self.rect.y = 60
            self.rect.x = randint(self.a,self.b)
        else:
            self.rect.y += self.speed


class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [pygame.transform.scale(pygame.image.load(img),(MonsterSettings.monsterWidth, MonsterSettings.monsterHeight)) for img in GamePath.monster]
        self.images[1] = pygame.transform.flip(self.images[1], True, False)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.x = x
        self.y = y
        self.initialPosition = y  # 记录初始位置
        self.speed = randint(1,2)+randint(1,5)%10
        self.direction = 1
        self.patrollingRange = 25
        self.HP = MonsterSettings.monsterHP
        self.Attack = MonsterSettings.monsterAttack
        self.Defense = MonsterSettings.monsterDefense
        self.Height = MonsterSettings.monsterHeight
        self.Width = MonsterSettings.monsterWidth
        self.gold_coin = MonsterSettings.monsterCoin

    def update(self):
        self.rect.y += self.speed * self.direction
        if abs(self.rect.y - self.initialPosition) > self.patrollingRange:
            self.direction *= -1  # 反转方向
        if self.speed != 0:
            if self.direction == -1:
                self.image = self.images[1]
            if self.direction == 1:
                self.image = self.images[0]

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y,centerx,centery):
        super().__init__()
        self.images = [pygame.transform.scale(pygame.image.load(img),(MonsterSettings.monsterWidth * 3, MonsterSettings.monsterHeight * 3))for img in GamePath.boss]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.initialPosition = 0
        self.x = x
        self.y = y
        self.centerx = centerx
        self.centery = centery
        self.dirx = 1
        self.diry = 1
        self.HP = MonsterSettings.monsterHP + 14
        self.Attack = MonsterSettings.monsterAttack + 3
        self.Defense = MonsterSettings.monsterDefense + 3
        self.Height = MonsterSettings.monsterHeight
        self.Width = MonsterSettings.monsterWidth-100
        self.gold_coin = MonsterSettings.monsterCoin + 100

    def update(self):
        self.diry = (self.rect.x-self.centerx)/((self.rect.x-self.centerx)**2+(self.rect.y-self.centery)**2)**(1/2)
        self.dirx = (self.rect.y-self.centery)/((self.rect.x-self.centerx)**2+(self.rect.y-self.centery)**2)**(1/2)
        self.rect.x += self.dirx*0.8
        self.rect.y -= self.diry*0.8
        if self.diry > 0 and self.dirx < 0:
            self.image = self.images[2]
        elif self.diry < 0 and self.dirx > 0:
            self.image = pygame.transform.flip(self.images[2], True, False)
        elif self.dirx > 0 and self.diry > 0:
            self.image = self.images[3]
        elif self.dirx < 0 and self.diry < 0:
            self.image = self.images[0]


