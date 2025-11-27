
import pygame
from Settings import*
import Scene

class Coinbox():
    def __init__(self, window, player,scene):
        self.window = window
        self.player = player
        self.pause = False
        self.scene = scene

    def score_update(self):
        if self.scene == Scene.README:
            self.pause = True
        if self.player.sleep >= 8 and self.player.sleep <= 12 and self.player.saciety >= 10 and self.player.saciety <= 20:
            self.window.blit(Font.win_surface,(280,190))
            self.window.blit(Font.win1_surface,(310,240))
            self.pause = True
        if self.player.sleep > 12 :
            self.window.blit(Font.warn1_surface,(390,160))
            self.window.blit(Font.warn3_surface,(230,210))
            self.pause = True
        if self.player.saciety > 20:
            self.window.blit(Font.warn2_surface,(390,160))
            self.window.blit(Font.warn3_surface,(230,210))
            self.pause = True
        score_font = pygame.font.Font(None,30)
        self.score_surface = score_font.render("satiety %s" % self.player.saciety,True,(0,0,0))
        self.score1_surface = score_font.render("sleep %s" % self.player.sleep,True,(0,0,0))
        self.window.blit(self.score_surface,(250,65))
        self.window.blit(self.score1_surface,(250,90))    

    def reset(self):
        self.pause = False