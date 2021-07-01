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
        self.speed_y = 0

    def update(self):
        self.speed_y = 1
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
    screen = pygame.display.set_mode((400, 640))
    pygame.display.set_caption("SofaShop")
    clock = pygame.time.Clock()
    counter = 0
    running = True
    curtains = pygame.sprite.Group()

    sofa = pygame.sprite.GroupSingle()
    
    sofa.add(Sofa((200, 580), screen))
    while running:
        counter += 1
        if (counter % 100) == 0:
            curtains.add(Curtains((random.randint(20, 400), 0), screen))
        curtains.update()

        for curtain in curtains:
            collide = curtain.rect.colliderect(sofa.sprites()[0].rect)
            if collide:
                if sofa.sprites()[0].color == curtain.color:
                    sofa.sprites()[0].newColor()
                else:
                    print("fail")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            key_input = pygame.key.get_pressed()  
            if key_input[pygame.K_LEFT]:
                sofa.sprites()[0].left()
            if key_input[pygame.K_RIGHT]:
                sofa.sprites()[0].right()
        

        screen.fill((255, 255, 255))
        curtains.draw(screen)
        sofa.draw(screen)

        pygame.display.flip()
        clock.tick(60)


run_game()
pygame.quit()