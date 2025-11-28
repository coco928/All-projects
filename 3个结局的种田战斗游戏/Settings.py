
# -*- coding:utf-8 -*-

from enum import Enum
import pygame

pygame.init()

days = 1

class WindowSettings:
    name = "BunnyKillsMommy"
    width = 1280
    height = 720
    outdoorScale = 1.5 # A necessary scale to allow camera movement in outdoor scenes

class PlayerSettings:
    playerSpeed = 5
    playerWidth = 50
    playerHeight = 75
    playerHP = 20
    playerAttack = 5
    playerDefence = 1
    playerMoney = 100
    playerPotion = 0
    playerCabbage = 0
    playerWatermelon = 0
    playerBroccoli = 0
    playersleep = 0
    playersaciety = 0
    playerDebris = 0
    playerFruits = 0

class NPCSettings:
    npcSpeed = 1
    npcWidth = 100
    npcHeight = 100
    talkCD = 30           # 1s

class MonsterSettings:
    monsterWidth = 100
    monsterHeight = 120
    monsterHP = 10
    monsterAttack = 3
    monsterDefense = 1
    monsterspeed = 2
    monsterCoin = 7


class SceneSettings:
    tileXnum = 36
    tileYnum = 18
    tileWidth = tileHeight = 40
    obstacleDensity = 0.2
    shovelWidth = 80
    shovelHeight = 90
    seedWidth = 30
    seedHeight = 40


class FieldSettings:
    fruitWidth = 78
    fruitHeight = 78

class SceneType(Enum):
    CITY = 1
    WILD = 2
    HOME = 3

class Font:
    #home related font
    win_font = pygame.font.Font(None,60)
    win_surface = win_font.render("You have got enough sleep and food!",True,(3,168,158))
    win1_surface = win_font.render("Please go out to have a nice day!",True,(3,168,158))
    title_font = pygame.font.Font(None,50)
    title_surface = title_font.render("Notice",True,(255,255,255))
    notice_font = pygame.font.Font(None,40)
    notice_surface = notice_font.render("you should get enough sleep but don't sleep too much",True,(255,255,255))
    notice1_surface = notice_font.render("suitable scale for sleep:[8,12]",True,(255,255,255))
    notice2_surface = notice_font.render("you should have enough food but don't eat too much",True,(255,255,255))
    notice3_surface = notice_font.render("suitable scale for satiety:[10,20]",True,(255,255,255))    
    notice4_surface = notice_font.render("represents food for eating",True,(255,255,255))
    notice5_surface = notice_font.render("represents time for sleeping",True,(255,255,255))
    a_surface = notice_font.render("Click to see the rule",True,(0,0,0))
    warn1_font = pygame.font.Font(None,60)
    warn1_surface = warn1_font.render("You've eaten too much!",True,(255,0,0))
    warn2_surface = warn1_font.render("You've slept too much!",True,(255,0,0))
    warn3_surface = warn1_font.render("Click the right mouse button to try again!",True,(255,0,0))
    b_surface = notice_font.render("Click to get back to the game",True,(255,255,255))
    npc_dialogue = ["Thank god you're finally awake!!",
                    "You don't know me? All right.. ",
                    "I'm the village chief here. Oh, in case you don't know, you're at the The Great Great Town.",
                    "Lately our beautiful town has been attacked by an unknown mysterious force!",
                    "Some terrible creatures underground destroyed our water supply...",
                    "And we only have 3 days to save the town..."
                    "Can you help us? You just need to do what I tell you.",
                    "the first thing you should do is kill 3 monsters underground, and you can earn the coins.",
                    "These coins can be exchanged for seeds on the shopping desk,"
                    "and you can plant them in the vegetable field.",
                    "They will absorb some of the polluted water sources.",
                    "Please take action now and finish today! ",
                    "After doing these, You can go home to welcome the arrival of the next day."
                    # "Go underground and kill those bad ass, then you can earn money and some Debris.",
                    ]
    npc_dialogue2 = ["Hello! Maybe you did a great job yesterday?",
                     "If so, you can go harvest the fruit now. But these contaminated plants cannot be used to eat.",
                     "Because the water is polluted, I'm so sorry about that but you can't plant any plants today...",
                     "Perhaps you can find other uses for it in the shopping desk……",
                     "And don't forget kill monsters underground.",
                     "Perhaps you have already discovered that you obtained many debris after killing the monster.",
                     "If you want to Eliminate the Source of Water Pollution, you need to have 300 debris at least.",
                     "Only in this way will the Boss appear underground the next day.",
                     "By the way, don't forget to improve your attributes on the shopping desk. ",
                     "Boss is much stronger than ordinary monsters!"
                     ]
    npc_dialogue3 = ["Check your attributes and go fight against the monsters!",
                     "Looking forward to hearing your good news!"]
    
class DialogSettings:
    boxWidth = 950
    boxHeight = 230
    boxAlpha = 150
    boxStartX = WindowSettings.width // 4-100           # Coordinate X of the box
    boxStartY = WindowSettings.height // 3 * 2 -180 # Coordinate Y of the box

    textSize = 25 # Default font size
    textStartX = boxStartX + 20         # Coordinate X of the first line of dialog
    textStartY = boxStartY + 10    # Coordinate Y of the first line of dialog
    textVerticalDist = textSize // 4 * 3                # Vertical distance of two lines

    npcWidth = WindowSettings.width // 5
    npcHeight = WindowSettings.height // 3
    npcCoordX = 0
    npcCoordY = WindowSettings.height * 2 // 3 - 20

class BattleSettings:
    boxWidth = WindowSettings.width * 3 // 4 
    boxHeight = WindowSettings.height * 3 // 4 
    boxAlpha = 200
    boxStartX = WindowSettings.width // 8           # Coordinate X of the box
    boxStartY = WindowSettings.height // 8
    textSize = 48 # Default font size
    textStartX = WindowSettings.width // 4 
    textPlayerStartX = WindowSettings.width // 4          # Coordinate X of the first line of dialog
    textMonsterStartX = WindowSettings.width // 2 +100   
    textStartY = WindowSettings.height // 3         # Coordinate Y of the first line of dialog
    textVerticalDist = textSize // 4 * 3            # Vertical distance of two lines

    playerWidth = WindowSettings.width // 7
    playerHeight = WindowSettings.height // 3
    playerCoordX = WindowSettings.width // 8 +110
    playerCoordY = WindowSettings.height // 2

    monsterWidth = WindowSettings.width // 4
    monsterHeight = WindowSettings.height // 2
    monsterCoordX = WindowSettings.width * 5 // 8
    monsterCoordY = WindowSettings.height // 2 -120

    
    animationCount = 15

    stepSpeed = 20

class ShopSettings:
    deskWidth = 200
    deskHeight = 90

    goodsSize = 36
    textVerticalDist = goodsSize // 4 * 3

    boxWidth = 900
    boxHeight = 350
    boxStartX = WindowSettings.width // 4-125    # Coordinate X of the box
    boxStartY = WindowSettings.height // 3-50  # Coordinate Y of the box

    textSize = 56 # Default font size
    textStartX = boxStartX          # Coordinate X of the first line of dialog
    textStartY = boxStartY + 30    # Coordinate Y of the first line of dialog

class PortalSettings:
    portalWidth = 200
    portalHeight = 350

class WildSettings:
    testSize = 36

class HomeSettings:

    windowWidth = 800
    windowHeight = 600
    width = 800
    height = 600

class MenuSettings:
    textSize = 36
    blinkInterval = 15

class GamePath:
    # player/npc related path
    player = [r".\assets\player\bunny1_ready.png",
              r".\assets\player\bunny1_walk2.png",
              r".\assets\player\bunny1_walk1.png"]
    player_state = [r".\assets\player\bunny1_walk2.png",r".\assets\player\bunny1_walk2.png",r".\assets\player\bunny1_walk2.png",r".\assets\player\bunny1_walk1.png",r".\assets\player\bunny1_walk1.png",r".\assets\player\bunny1_walk1.png"]#walking
    npc =r".\assets\npc\chief_standing.png"
    monster = [r".\assets\monster\monster1.png",r".\assets\monster\monster2.png",r".\assets\monster\monster3.png"]
    player_fight = [r".\assets\player\fight1.png"]
    monster_fight = [r".\assets\player\fight2.png",r".\assets\player\fight3.png",r".\assets\player\fight4.png"]
    groundTiles = [
        r".\assets\tiles\ground1.png", 
        r".\assets\tiles\ground2.png", 
        r".\assets\tiles\ground3.png", 
        r".\assets\tiles\ground4.png", 
        r".\assets\tiles\ground5.png", 
        r".\assets\tiles\ground6.png", 
    ]
    
    cityTiles = [
        r".\assets\tiles\Grass1.png", 
        r".\assets\tiles\Grass2.png", 
        r".\assets\tiles\Grass3.png", 
        r".\assets\tiles\Grass4.png"
    ]

    tree = r".\assets\tiles\tree.png"
    box = r".\assets\tiles\box.png"

    portal = r".\assets\others\well_and_ladder.png"
    home = r".\assets\others\home.png"

    home_bg = r".\assets\home\bg4.jpg"

    menu = r".\assets\others\menu.png"

    food = r".\assets\home\sleep.png"
    food1 = r".\assets\home\sleep1.png"
    
    doors = [r".\assets\door\1.png",
             r".\assets\door\1.png",
             r".\assets\door\1.png",
             r".\assets\door\2.png",
             r".\assets\door\2.png",
             r".\assets\door\2.png",
             r".\assets\door\3.png",
             r".\assets\door\3.png",
             r".\assets\door\3.png",
             r".\assets\door\4.png",
             r".\assets\door\4.png",
             r".\assets\door\4.png",
             r".\assets\door\5.png",
             r".\assets\door\5.png",
             r".\assets\door\5.png",
             r".\assets\door\6.png"]
    
    field = r".\assets\tiles\field.png"
    shovel_ori = r".\assets\others\shovel.png"
    desk = r".\assets\others\desk.png"
    seed = r".\assets\tiles\seed.png"
    boss = [r".\assets\monster\boss1.png",
            r".\assets\monster\boss2.png",
            r".\assets\monster\boss3.png",
            r".\assets\monster\boss4.png"]
    
    cabbage = r".\assets\others\cabbage.png"
    watermelon = r".\assets\others\watermelon.png"
    broccoli = r".\assets\others\broccoli.png"
    
    shovel_flipped = pygame.transform.flip(pygame.transform.scale(pygame.image.load(shovel_ori), 
                            (SceneSettings.shovelWidth, SceneSettings.shovelHeight)),True,False)
    shovel = pygame.image.load(shovel_ori)
    shovel = pygame.transform.scale(shovel,(SceneSettings.shovelWidth, SceneSettings.shovelHeight))
    shovel_iamges = [shovel,shovel,shovel,shovel,shovel,shovel,shovel,shovel,
                    shovel_flipped,shovel_flipped,shovel_flipped,shovel_flipped,shovel_flipped,shovel_flipped,shovel_flipped,shovel_flipped,
                    shovel,shovel,shovel,shovel,shovel,shovel,shovel,shovel,
                    shovel_flipped,shovel_flipped,shovel_flipped,shovel_flipped,shovel_flipped,shovel_flipped,shovel_flipped,shovel_flipped,
                    shovel,shovel,shovel,shovel,]

    end1 = [r".\assets\end\end00.png",    #end1一共28张, 一张重复20次
            r".\assets\end\end01.png",    #end1也就是正常的结局,bunny & mommy 杀了村民和村长
            r".\assets\end\end02.png",
            r".\assets\end\end03.png",
            r".\assets\end\end05.png",
            r".\assets\end\end06.png",
            r".\assets\end\end07.png",
            r".\assets\end\end08.png",
            r".\assets\end\end09.png",
            r".\assets\end\end10.png",
            r".\assets\end\end11.png",
            r".\assets\end\end12.png",
            r".\assets\end\end13.png",
            r".\assets\end\end14.png",
            r".\assets\end\end15.png",
            r".\assets\end\end16.png",
            r".\assets\end\end17.png",
            r".\assets\end\end18.png",
            r".\assets\end\end19.png",
            r".\assets\end\end20.png",
            r".\assets\end\end21.png",
            r".\assets\end\end22.png",
            r".\assets\end\end23.png",
            r".\assets\end\end24.png",
            r".\assets\end\end25.png",
            r".\assets\end\end26.png",
            r".\assets\end\end27.png",
            r".\assets\end\end28.png"]
    end2 = r".\assets\end\lose.png"
    end3 = r".\assets\end\NOBOSS.png"
    end4 = r".\assets\end\BADEND.png"

class BgmPath:
    BgmMain = r".\assets\bgm\K.K.House.ogg"
    BgmHome = r".\assets\bgm\Prelude.ogg"
    BgmWild = r".\assets\bgm\Chaos.ogg"
    BgmLose = r".\assets\bgm\the_spring_lullaby.ogg"
    BgmThunder = r".\assets\bgm\thunder.wav"
    BgmYell = r".\assets\bgm\yell.mp3"
    BgmFire = r".\assets\bgm\fire.wav"


class GameState(Enum):
    MAIN_MENU = 1
    GAME_TRANSITION = 2
    GAME_OVER = 3
    GAME_WIN = 4
    GAME_PAUSE = 5
    GAME_PLAY_WILD = 6
    GAME_PLAY_CITY = 7
    GAME_PLAY_BOSS = 8
    GAME_PLAY_HOME = 9
    README = 10

class GameEvent:
    EVENT_BATTLE = pygame.USEREVENT + 1
    EVENT_DIALOG = pygame.USEREVENT + 2
    EVENT_SWITCH = pygame.USEREVENT + 3
    EVENT_RESTART = pygame.USEREVENT + 4
    EVENT_SHOP = pygame.USEREVENT + 5
    EVENT_HOME = pygame.USEREVENT + 6