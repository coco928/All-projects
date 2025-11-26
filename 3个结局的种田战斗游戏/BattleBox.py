# -*- coding:utf-8 -*-

from typing import *
from Settings import BattleSettings, GamePath, BgmPath
import pygame


class BattleBox:
    def __init__(self, window, player, monster, monstertype,fontSize: int = BattleSettings.textSize,
                 fontColor: Tuple[int, int, int] = (255, 255, 255),
                 bgColor: Tuple[int, int, int, int] = (255, 0, 0, BattleSettings.boxAlpha)):

        # 初始化窗口和字体
        self.window = window

        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(None, self.fontSize)
        self.bg = pygame.Surface((BattleSettings.boxWidth, BattleSettings.boxHeight), pygame.SRCALPHA)
        self.bg.fill(bgColor)

        # 初始化相关角色的参数，没有实际操作的权力
        self.player = player
        self.playerHP = player.HP
        self.playerImg = pygame.transform.scale(player.images[0], (BattleSettings.playerWidth, BattleSettings.playerHeight))
        self.playerX = BattleSettings.playerCoordX
        self.playerY = BattleSettings.playerCoordY
        self.monster = monster
        self.monsterHP = monster.HP
        self.monsterImg = pygame.transform.scale(monster.images[1],
                                                 (BattleSettings.monsterWidth, BattleSettings.monsterHeight))
        self.monsterX = BattleSettings.monsterCoordX
        self.monsterY = BattleSettings.monsterCoordY
        self.monsterCoin = monster.gold_coin
        # 默认玩家先手
        self.attacker = 0
        # 区分放动画状态和攻击结算状态
        self.isPlayingAnimation = True
        self.currentAnimationCount = 0
        # 移动方向
        self.dir = 1
        # 是否结束
        self.isFinished = False
        playerfightimage = [pygame.image.load(image) for image in GamePath.player_fight]
        self.monsterfightimage = [pygame.transform.scale(pygame.image.load(image),(BattleSettings.playerWidth*1.5+20,BattleSettings.playerHeight*1.5+30)) for image in GamePath.monster_fight]
        self.fight1_player = pygame.transform.scale(playerfightimage[0],(500, BattleSettings.monsterHeight))
        self.monstertype = monstertype
        self.index = 0



    def get_result(self):
        if self.attacker == 0:
            self.monsterHP = max(0, self.monsterHP -
                                 (self.player.attack - self.monster.Defense))
            self.attacker = 1
            self.dir = -1
        else:
            self.playerHP = max(0, self.playerHP -
                                (self.monster.Attack - self.player.defence))
            self.attacker = 0
            self.dir = 1

        self.isPlayingAnimation = True

    def render(self):
        # 绘制背景和文字
        self.monster.speed = 0
        self.window.blit(self.bg, (BattleSettings.boxStartX,
                                   BattleSettings.boxStartY))
        if self.monstertype == 0:
            if self.monsterX < BattleSettings.monsterCoordX:
                self.playerImg = pygame.transform.scale(self.player.images[0], (BattleSettings.playerWidth, BattleSettings.playerHeight))
            else:
                self.playerImg = pygame.transform.scale(self.player.images[1], (BattleSettings.playerWidth, BattleSettings.playerHeight))
        else:
            if self.playerX > BattleSettings.playerCoordX:
                self.playerImg = pygame.transform.scale(self.player.images[2], (BattleSettings.playerWidth, BattleSettings.playerHeight))
            else:
                self.playerImg = pygame.transform.scale(self.player.images[1], (BattleSettings.playerWidth, BattleSettings.playerHeight))
        self.window.blit(self.playerImg, (self.playerX,
                                          self.playerY))
        self.window.blit(self.monsterImg, (self.monsterX,
                                           self.monsterY))

        text = "player HP: " + str(self.playerHP)
        self.window.blit(self.font.render(text, True, self.fontColor),
                         (BattleSettings.textPlayerStartX, BattleSettings.textStartY-50))
        

        text = "monster HP: " + str(self.monsterHP)
        self.window.blit(self.font.render(text, True, self.fontColor),
                         (BattleSettings.textMonsterStartX, BattleSettings.textStartY-50))

        # 绘制战斗过程

        if self.isPlayingAnimation:
            if self.currentAnimationCount < BattleSettings.animationCount:
                currentDir = self.dir
            else:
                currentDir = self.dir * -1

            if self.attacker == 0:
                if self.monstertype == 0:
                    self.fight1_player = pygame.transform.flip(self.fight1_player, True, False)
                    self.window.blit(self.fight1_player, (self.monsterX - 100,
                                                          self.monsterY))
                else:
                    self.playerX += currentDir * BattleSettings.stepSpeed
                    self.fight1_player = pygame.transform.flip(self.fight1_player, True, False)
                    self.window.blit(self.fight1_player, (self.monsterX - 100,
                                                          self.monsterY))
                # --------------------------------------------------------------------------------------------------------------------
                Sound = pygame.mixer.Sound(BgmPath.BgmThunder)
                Sound.play(1, 1000)

            else:
                if self.monstertype == 0:
                    self.monsterX += currentDir * BattleSettings.stepSpeed
                    # ------------------------------------------------------------------------------------------------------
                    Sound2 = pygame.mixer.Sound(BgmPath.BgmYell)
                    Sound2.play(1, 1000)
                else:
                    self.index = (self.index + 1) % 3
                    self.window.blit(self.monsterfightimage[self.index], (self.playerX - 100,
                                                                          self.monsterY))
                    # -----------------------------------------------------------------------------------------------------
                    Sound3 = pygame.mixer.Sound(BgmPath.BgmFire)
                    Sound3.play(1, 1000)

            self.currentAnimationCount += 1

            if self.currentAnimationCount == BattleSettings.animationCount * 2:
                self.isPlayingAnimation = False
                self.currentAnimationCount = 0

        # 战斗判定以及结算

        elif not self.isFinished:
            self.get_result()

        if self.playerHP == 0 or self.monsterHP == 0:

            if self.monsterHP == 0:
                text = "WELL DONE!"
                self.window.blit(self.font.render(text, True, self.fontColor),
                                 (BattleSettings.textStartX + 230,
                                  BattleSettings.textStartY + BattleSettings.textVerticalDist))
                self.monster.kill()
                self.player.HP = self.playerHP
                

            if self.playerHP == 0:
                self.player.HP = self.playerHP
                text = "Oh no!"
                self.window.blit(self.font.render(text, True, self.fontColor),
                                 (BattleSettings.textStartX + 240,
                                 BattleSettings.textStartY + BattleSettings.textVerticalDist))
            self.isFinished = True
            self.isPlayingAnimation = False
