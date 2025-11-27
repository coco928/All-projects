import pygame
import Map
from Settings import *
from NPC import *
from Portal import *
from Field import *
from Coinbox import *
from random import *


class Scene():
    def __init__(self, window):
        self.type = None
        self.map = None
        self.obstacles = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.home = pygame.sprite.Group()
        self.fields = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.desks = pygame.sprite.Group()
        self.window = window
        self.width = WindowSettings.width
        self.height = WindowSettings.height
        self.monsters = pygame.sprite.Group()
        # ------------------------------------------------------------------
        self.obstacles_w = pygame.sprite.Group()

        self.shoppingBox = None

        self.viewport_x = 1280
        self.viewport_y = 760

    def render(self):
        for i in range(SceneSettings.tileXnum):
            for j in range(SceneSettings.tileYnum):
                self.window.blit(self.map[i][j], 
                                 (SceneSettings.tileWidth * i, 
                                SceneSettings.tileHeight * j))
        self.monsters.draw(self.window)        
        self.obstacles.draw(self.window)
        self.npcs.draw(self.window)
        self.portals.draw(self.window)
        self.home.draw(self.window)
        self.fields.draw(self.window)
        self.desks.draw(self.window)
        # ------------------------------------------------------------
        self.obstacles_w.draw(self.window)

        for field in self.fields:
            if field.is_planted:
                Field.grow_plants(field, self.window)
        
        
class CityScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.type = SceneType.CITY
        self.map = Map.gen_city_map()
        self.obstacles = Map.gen_obstacles()
        self.desks.add(Desk(self.width//2-0.5*ShopSettings.deskWidth, self.height//5 - 100))
        self.npcs.add(NPC(self.width // 3, self.height // 3))
        self.portals.add(Portal(self.width // 11 , self.height // 3 * 1.8 ))
        self.home.add(Home(self.width // 4 * 3,self.height // 3))

        self.fields.add (Field(WindowSettings.width//5-100,WindowSettings.height // 9,self),
        Field(WindowSettings.width//5 + SceneSettings.tileWidth*2-100, WindowSettings.height // 9 + SceneSettings.tileHeight*2,self),
        Field(WindowSettings.width//5 - 200 , WindowSettings.height // 9 + SceneSettings.tileHeight*2,self),
        Field(WindowSettings.width//5 + SceneSettings.tileWidth*2 , WindowSettings.height // 9 ,self)
        )


class WildScene(Scene):
    def __init__(self, window,player):
        super().__init__(window)
        self.type = SceneType.WILD
        self.player = player
        self.map = Map.gen_wild_map()
        self.portal=Portal(self.width // 11, -self.height // 6)
        self.portals.add(self.portal)
        self.font = pygame.font.Font(None, WildSettings.testSize)
        # --------------------------------------------------------------------------------------------------
        self.obstacles_w = Map.get_obstacles(self.player.day)
        if self.player.debris < 300:
            self.type = Map.get_monster("monster")
            for each in self.type:
                self.monsters.add(each)
        else:
            if self.player.day == 3:
                self.type = Boss(self.portal.rect.center[0]+500,self.portal.rect.center[1] + 600,self.portal.rect.center[0],self.portal.rect.center[1])
            self.monsters.add(self.type)
        self.x = 0
        self.y = 0
        self.index = 0
        # ---------------------------------------------------------------------------------------------------
        self.th = 0

    def render(self):
        keys = pygame.key.get_pressed()
        # ----------------------------------------------------------------------------------------------
        if self.player.coll_w != 0:
            self.th += 1
        else:
            if keys[pygame.K_UP]:
                self.y += self.player.speed
            if keys[pygame.K_DOWN]:
                self.y -= self.player.speed
            if keys[pygame.K_LEFT]:
                self.x += self.player.speed
            if keys[pygame.K_RIGHT]:
                self.x -= self.player.speed
            for each in self.monsters:
                if keys[pygame.K_UP]:
                    each.rect.y += self.player.speed
                    if self.player.debris < 300:
                        each.initialPosition += self.player.speed
                    else:
                        each.centery += self.player.speed
                if keys[pygame.K_DOWN]:
                    each.rect.y -= self.player.speed
                    if self.player.debris < 300:
                        each.initialPosition -= self.player.speed
                    else:
                        each.centery -= self.player.speed
                if keys[pygame.K_LEFT]:
                    each.rect.x += self.player.speed
                    if self.player.debris >= 300:
                        each.centerx += self.player.speed
                if keys[pygame.K_RIGHT]:
                    each.rect.x -= self.player.speed
                    if self.player.debris >= 300:
                        each.centerx -= self.player.speed
            
            for each in self.portals:
                if keys[pygame.K_UP]:
                    each.rect.y += self.player.speed
                if keys[pygame.K_DOWN]:
                    each.rect.y -= self.player.speed
                if keys[pygame.K_LEFT]:
                    each.rect.x += self.player.speed
                if keys[pygame.K_RIGHT]:
                    each.rect.x -= self.player.speed
#               ----------------------------------------------------------
            for each in self.obstacles_w:
                if keys[pygame.K_UP] :
                    each.rect.y += self.player.speed
                if keys[pygame.K_DOWN] :
                    each.rect.y -= self.player.speed
                if keys[pygame.K_LEFT] :
                    each.rect.x += self.player.speed
                if keys[pygame.K_RIGHT] :
                    each.rect.x -= self.player.speed

        for i in range(4 * SceneSettings.tileXnum):
            for j in range(4 * SceneSettings.tileYnum):
                self.window.blit(self.map[i][j],(SceneSettings.tileWidth * (i-2*SceneSettings.tileXnum)+self.x,
                        SceneSettings.tileHeight * (j-2*SceneSettings.tileYnum)+self.y))
        if -900 <= (self.player.rect.x - self.portal.rect.center[0]) <= 1300 and\
            -410 < (self.player.rect.y-self.portal.rect.center[1]) <= 700:
            self.player.speed = 5
        else:
            self.player.speed = 0
            if keys[pygame.K_RETURN]:
                self.player.rect.center= (320, 500)
                self.portal.rect.topleft = (self.portal.x,self.portal.y)
                for each in self.monsters:
                    each.rect.topleft =(each.x,each.y)
                    each.initialPosition = each.y
                # =--------------------------------------------------
                self.obstacles_w = Map.get_obstacles(self.player.day)
                self.x = 0
                self.y = 0
            else:
                self.window.blit(self.font.render("you have reached the end and stuck by the wall", True, (225, 0, 0)),(375,300))
                self.window.blit(self.font.render("press ENTER to get back to where you start...", True, (225, 0, 0)),(380,330))

        self.monsters.draw(self.window)
        self.portals.draw(self.window)
        # ------------------------------------------------------------------------------------------------------------
        self.obstacles_w.draw(self.window)
        PlayerCoin = self.player.money
        PlayerDebris = self.player.debris
        PlayerHp = self.player.HP
        text1 = self.font.render(f"Debris = {PlayerDebris}", True, (225, 225, 0))
        text2 = self.font.render(f"Money = {PlayerCoin}", True, (225, 225, 0))
        text0 = self.font.render(f"Hp = {PlayerHp}", True, (225, 225, 0))
        text3 = self.font.render(f"Attack = {self.player.attack}", True,(225,225,0))
        text4 = self.font.render(f"Defence = {self.player.defence}", True, (225,225,0))
        self.window.blit(text0, (795, 30))
        self.window.blit(text1, (940, 30))
        self.window.blit(text2, (1100, 30))
        self.window.blit(text3, (450, 30))
        self.window.blit(text4, (600, 30))
        # ------------------------------------------------------------------------------------------------------------
        if self.th == 6:
            self.player.coll_w = 0
            self.th = 0



        if (self.player.day == 4) and (self.player.potion > 0):
            end1 = [pygame.transform.scale(pygame.image.load(end),(1280,720)) for end in GamePath.end1]
            self.window.blit(end1[self.index],(0,0))
            if self.index < len(end1) :
                self.index+= 1
            elif self.index == len(end1):
                self.index = len(end1)
            pygame.time.wait(400)
        elif (self.player.day == 4) and (self.player.potion == 0):
            end4 = pygame.image.load(GamePath.end4)
            end4 = pygame.transform.scale(end4, (1280, 720))
            self.window.blit(end4, (0, 0))


class HomeScene(Scene):
    def __init__(self, window,player):
        super().__init__(window)
        self.type = SceneType.HOME
        bg = pygame.image.load(GamePath.home_bg)
        self.player = player
        self.bg = pygame.transform.scale(bg,(800,600)) 
        self.coins.add(Coin(250,60+randint(0,200),10,0,290,490),Coin(360,60+randint(0,200),6,1,340,610),Coin(470,60+randint(0,200),7,0,560,710),Coin(580,60+randint(0,200),8,1,660,810),Coin(690,60+randint(0,200),9,0,760,990),Coin(800,60+randint(0,200),5,1,340,740))
        self.door_index = 0
        self.doors = [pygame.transform.scale(pygame.image.load(door),(800,600)) for door in GamePath.doors]
    
    def render(self):
        self.window.blit(self.bg,(240,60))
        self.coins.draw(self.window)
        self.window.blit(Font.a_surface,(490,610))
        a = Coinbox(self.window,self.player,self)
        a.score_update()
        if self.player.sleep >= 8 and self.player.sleep <= 12 and self.player.saciety >= 10 and self.player.saciety <= 20:
            if self.door_index < 15:
                self.door_index += 1
            else:
                self.door_index = 15            
            self.window.blit(self.doors[self.door_index],(240,60))      
        if self.player.sleep == 0 and self.player.saciety == 0:
            a.reset()


class MainMenuScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.bg = pygame.image.load(GamePath.menu)
        self.bg = pygame.transform.scale(self.bg, 
                (WindowSettings.width, WindowSettings.height))
        
        self.font = pygame.font.Font(None, MenuSettings.textSize)
        self.text = self.font.render("Press ENTER to start",
                                True, (255, 255, 255))
        self.textRect = self.text.get_rect(center=(WindowSettings.width // 2, 
                                WindowSettings.height - 50))
        
        self.blinkTimer = 0
        
    def render(self):
        self.window.blit(self.bg, (0, 0))
        
        self.blinkTimer += 1
        if self.blinkTimer >= MenuSettings.blinkInterval:
            self.window.blit(self.text, self.textRect)
            if self.blinkTimer >= MenuSettings.blinkInterval * 2:
                self.blinkTimer = 0

class README(Scene):
    def __init__(self, window):
        super().__init__(window)        
        self.coin = pygame.image.load(GamePath.food)
        self.coin1 = pygame.image.load(GamePath.food1)

    def render(self):    
        self.window.fill((0,0,0))
        self.window.blit(Font.title_surface,(610,110))
        self.window.blit(Font.notice_surface,(270,170))
        self.window.blit(Font.notice1_surface,(270,220))
        self.window.blit(Font.notice2_surface,(270,270))
        self.window.blit(Font.notice3_surface,(270,320))
        self.window.blit(Font.b_surface,(390,560))
        self.window.blit(pygame.transform.scale(self.coin,(60,60)),(440,380))
        self.window.blit(Font.notice4_surface,(510,400))
        self.window.blit(pygame.transform.scale(self.coin1,(90,60)),(420,450))
        self.window.blit(Font.notice5_surface,(510,460))


