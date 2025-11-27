# -*- coding:utf-8 -*-

import pygame
import sys

from SceneManager import SceneManager
from Settings import *
from Player import Player


def run_game():
    pygame.init()

    window = pygame.display.set_mode((WindowSettings.width, WindowSettings.height))
    pygame.display.set_caption(WindowSettings.name)
    pygame.mixer.music.load(BgmPath.BgmMain)
    pygame.mixer.music.play(-1)

    # 创建角色 和 NPC 精灵
    player = Player(WindowSettings.width // 2, WindowSettings.height // 2)
    clock = pygame.time.Clock()
    sceneManager = SceneManager(window, player,None)
    index = 0
    # 游戏主循环
    while player.day <= 4:
        if (player.HP == 0) or ((player.debris < 300) and (player.day == 3)) or ((player.day == 4) and (player.potion == 0)):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.quit()
                        sys.exit()
            if index == 0:
                pygame.mixer.music.load(BgmPath.BgmLose)
                pygame.mixer.music.play(-1)
            index += 1
        if (player.day == 4) and (player.potion > 0) and (sceneManager.scene.index == 27):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.quit()
                        sys.exit()
        clock.tick(30)
        keys = pygame.key.get_pressed()
        sceneManager.key = keys
        
        if sceneManager.state == GameState.MAIN_MENU:
            sceneManager.render()
        elif sceneManager.state == GameState.README:
            sceneManager.render()
        else:
            # 更新 NPC / Player
            player.update(keys,sceneManager.state)    # 主要是角色移动
                # 主要是场景中对象的动画更新，暂时不涉及player的部分

            # talking 的render 必须要在scene render以后，不然会被背景盖掉
            sceneManager.render()    
            sceneManager.update()
            if player.day < 4:
                player.draw(window)
        sceneManager.update_collide()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 传送
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pressed()
                if sceneManager.state == GameState.GAME_PLAY_HOME:
                    if player.sleep > 12 or player.saciety > 20:
                        if mouse[2]:
                            player.saciety = 0
                            player.sleep = 0
                            sceneManager.flush_scene(GameState.GAME_PLAY_HOME)
                if mouse[0] and sceneManager.state == GameState.GAME_PLAY_HOME:
                    sceneManager.state == GameState.README
                    sceneManager.flush_scene(GameState.README)
                elif mouse[0] and sceneManager.state == GameState.README:
                    sceneManager.state == GameState.GAME_PLAY_HOME
                    sceneManager.flush_scene(GameState.GAME_PLAY_HOME)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN\
                and sceneManager.state == GameState.MAIN_MENU:
                    sceneManager.flush_scene(GameState.GAME_PLAY_CITY)
            if event.type == GameEvent.EVENT_SWITCH:
                if sceneManager.state == GameState.GAME_PLAY_CITY:
                    sceneManager.flush_scene(GameState.GAME_PLAY_WILD)
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(BgmPath.BgmWild)
                    pygame.mixer.music.play(-1)
                elif sceneManager.state == GameState.GAME_PLAY_WILD:
                    sceneManager.flush_scene(GameState.GAME_PLAY_CITY)
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(BgmPath.BgmMain)
                    pygame.mixer.music.play(-1)
                    player.rect.center = (640,360)
            if event.type == GameEvent.EVENT_HOME:
                if sceneManager.state == GameState.GAME_PLAY_CITY:
                    sceneManager.flush_scene(GameState.GAME_PLAY_HOME)
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(BgmPath.BgmHome)
                    pygame.mixer.music.play(-1)
                    player.rect.center =((HomeSettings.windowWidth//2 + 240,560))
                    player.sleep = 0
                    player.saciety = 0
                elif sceneManager.state == GameState.GAME_PLAY_HOME:
                    sceneManager.flush_scene(GameState.GAME_PLAY_CITY)
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(BgmPath.BgmMain)
                    pygame.mixer.music.play(-1)
                    player.rect.center = (640,360)
                    player.day += 1
                    player.HP += 10

        window.blit(pygame.font.Font(None,60).render("Day" + str(player.day),True,(255,255,255)),(0,0))    

        if player.HP == 0:
            lose = pygame.image.load(GamePath.end2)
            lose = pygame.transform.scale(lose, (1280,720))
            window.blit(lose, (0,0))
        if (player.debris < 300) and (player.day == 3):
            end3 = pygame.image.load(GamePath.end3)
            end3 = pygame.transform.scale(end3, (1280, 720))
            window.blit(end3, (0,0))
        pygame.display.flip()

if __name__ == "__main__":
    run_game()