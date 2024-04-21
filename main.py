import pygame
import time
import random


class Background:
    image = None
    margin_left = None
    margin_right = None

    def move(self, screen, scr_height, movL_x, movL_y, movR_x, movR_y):
            for i in range(0, 2):
                screen.blit(self.image, (movL_x, movL_y - i * scr_height))
                screen.blit(self.image, (movR_x, movR_y - i * scr_height))
                screen.blit(self.margin_left, (0, movL_y - i * scr_height))
                screen.blit(self.margin_right, (740, movR_y - i * scr_height))
                
    def __init__(self):
        background_fig = pygame.image.load("Images/background.png")
        background_fig = background_fig.convert()
        background_fig = pygame.transform.scale(background_fig, (800,602))
        self.image = background_fig

        margin_left_fig = pygame.image.load("Images/margin_1.png")
        margin_left_fig.convert()
        margin_left_fig = pygame.transform.scale(margin_left_fig, (60,602))
        self.margin_left = margin_left_fig

        margin_right_fig = pygame.image.load("Images/margin_2.png")
        margin_right_fig.convert()
        margin_right_fig = pygame.transform.scale(margin_right_fig, (60,602))
        self.margin_right = margin_right_fig


    def update(self, dt):
        pass
    
    def draw(self, screen):
        screen.blit(self.image, (0,0))


class player:
    image = None
    x = None
    y = None

    def __init__(self, x, y):
        player_fig = pygame.image.load("images/player.png")
        player_fig.convert()
        player_fig = pygame.transform.scale(player_fig, (90, 90))
        self.image = player_fig
        self.x = x
        self.y = y 

    def draw(self, screen, x, y):
        screen.blit(self.image, (x,y))

class hazard:
    image = None
    x = None
    y = None

    def __init__(self, img, x, y):
        hazard_fig = pygame.image.load(img)
        hazard_fig.convert()
        hazard_fig = pygame.transform.scale(hazard_fig, (130, 130))
        self.image = hazard_fig
        self.x = x 
        self.y = y 

    def draw (self, screen,x, y):
        screen.blit(self.image, (x, y))

class Game:
    screen = None
    screen_size = None
    width = 800
    height = 600
    run = True
    background = None
    player = None
    hazard = []
    render_text_bateulateral = None
    render_text_perdeu = None

    DIREITA = pygame.K_RIGHT
    ESQUERDA = pygame.K_LEFT
    mudar_x = 0.0 

    def __init__(self, size, fullscreen):
        pygame.init()
        
        if fullscreen:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height))
        
        self.screen_size = self.screen.get_size()
        pygame.mouse.set_visible(0)
        pygame.display.set_caption("Título do Seu Jogo")

        my_font = pygame.font.Font("Fonts/Fonte4.ttf", 100)
        self.render_text_bateulateral = my_font.render("VOCÊ BATEU!", 0, (255, 255, 255))
        self.render_text_perdeu = my_font.render("GAME OVER", 0, (255, 0, 0))

        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            if event.type == pygame.KEYDOWN:
                if event.key == self.ESQUERDA:
                    self.mudar_x = -3

                if event.key == self.DIREITA:
                    self.mudar_x = 3 

            if event.type == pygame.KEYUP:
                if event.key == self.ESQUERDA or event.key == self.DIREITA:
                    self.mudar_x = 0
              
    def elements_update(self, dt):
        self.background.update(dt)

    def elements_draw(self):
        self.background.draw(self.screen)
    
    def loop(self):
        velocidade_background = 10
        velocidade_hazard = 10
        hzard = 0
        h_x = random.randrange(125, 660)
        h_y = -500
        h_width = 100
        h_height = 110

      
        movL_x = 0
        movL_y = 0
        movR_x = 740
        movR_y = 0
        self.background = Background()
        x = (self.width - 56)/2
        y = self.height - 125
        self.player = player(x,y)
        clock = pygame.time.Clock()
        dt = 16

        self.hazard.append(hazard("Images/satelite.png", h_x, h_y))
        self.hazard.append(hazard("Images/nave.png", h_x, h_y))
        self.hazard.append(hazard("Images/cometaVermelho.png", h_x, h_y))
        self.hazard.append(hazard("Images/meteoros.png", h_x, h_y))
        self.hazard.append(hazard("Images/buracoNegro.png", h_x, h_y))

        while self.run:
            clock.tick(1000 / dt)
            self.background.move(self.screen, self.height,movL_x, movL_y, movR_x, movR_y)
            movL_y = movL_y + velocidade_background
            movR_y = movR_y + velocidade_background

            if movL_y > 600 and movR_y > 600:
                movL_y -= 600
                movR_y -= 600 

            x = x +self.mudar_x   
            self.handle_events()
            self.elements_update(dt)
            self.elements_draw()
            
            self.player.draw(self.screen, x, y)
            if x > 760 - 92 or x < 40 + 5:
                self.screen.blit(self.render_text_bateulateral, (80,200))
                pygame.display.update()
                time.sleep(3)
                self.loop()
                self.run = False

            h_y = h_y + velocidade_hazard/4
            self.hazard[hzard].draw(self.screen, h_x, h_y)
            h_y = h_y + velocidade_hazard
            
            if h_y > self.height:
                h_y = 0 - h_height
                h_x = random.randrange(125, 650 - h_height)
                hzard = random.randint(0, 4) 


            pygame.display.update()
            clock.tick(60)  # Limitar a taxa de quadros para 60 FPS
game = Game((800, 600), fullscreen=False)
game.loop()
