# -*- coding:utf-8 -*-

from Settings import *
import pygame
from Scene import *
from Field import *

# 设置角色动画
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [pygame.transform.scale(pygame.image.load(img), 
                            (PlayerSettings.playerWidth, PlayerSettings.playerHeight)) for img in GamePath.player]
        self.flipimgs = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(img), 
                            (PlayerSettings.playerWidth, PlayerSettings.playerHeight)),True,False) for img in GamePath.player_state]
        self.walkimgs = [pygame.transform.scale(pygame.image.load(img), 
                            (PlayerSettings.playerWidth, PlayerSettings.playerHeight)) for img in GamePath.player_state]
        self.index = 0
        self.image = self.images[self.index]
        self.isfighting = False
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = PlayerSettings.playerSpeed
        self.talking = False
        # home
        self.sleep = PlayerSettings.playersleep
        self.saciety = PlayerSettings.playersaciety
        # attr
        self.HP = PlayerSettings.playerHP
        self.attack = PlayerSettings.playerAttack
        self.defence = PlayerSettings.playerDefence
        self.potion = PlayerSettings.playerPotion
        self.cabbage = PlayerSettings.playerCabbage
        self.watermelon = PlayerSettings.playerWatermelon
        self.broccoli = PlayerSettings.playerBroccoli
        self.money = PlayerSettings.playerMoney
        self.debris = PlayerSettings.playerDebris
        self.fruits = PlayerSettings.playerFruits
        self.day = days
        self.dx = 0
        self.dy = 0
        self.fruits_planted = pygame.sprite.Group()
        self.coll_w = 0


    def attr_update(self, addCoins = 0, addHP = 0, addAttack = 0, addDefence = 0,addPotion = 0,addCabbage = 0,
                    addWatermelon = 0,addBroccoli = 0,addsaciety = 0,addsleep = 0,adddebris = 0, addFruits = 0):
        if self.money + addCoins < 0:
            return
        if self.HP + addHP < 0:
            return
        if self.cabbage + addCabbage < 0:
            return
        if self.watermelon + addWatermelon < 0:
            return
        if self.broccoli + addBroccoli < 0:
            return
        if self.fruits + addFruits < 0:
            return
        if self.defence + addDefence >3:
            return
        self.money += addCoins
        self.HP += addHP
        self.attack += addAttack
        self.defence += addDefence
        self.potion += addPotion
        self.cabbage += addCabbage
        self.watermelon += addWatermelon
        self.broccoli += addBroccoli
        self.sleep += addsleep
        self.saciety += addsaciety
        self.debris += adddebris
        self.fruits += addFruits


    
    def update(self, keys, state):
        if self.talking:
            # 如果不移动，显示静态图像
            self.index = 0
            self.image = self.walkimgs[self.index]
        elif self.isfighting:
            self.index = 0
            self.image = self.walkimgs[self.index]            
        elif state == GameState.GAME_PLAY_HOME or state == GameState.README:
            self.dx = 0
            self.dy = 0
            if keys[pygame.K_LEFT] and self.rect.left > 240:
                self.dx -= self.speed
                self.image = self.flipimgs[self.index]
            elif keys[pygame.K_RIGHT] and self.rect.right < 1040:
                self.dx += self.speed                
                self.image = self.walkimgs[self.index]
            else:
                self.image = self.images[0]
               
            self.rect = self.rect.move(self.dx, self.dy)
            if any(keys):
               self.index = (self.index + 1) % 6


        else:
            # Update Player Position
            self.dx = 0
            self.dy = 0
            if keys[pygame.K_UP]:
                if self.rect.top > 0:
                    self.dy -= self.speed
                if self.image in self.walkimgs:
                    self.image = self.walkimgs[self.index]
                else:
                    self.image = self.image = self.flipimgs[self.index]
            if keys[pygame.K_DOWN]:
                if self.rect.bottom < WindowSettings.height:
                    self.dy += self.speed
                if self.image in self.walkimgs:
                    self.image = self.walkimgs[self.index]
                else:
                    self.image = self.image = self.flipimgs[self.index]               
            if keys[pygame.K_LEFT]:
                if self.rect.left > 0:
                    self.dx -= self.speed
                self.image = self.flipimgs[self.index]
                
                    
            if keys[pygame.K_RIGHT]:
                if self.rect.right < WindowSettings.width:
                    self.dx += self.speed                
                self.image = self.walkimgs[self.index]
                
            self.rect = self.rect.move(self.dx, self.dy)

            # 更新角色动画
            if any(keys):
               self.index = (self.index + 1) % 6 

                


    def draw(self, window):
        window.blit(self.image, self.rect)