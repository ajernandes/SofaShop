import pygame
import random

colors = [(50,168,82), (173,247,19), (119,37,253), (117,182,240), (243,135,90)]

class Curtains(pygame.sprite.Sprite):

    def __init__(self, pos, screen):
        super().__init__()
        self.screen = screen
        self.pos = pos
        self.color = random.choice(colors)
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
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
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.image.fill(self.color)
        self.sofaImage = pygame.image.load("sofa.png")
        self.image.blit(self.sofaImage, (0, 0))

        self.rect = self.image.get_rect()
        self.rect.y = self.pos[1]
        self.pos_x = pos[0]

    def newColor(self):
        self.color = random.choice(colors)
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
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

def run_game():
    pygame.init()
    pygame.font.init()
    try:
        pygame.mixer.music.load('8-bit.mp3')
        pygame.mixer.music.play(-1)
    except:
        print("Issue with music, skipping...")
    screen = pygame.display.set_mode((400, 640))
    pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
    pygame.display.set_caption("SofaShop")
    clock = pygame.time.Clock()
    counter = 0
    sofaCounter = 0
    running = True
    playing = True
    curtains = pygame.sprite.Group()

   
    sofa = pygame.sprite.GroupSingle()
    
    sofa.add(Sofa((200, 550), screen))
    while running:
        counter += 1
        if (playing):
            if (counter % 50) == 0:
                curtains.add(Curtains((random.randint(20, 400), 0), screen))
            curtains.update()

        for curtain in curtains:
            try:
                collide = curtain.rect.colliderect(sofa.sprites()[0].rect)
            except (IndexError):
                continue
            if collide:
                if sofa.sprites()[0].color == curtain.color:
                    sofaCounter += 1
                    curtains.remove(curtain)
                    sofa.sprites()[0].newColor()
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

        while not playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            screen.fill((255, 0, 0))
            
            deadFont = pygame.font.SysFont("Arial", 20)
            deadFontsub = pygame.font.SysFont("Arial", 20)
            text = deadFont.render("You did not ♫ match your curtains too ♫", True, (0,0,0))
            subtext = deadFontsub.render("Final Score: " + str(sofaCounter), True, (0,0,0))

            screen.blit(text, dest=(55,320))
            screen.blit(subtext, dest=(55,350))
            pygame.display.flip()
            clock.tick(60)
        
        screen.fill((255, 255, 255))
        curtains.draw(screen)
        sofa.draw(screen)

        counterFont = pygame.font.SysFont("Arial", 14)
        text = counterFont.render("Curtains Matched: " + str(sofaCounter), True, (0,0,0))
        screen.blit(text, dest=(290,10))

        pygame.display.flip()
        clock.tick(60)


run_game()
pygame.quit()