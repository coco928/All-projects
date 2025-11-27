# -*- coding:utf-8 -*-

from Settings import *
import pygame

class Field(pygame.sprite.Sprite):
    def __init__(self, x, y, scene):
        super().__init__()
        self.image = pygame.image.load(GamePath.field)
        self.image = pygame.transform.scale(self.image,
                            (SceneSettings.tileWidth*2, SceneSettings.tileHeight*1))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.talking = False
        self.talkCD = 0 # cooldown of talk
        self.index = 0
        self.is_planted = False
        self.x = x
        self.y = y
        self.scene = scene
        self.cabbage = False
        self.watermelon = False
        self.broccoli = False

    
    def draw(self, window, dx=0, dy=0):
        window.blit(self.image, self.rect)

    def grow_plants(self, window):
        
        if self.index < 35:
            self.index += 1
            window.blit(GamePath.shovel_iamges[self.index], (self.x -10, self.y + 15))
        else:
            self.index = 35
            seed = pygame.image.load(GamePath.seed)
            seed = pygame.transform.scale(seed,(SceneSettings.seedWidth,SceneSettings.seedHeight))
            window.blit(seed, (self.x + 20 , self.y - 10))
        pass


    def reset_talk_CD(self):
        self.talkCD = NPCSettings.talkCD 

    def can_talk(self):
        return self.talkCD == 0


class Fruit(pygame.sprite.Sprite):
    def __init__(self, field, image):    
        super().__init__()    
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image,
                            (FieldSettings.fruitWidth,
                              FieldSettings.fruitHeight))
        self.field = field
        self.rect = self.image.get_rect()
        self.rect.x = field.x
        self.rect.y = field.y - 35

    def draw(self, window, dx=0, dy=0):
        window.blit(self.image, self.rect)       


