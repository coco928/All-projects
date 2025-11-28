# -*- coding:utf-8 -*-

from Settings import *
import pygame
import ShoppingBox
from Scene import *
from Player import *
from NPC import *
from BattleBox import *
from Map import*
import random
from DialogBox import *
from Field import *

class SceneManager:
    def __init__(self, window, player,key):
        self.scene = MainMenuScene(window)
        self.state = GameState.MAIN_MENU
        self.window = window
        self.player = player
        self.pause = False
        self.battleBox = None
        self.player = player
        self.key = key
        self.has_planted=False

    def update_collide(self):
        # Player -> Obstacles
        ##### Your Code Here ↓ #####
        if pygame.sprite.spritecollide(self.player, self.scene.obstacles, False):
            self.player.rect = self.player.rect.move(-self.player.dx, -self.player.dy)
        if self.player.day > 1 :
            if pygame.sprite.spritecollide(self.player, self.player.fruits_planted, True):
                self.player.fruits += 1
                self.player.rect = self.player.rect.move(-self.player.dx, -self.player.dy)
        if pygame.sprite.spritecollide(self.player, self.scene.obstacles_w, False):
            self.player.rect = self.player.rect.move(-self.player.dx * 3, -self.player.dy * 3)
            self.player.coll_w = 1
        ##### Your Code Here ↑ #####
        if self.state != GameState.MAIN_MENU and self.state != GameState.README:
        #player -> Desk(friendlynpc1)
        ##### Your Code Here ↓ #####
            self.check_event_shopping(self.player)
            if pygame.sprite.spritecollide(self.player, self.scene.desks, False):
                self.player.rect = self.player.rect.move(-self.player.dx, -self.player.dy)            
        ##### Your Code Here ↑ #####
        #player -> Field(friendlynpc2)
        ##### Your Code Here ↓ #####
            self.check_event_planting(self.player)
            if pygame.sprite.spritecollide(self.player, self.scene.fields, False) and (self.player.day != 2):
                self.player.rect = self.player.rect.move(-self.player.dx, -self.player.dy)
        ##### Your Code Here ↑ #####
        #player -> Village Chief(friendlynpc3)
        ##### Your Code Here ↓ #####
            self.check_event_talking(self.player, self.key)
            if pygame.sprite.spritecollide(self.player, self.scene.npcs, False):
                self.player.rect = self.player.rect.move(-self.player.dx, -self.player.dy)
        ##### Your Code Here ↑ #####
            if self.state == GameState.GAME_PLAY_WILD:
        #player -> Monsters and Boss
        ##### Your Code Here ↓ #####
                self.check_event_battle(self.player, self.key)
        ##### Your Code Here ↑ #####        
       
        # Player -> Portals
        ##### Your Code Here ↓ #####
        if pygame.sprite.spritecollide(self.player, self.scene.portals, False, pygame.sprite.collide_mask):
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH))
        if pygame.sprite.spritecollide(self.player,self.scene.home,False,pygame.sprite.collide_mask):
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_HOME))
        if self.player.sleep >= 8 and self.player.sleep <= 12 and self.player.saciety >= 10 and self.player.saciety <= 20:
                if self.player.rect.x > 870 and self.state == GameState.GAME_PLAY_HOME:
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_HOME))
        ##### Your Code Here ↑ #####            
        # Player -> coins
        ##### Your Code Here ↓ #####
        if self.scene == README:
            self.pause = True
        if (self.player.sleep >= 8 and self.player.sleep <= 12 and self.player.saciety >= 10 and self.player.saciety <= 20) or (self.player.sleep > 12) or (self.player.saciety > 20):
            self.pause = True
        if self.player.sleep == 0:
            self.pause = False
        for coin in self.scene.coins.sprites():
            if self.player.rect.colliderect(coin.rect):
                coin.rect.y = 60
                coin.rect.x = random.randint(coin.a,coin.b)
                if not self.pause:
                    if self.scene.coins.sprites().index(coin) in [0,2,4]:
                        self.player.attr_update(addsleep = 1)
                    else:
                        self.player.attr_update(addsaciety = 1)
        ##### Your Code Here ↑ #####


    def check_event_battle(self, player, keys):
        if self.battleBox is None:
            self.player.isfighting = False
            if self.scene.monsters != None:
                for monster1 in self.scene.monsters.sprites():
                    if pygame.sprite.collide_rect(player, monster1):
                        if self.player.debris >= 300:
                            self.battleBox = BattleBox(self.window, player, monster1,monstertype = 1)
                        else:
                            self.battleBox = BattleBox(self.window, player, monster1,monstertype = 0)
                        self.battleBox.render()
                    if self.player.debris == 300 and self.player.day != 3:
                        monster1.kill()
        else:
            self.battleBox.render()
            self.player.isfighting = True
            self.player.speed= 0
            if self.battleBox.isFinished and keys[pygame.K_RETURN]:
                
                if self.player.HP == 0:
                    self.player.attr_update(addCoins = -10, addAttack = -3, addDefence = -3)
                else:
                    self.player.attr_update(adddebris = 50,addCoins = MonsterSettings.monsterCoin)
                    if self.battleBox.monstertype == 1:
                        self.player.day = 4
                self.battleBox = None

   
    def check_event_shopping(self, player):
        for desk in self.scene.desks.sprites():
            if desk.talking:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                        if event.key == pygame.K_UP:
                            self.scene.shoppingBox.selectedID = max(0, 
                                self.scene.shoppingBox.selectedID - 1)
                        elif event.key == pygame.K_DOWN:
                            self.scene.shoppingBox.selectedID = min(7, 
                                self.scene.shoppingBox.selectedID + 1)
                        elif event.key == pygame.K_RETURN:
                            if self.scene.shoppingBox.selectedID == 7:
                                desk.talking = False
                                desk.reset_talk_CD() 
                                player.talking = False
                                self.scene.shoppingBox = None
                            else:
                                self.scene.shoppingBox.buy() 
            if self.scene.shoppingBox is not None:    
                self.scene.shoppingBox.render()
            else:
                if pygame.sprite.collide_rect(desk, player):
                    desk.talking = True
                    player.talking = True
                    self.scene.shoppingBox = ShoppingBox.ShoppingBox(self.window, 
                        GamePath.desk, player, 
                        {"Attack +1": "         Coin -7", 
                        "Defence +1": "         Coin -7",
                        "HP +5": "              Coin -5", 
                        "Potion": "             Fruit - 4",
                        "CabbageSeed + 1":"     Coin - 3",
                        "WatermelonSeed + 1":"  Coin - 3",
                        "BroccoliSeed + 1":"    Coin - 3",
                        "Exit": ""})
                    self.scene.shoppingBox.render()


    def check_event_planting(self, player):
        if self.player.day == 1:
            for field in self.scene.fields.sprites():
                if field.talking:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                            if event.key == pygame.K_UP:
                                self.scene.shoppingBox.selectedID = max(0, 
                                    self.scene.shoppingBox.selectedID - 1)
                            elif event.key == pygame.K_DOWN:
                                self.scene.shoppingBox.selectedID = min(3, 
                                    self.scene.shoppingBox.selectedID + 1)
                            elif event.key == pygame.K_RETURN:
                                if self.scene.shoppingBox.selectedID == 3:
                                    field.talking = False
                                    field.reset_talk_CD() 
                                    player.talking = False
                                    self.scene.shoppingBox = None
                                else:
                                    if field.is_planted == False:
                                        self.scene.shoppingBox.plant(field)
                                        field.talking = False
                                        field.reset_talk_CD() 
                                        player.talking = False
                                        self.scene.shoppingBox = None
                                    elif field.is_planted:
                                        field.talking = False
                                        field.reset_talk_CD() 
                                        player.talking = False
                                        self.scene.shoppingBox = None
                if self.scene.shoppingBox is not None:    
                    self.scene.shoppingBox.render()
                elif pygame.sprite.collide_rect(field, player):
                    field.talking = True
                    player.talking = True

                    self.scene.shoppingBox = ShoppingBox.ShoppingBox(self.window, GamePath.shovel_ori, player, 
                {"Bury a CabbageSeed Here":"",
                "Bury a WatermelonSeed Here":"",
                "Bury a BroccoliSeed Here":"",
                "Exit":""})
                    self.scene.shoppingBox.render()
                if field.is_planted and self.has_planted == False:
                    if field.cabbage:
                        self.player.fruits_planted.add(Fruit(field, GamePath.cabbage))
                    elif field.watermelon:
                        self.player.fruits_planted.add(Fruit(field, GamePath.watermelon))
                    elif field.broccoli:
                        self.player.fruits_planted.add(Fruit(field, GamePath.broccoli))
                    self.has_planted = True

        elif self.player.day >1:
            for fruit in self.player.fruits_planted:
                    if pygame.sprite.collide_rect(fruit, self.player):
                        self.player.attr_update(addFruits = +1)
                        return


 

    def check_event_talking(self, player, keys):
        # check for all npcs
        for npc in self.scene.npcs.sprites():
            # 结束对话
            if npc.talking and keys[pygame.K_RETURN]:
                npc.talking = False
                player.talking = False
                npc.reset_talk_CD()
            if abs(player.rect.center[0]-npc.rect.center[0]) > 100 or abs(player.rect.center[1]-npc.rect.center[1]) > 100:
                npc.speed = NPCSettings.npcSpeed
            else:        
                npc.speed = 0
            # 保持对话
        if pygame.sprite.spritecollide(self.player, self.scene.npcs, False):
            for npc in self.scene.npcs.sprites():                
                npc.talking = True
        for npc in self.scene.npcs.sprites():    
            if  npc.talking == True:
                player.talking = True
                if player.day == 1:
                    dialogBoxTemp = DialogBox(self.window, GamePath.npc,
                            Font.npc_dialogue)
                elif player.day == 2:
                    dialogBoxTemp = DialogBox(self.window, GamePath.npc,
                                              Font.npc_dialogue2)
                else:
                    dialogBoxTemp = DialogBox(self.window, GamePath.npc,
                                              Font.npc_dialogue3)  
                dialogBoxTemp.render()

                


    def flush_scene(self, dest):
        if dest == GameState.GAME_PLAY_CITY:
            self.scene = CityScene(self.window)
        elif dest == GameState.GAME_PLAY_WILD:
            self.scene = WildScene(self.window, self.player)
        elif dest == GameState.GAME_PLAY_HOME:
            self.scene = HomeScene(self.window, self.player)
        elif dest == GameState.README:
            self.scene = README(self.window)
        self.state = dest
    

    def update(self):
        # update npc
        for each in self.scene.npcs.sprites():
            each.update()
        for each in self.scene.coins.sprites():
            each.update()
        for each in self.scene.monsters.sprites():
            each.update()
        for each in self.scene.obstacles_w.sprites():
            each.update()



    def render(self):
        self.scene.render()
        if self.player.day > 1:
            if self.state == GameState.GAME_PLAY_CITY:
                for fruit in self.player.fruits_planted:
                    Fruit.draw(fruit, self.window)



   
