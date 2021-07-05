import pygame
import random

colors = [(50,168,82), (173,247,19), (119,37,253), (117,182,240), (243,135,90)]

class UnmadeLogo(pygame.sprite.Sprite):

    def __init__(self, pos, screen):
        super().__init__()
        self.screen = screen
        self.pos = pos
        self.image = pygame.Surface((200 , 200), pygame.SRCALPHA)
        self.logo = pygame.image.load("unmade.png")
        self.image.blit(self.logo, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos


class SofaLogo(pygame.sprite.Sprite):

    def __init__(self, pos, screen):
        super().__init__()
        self.screen = screen
        self.pos = pos
        self.image = pygame.Surface((200 , 200), pygame.SRCALPHA)
        self.logo = pygame.image.load("sofashop.png")
        self.image.blit(self.logo, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos


class Curtains(pygame.sprite.Sprite):

    def __init__(self, pos, screen):
        super().__init__()
        self.screen = screen
        self.pos = pos
        self.color = random.choice(colors)
        self.image = pygame.Surface((100 , 100), pygame.SRCALPHA)
        self.image.fill(self.color)
        self.sofaImage = pygame.image.load("curtains.png")
        self.image.blit(self.sofaImage, (0, 0))
        self.rect = self.image.get_rect()
        self.pos_y = pos[1]
        self.speed_y = 2

    def update(self):
        self.pos_y += self.speed_y
        self.rect.center = (self.pos[0], self.pos_y)
        if self.pos_y > self.screen.get_height():
            self.kill()


class Sofa(pygame.sprite.Sprite):

    def __init__(self, pos, screen):
        super().__init__()
        self.pos = pos
        self.screen = screen
        self.color = random.choice(colors)
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.image.fill(self.color)
        self.sofaImage = pygame.image.load("sofa.png")
        self.image.blit(self.sofaImage, (0, 0))

        self.rect = self.image.get_rect()
        self.rect.y = self.pos[1]
        self.pos_x = pos[0]

    def newColor(self):
        self.color = random.choice(colors)
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.image.fill(self.color)
        self.sofaImage = pygame.image.load("sofa.png")
        self.image.blit(self.sofaImage, (0, 0))
    
    def update(self):
        self.pos_x = pygame.mouse.get_pos()[0]
        self.rect.x = self.pos_x
    
    def left(self):
        if(not self.pos_x < 0):
            self.pos_x -= 15
            self.rect.x = self.pos_x


    def right(self):
        if(not self.pos_x > 400):
            self.pos_x += 15
            self.rect.x = self.pos_x
def title_screen():
    title = True
    w, h = pygame.display.get_surface().get_size()
    clock = pygame.time.Clock()
    screen.fill((196,232,232))
    titleFont = pygame.font.SysFont("Arial", 50)
    levelDisp = titleFont.render("Sofa Shop - The Game", True, (0,0,0))
    screen.blit(levelDisp, dest=(w*.39,h*.3))
    titleFont = pygame.font.SysFont("Arial", 30)
    levelDisp = titleFont.render("Press any key to begin...", True, (0,0,0))
    screen.blit(levelDisp, dest=(w*.43,h*.6))
    logos = pygame.sprite.Group()
    logos.add(UnmadeLogo((w*.4,h*.5), screen))
    logos.add(SofaLogo((w*.6, h*.5), screen))
    logos.draw(screen)
    pygame.display.flip()
    while title:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                title = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                title = False
        clock.tick(60)
    run_game()

def run_game():
    w, h = pygame.display.get_surface().get_size()
    clock = pygame.time.Clock()
    counter = 0
    sofaCounter = 0
    level = 1
    levelSofaCounter = 0
    running = True
    playing = True
    curtains = pygame.sprite.Group()

   
    sofa = pygame.sprite.GroupSingle()
    
    sofa.add(Sofa((w/2, h*.8), screen))
    while running:
        counter += 1
        if (playing):
            if (counter % (100 - int(level ** (1 / 5) - 5.5))) == 0:
                w, h = pygame.display.get_surface().get_size()
                curtains.add(Curtains((random.randint(0, w), 0), screen))
                if level > 5:
                    for x in range(round(level ** 1/10)):
                        curtains.add(Curtains((random.randint(0, w), 0), screen))
            curtains.update()

        for curtain in curtains:
            try:
                collide = curtain.rect.colliderect(sofa.sprites()[0].rect)
            except (IndexError):
                continue
            if collide:
                if sofa.sprites()[0].color == curtain.color:
                    sofaCounter += 1
                    levelSofaCounter += 1
                    curtains.remove(curtain)
                    sofa.sprites()[0].newColor()
                    if levelSofaCounter == level ** 2 - level + 2:
                        levelSofaCounter = 0
                        level += 1
                else:
                    playing = False
                    curtains.empty()
                    sofa.empty()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            try:
                if event.type == pygame.MOUSEMOTION:
                    sofa.sprites()[0].update()
            except (IndexError):
                continue

        while not playing: #this is when you are dead
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return

            screen.fill((196,232,232))
            
            deadFont = pygame.font.SysFont("Arial", 25)
            deadFontsub = pygame.font.SysFont("Arial", 20)
            text = deadFont.render("You did not ♫ match your curtains too ♫", True, (0,0,0))
            subtext = deadFontsub.render("Final Score: " + str(sofaCounter), True, (0,0,0))
            finalLevel = deadFontsub.render("Final Level: " + str(level), True, (0,0,0))
            endGame = deadFontsub.render("(Click anywhere to close)", True, (0,0,0))

            screen.blit(text, dest=(w*.4,320))
            screen.blit(subtext, dest=(w*.4,350))
            screen.blit(finalLevel, dest=(w*.4,370))
            screen.blit(endGame, dest=(w*.4,390))
            pygame.display.flip()
            clock.tick(60)
        
        screen.fill((255, 255, 255))
        curtains.draw(screen)
        sofa.draw(screen)

        counterFont = pygame.font.SysFont("Arial", 14)
        text = counterFont.render("Curtains Matched: " + str(sofaCounter), True, (0,0,0))
        levelDisp = counterFont.render("Level: " + str(level), True, (0,0,0))
        screen.blit(text, dest=(w*.9,10))
        screen.blit(levelDisp, dest=(w*.9,25))

        pygame.display.flip()
        clock.tick(60 + (sofaCounter + 4) ** 3)

pygame.init()
pygame.font.init()
try:
    pygame.mixer.music.load('8-bit.mp3')
    pygame.mixer.music.play(-1)
except:
    print("Issue with music, skipping...")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
pygame.display.set_caption("Sofa Shop - The Game")
title_screen()
pygame.quit()