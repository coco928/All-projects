# -*- coding:utf-8 -*-

from typing import *
from Settings import DialogSettings, ShopSettings, GamePath
import pygame
from Field import *
from Player import *

class ShoppingBox:
    def __init__(self, window, npcPath, player, items,
                 fontSize: int = ShopSettings.goodsSize, 
                 fontColor: Tuple[int, int, int] = (255, 255, 255), 
                 bgColor: Tuple[int, int, int, int] = (0, 0, 0, 150)):
        self.window = window
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(None, self.fontSize)
        
        self.bg = pygame.Surface((ShopSettings.boxWidth, 
                                  ShopSettings.boxHeight),pygame.SRCALPHA)
        self.bg.fill(bgColor)

        self.npc = pygame.image.load(npcPath)
        self.npc = pygame.transform.scale(self.npc,
                (DialogSettings.npcWidth, DialogSettings.npcHeight))
        
        self.player = player
        self.items = items

        self.selectedID = 0



    def buy(self):
        if self.selectedID == 0:
            self.player.attr_update(addCoins = -7, addAttack = 1)
            return
        elif self.selectedID == 1:
            self.player.attr_update(addCoins = -7, addDefence = 1)
            return
        elif self.selectedID == 2:
            self.player.attr_update(addCoins = -5, addHP = 5)
            return
        elif self.selectedID == 3:
            self.player.attr_update(addFruits = -4, addPotion = 1)
            return
        elif self.selectedID == 4:
            self.player.attr_update(addCoins = -3, addCabbage = 1)
            return
        elif self.selectedID == 5:
            self.player.attr_update(addCoins = -3, addWatermelon = 1)
            return
        elif self.selectedID == 6:
            self.player.attr_update(addCoins = -3, addBroccoli = 1)
            return

    def plant(self, field):
        if self.selectedID == 0:
            if self.player.cabbage > 0 :
                self.player.attr_update(addCabbage = -1)
                field.is_planted = True
                field.cabbage = True
                self.player.fruits_planted.add(Fruit(field, GamePath.cabbage))
            else:
                field.is_planted = False
        elif self.selectedID == 1:
            if self.player.watermelon > 0:
                self.player.attr_update(addWatermelon = -1)
                field.is_planted = True
                field.watermelon = True
                self.player.fruits_planted.add(Fruit(field, GamePath.watermelon))
            else:
                field.is_planted = False
        elif self.selectedID == 2:
            if self.player.broccoli > 0:
                self.player.attr_update(addBroccoli = -1)
                field.is_planted = True
                field.broccoli = True
                self.player.fruits_planted.add(Fruit(field, GamePath.broccoli))
            else:
                field.is_planted = False
        

    def render(self):
        self.window.blit(self.bg, 
            (ShopSettings.boxStartX, ShopSettings.boxStartY))
        self.window.blit(self.npc,
            (DialogSettings.npcCoordX, DialogSettings.npcCoordY))
        
        offset = 0
        for id, item in enumerate(list(self.items.keys())):
            if id == self.selectedID:
                text = '-->' + item + ' ' + self.items[item]
            else:
                text = '      ' + item + ' ' + self.items[item]
            self.window.blit(self.font.render(text, True, self.fontColor),
                (ShopSettings.textStartX+25, ShopSettings.textStartY + offset))
            offset += ShopSettings.textVerticalDist

        
        texts = ["Coins: " + str(self.player.money),
                 "HP: " + str(self.player.HP),
                 "Attack: " + str(self.player.attack),
                 "Defence: " + str(self.player.defence),
                 "Detris: " + str(self.player.debris),
                 "CabbageSeed: " + str(self.player.cabbage),
                 "WatermelonSeed: " + str(self.player.watermelon),
                 "BroccoliSeed: " + str(self.player.broccoli),
                 "Potion: " + str(self.player.potion),
                 "Fruits:" + str(self.player.fruits)
                 ]
    
        offset = 0
        for text in texts:
            self.window.blit(self.font.render(text, True, self.fontColor),
                (ShopSettings.textStartX + ShopSettings.boxWidth * 7/10, ShopSettings.textStartY + offset))
            offset += ShopSettings.textVerticalDist
       