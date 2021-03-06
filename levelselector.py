import pygame
from functions import miniConvert
from game import Game
from json_manipulation import deleteLevel
from convert import convertShortTime
import json

pygame.init()


def levelSelector():
    jeu = Game()
    pygame.font.init()

    blocks = [
        pygame.image.load("templates/templatesmini/brick.png"),
        pygame.image.load("templates/templatesmini/snow.png"),
        pygame.image.load("templates/templatesmini/finishflag.png"),
        pygame.image.load("templates/templatesmini/start.png"),
        pygame.image.load("templates/templatesmini/lava.png"),
    ]
    bumpers = [
        pygame.image.load("templates/templatesmini/ArrowUp.png"),
        pygame.image.load("templates/templatesmini/ArrowDown.png"),
        pygame.image.load("templates/templatesmini/ArrowLeft.png"),
        pygame.image.load("templates/templatesmini/ArrowRight.png"),
        pygame.image.load("templates/templatesmini/Levier.png"),
    ]
    switchers = [
        pygame.image.load("templates/templatesmini/SwitcherLR.png"),
        pygame.image.load("templates/templatesmini/SwitcherUD.png"),
        pygame.image.load("templates/templatesmini/leverOff.png"),
        pygame.image.load("templates/templatesmini/leverOn.png"),
    ]

    class listLevels:
        nbrNormalLevels = 0
        nbrPersoLevels = 0

        def __init__(self, name, level, record, typelevel, i):
            self.name = name
            self.level = level
            self.x = 100
            self.i = i
            self.wr = record
            self.font = pygame.font.Font("fonts/PixelOperatorMono8-Bold.ttf", 16)
            if typelevel == "normal":
                self.y = 50 + 150 * listLevels.nbrNormalLevels
                self.typeLevel = "normal"
                listLevels.nbrNormalLevels += 1
            if typelevel == "perso":
                self.y = 50 + 150 * listLevels.nbrPersoLevels
                self.typeLevel = "perso"
                listLevels.nbrPersoLevels += 1

        def show(self, fen, buttons):
            for col in range(15):
                for lig in range(15):
                    x, y = miniConvert(lig, col)
                    if self.level[lig][col] == 0:
                        pygame.draw.rect(
                            fen, (0, 0, 0), (self.x + x, self.y + y, 10, 10)
                        )
                    if self.level[lig][col] == 1:
                        fen.blit(blocks[0], (self.x + x, self.y + y))
                    if self.level[lig][col] == 2:
                        fen.blit(blocks[3], (self.x + x, self.y + y))
                    if self.level[lig][col] == 3:
                        fen.blit(blocks[2], (self.x + x, self.y + y))
                    if self.level[lig][col] == 4:
                        fen.blit(blocks[1], (self.x + x, self.y + y))
                    if self.level[lig][col] == 5:
                        fen.blit(blocks[4], (self.x + x, self.y + y))
                    if self.level[lig][col] == 6:
                        fen.blit(bumpers[0], (self.x + x, self.y + y))
                    if self.level[lig][col] == 7:
                        fen.blit(bumpers[1], (self.x + x, self.y + y))
                    if self.level[lig][col] == 8:
                        fen.blit(bumpers[2], (self.x + x, self.y + y))
                    if self.level[lig][col] == 9:
                        fen.blit(bumpers[3], (self.x + x, self.y + y))
                    if self.level[lig][col] == 10:
                        fen.blit(bumpers[4], (self.x + x, self.y + y))
                    if self.level[lig][col] == 11:
                        fen.blit(switchers[0], (self.x + x, self.y + y))
                    if self.level[lig][col] == 12:
                        fen.blit(switchers[1], (self.x + x, self.y + y))
                    if self.level[lig][col] == 13:
                        fen.blit(switchers[2], (self.x + x, self.y + y))
                    if self.level[lig][col] == 14:
                        fen.blit(switchers[3], (self.x + x, self.y + y))
            pygame.draw.rect(fen, (255, 255, 255), (self.x, self.y, 400, 150), 1)
            pygame.draw.rect(fen, (255, 255, 255), (self.x, self.y, 150, 150), 1)

            if buttons:
                fen.blit(buttons[6], (self.x + 150, self.y + 100))
                fen.blit(buttons[5], (self.x + 350, self.y + 100))
            textname = self.font.render(self.name, True, (255, 255, 255))
            fen.blit(textname, (self.x + 275 - (8 * len(self.name)), self.y + 60))

            recordText = self.font.render(
                "WR : {}".format(convertShortTime(self.wr)), True, (245, 176, 65)
            )
            if self.typeLevel == "normal":
                fen.blit(recordText, (self.x + 165, self.y + 120))
            else:
                fen.blit(recordText, (self.x + 165, self.y + 80))

    def scroll(dir, levels):
        for lvl in levels:
            lvl.y += dir

    def show(fen, imgs, status):
        pygame.draw.rect(fen, (0, 0, 0), (0, 0, 600, 50))
        fen.blit(imgs[4], (550, 550))
        if status == "normal":
            fen.blit(imgs[1], (0, 0))
            fen.blit(imgs[2], (300, 0))
        if status == "perso":
            fen.blit(imgs[0], (0, 0))
            fen.blit(imgs[3], (300, 0))

    win = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    pygame.display.set_caption("SLIDE - Level Selector")

    scrollspeed = 20
    buttons = [
        pygame.image.load("menuframes/normallevel.png"),
        pygame.image.load("menuframes/normallevel_selected.png"),
        pygame.image.load("menuframes/editorlevel.png"),
        pygame.image.load("menuframes/editorlevel_selected.png"),
        pygame.image.load("MenuFrames/editor_exit.png"),
        pygame.image.load("MenuFrames/trash.png"),
        pygame.image.load("MenuFrames/edit.png"),
    ]
    listNormalLevel = []
    listPersoLevel = []
    actualLevelDisplay = "normal"

    with open("level_data/normal_level.json") as f:
        normal_levels = json.load(f)
    i = 0
    for data in normal_levels:
        if data["level_name"] != "pattern" and data["level_name"] != "Secret Level":
            listNormalLevel.append(
                listLevels(
                    data["level_name"],
                    data["level_composition"],
                    data["WR"],
                    "normal",
                    i,
                )
            )
        i += 1

    with open("level_data/editor_level.json") as f:
        editor_levels = json.load(f)
    i = 0
    for data in editor_levels:
        if data["level_name"] != "pattern":
            listPersoLevel.append(
                listLevels(
                    data["level_name"],
                    data["level_composition"],
                    data["WR"],
                    "perso",
                    i,
                )
            )
        i += 1

    levelselector = True
    while levelselector:
        win.fill((0, 0, 0))
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                levelselector = False
                return

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and event.pos[0] > 0
                and event.pos[0] < 300
                and event.pos[1] > 0
                and event.pos[1] < 50
            ):
                actualLevelDisplay = "normal"

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and event.pos[0] > 300
                and event.pos[0] < 600
                and event.pos[1] > 0
                and event.pos[1] < 50
            ):
                actualLevelDisplay = "perso"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if actualLevelDisplay == "normal":
                        if listNormalLevel[0].y < 50:
                            scroll(scrollspeed, listNormalLevel)
                    elif actualLevelDisplay == "perso":
                        if len(listPersoLevel) > 0 and listPersoLevel[0].y < 50:
                            scroll(scrollspeed, listPersoLevel)
                elif event.button == 5:
                    if actualLevelDisplay == "normal":
                        if listNormalLevel[-1].y > 450:
                            scroll(-scrollspeed, listNormalLevel)
                    elif actualLevelDisplay == "perso":
                        if len(listPersoLevel) > 0 and listPersoLevel[-1].y > 450:
                            scroll(-scrollspeed, listPersoLevel)

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and event.pos[0] > 100
                and event.pos[0] < 500
                and event.pos[1] > 50
                and event.pos[1] < 600
            ):
                if actualLevelDisplay == "normal":
                    for lvl in listNormalLevel:
                        if event.pos[1] > lvl.y and event.pos[1] < lvl.y + 150:
                            jeu.level = lvl.level
                            jeu.testLevel()
                if actualLevelDisplay == "perso":
                    for lvl in listPersoLevel:
                        if event.pos[1] > lvl.y and event.pos[1] < lvl.y + 150:
                            if event.pos[0] > 450 and event.pos[1] > lvl.y + 100:
                                listPersoLevel = deleteLevel(listPersoLevel, lvl.i)
                            elif (
                                event.pos[0] > 250
                                and event.pos[0] < 300
                                and event.pos[1] > lvl.y + 100
                            ):
                                jeu.level = lvl.level
                                jeu.runEditor()
                            else:
                                jeu.level = lvl.level
                                jeu.testLevel("editor")

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and event.pos[0] > 550
                and event.pos[0] < 600
                and event.pos[1] > 550
                and event.pos[1] < 600
            ):
                levelselector = False
                return

        if actualLevelDisplay == "normal":
            for lvl in listNormalLevel:
                lvl.show(win, None)
        elif actualLevelDisplay == "perso":
            for lvl in listPersoLevel:
                lvl.show(win, buttons)
        show(win, buttons, actualLevelDisplay)
        pygame.display.update()


if __name__ == "__main__":
    levelSelector()
