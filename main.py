import pygame
import time
import random
import os
import sys

class Background:
    def __init__(self):
        self.image = pygame.image.load("Images/background.png").convert()
        self.image = pygame.transform.scale(self.image, (800, 602))
        self.margin_left = pygame.image.load("Images/margin_1.png").convert()
        self.margin_left = pygame.transform.scale(self.margin_left, (60, 602))
        self.margin_right = pygame.image.load("Images/margin_2.png").convert()
        self.margin_right = pygame.transform.scale(self.margin_right, (60, 602))

    def move(self, screen, scr_height, movL_y, movR_y):
        for i in range(0, 2):
            screen.blit(self.image, (0, movL_y - i * scr_height))
            screen.blit(self.image, (0, movR_y - i * scr_height))
            screen.blit(self.margin_left, (0, movL_y - i * scr_height))
            screen.blit(self.margin_right, (740, movR_y - i * scr_height))

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load("Images/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 0

    def update(self):
        self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Hazard:
    def __init__(self, img, x, y):
        self.image = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.scale(self.image, (130, 130))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Game:
    def __init__(self, size, fullscreen):
        pygame.init()
        self.width, self.height = size
        if fullscreen:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.mouse.set_visible(0)
        pygame.display.set_caption("Título do Seu Jogo")
        self.clock = pygame.time.Clock()
        self.dt = 16
        self.background = Background()
        self.player = Player((self.width - 56) / 2, self.height - 125)
        self.hazards = []
        self.run = True
        self.score = 0
        self.h_passed = 0
        self.velocity_background = 10
        self.velocity_hazard = 5
        self.hazard_delay = 0
        self.delay_timer = 0
        self.play_soundtrack()  # Chama o método para iniciar a trilha sonora

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.speed = -5
                elif event.key == pygame.K_RIGHT:
                    self.player.speed = 5
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.speed < 0:
                    self.player.speed = 0
                elif event.key == pygame.K_RIGHT and self.player.speed > 0:
                    self.player.speed = 0

    def check_collision(self):
        for hazard in self.hazards:
            if self.player.rect.colliderect(hazard.rect):
                self.play_sound("Sounds/jump2.wav")  # Chama o método para tocar o som de colisão
                return True
        return False

    def update_elements(self):
        self.background.move(self.screen, self.height, 0, 0)
        
        # Atraso entre a criação de hazards
        self.delay_timer += 1
        if self.delay_timer >= 30:
            self.delay_timer = 0
            h_x = random.randrange(125, 660)
            h_y = -500
            self.hazards.append(Hazard("Images/satelite.png", h_x, h_y))
        
        # Atualiza a posição dos hazards e verifica colisões
        for hazard in self.hazards:
            hazard.rect.y += self.velocity_hazard
            if hazard.rect.y > self.height:
                self.hazards.remove(hazard)
                self.score += 10  # Incrementa a pontuação quando um hazard passa

        # Atualiza o número de hazards que passaram
        self.h_passed = self.score // 10

    def draw_elements(self):
        self.background.move(self.screen, self.height, 0, 0)
        for hazard in self.hazards:
            hazard.draw(self.screen)

        font = pygame.font.SysFont(None, 35)
        passou = font.render("Passou: " + str(self.h_passed), True, (255, 255, 128))
        score_text = font.render("Score: " + str(self.score), True, (253, 231, 32))
        self.screen.blit(passou, (0, 50))
        self.screen.blit(score_text, (0, 100))

        self.player.update()
        self.player.draw(self.screen)

    def game_over(self):
        my_font = pygame.font.Font("Fonts/Fonte4.ttf", 100)
        render_text_perdeu = my_font.render("GAME OVER", 0, (255, 0, 0))
        self.screen.blit(render_text_perdeu, (80, 200))
        pygame.display.update()
        time.sleep(3)

    def play_soundtrack(self):
        #inclue a trilha sonora
        if os.path.isfile("Sounds/song.wav"):
            pygame.mixer.music.load("Sounds/song.wav")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(loops= -1)
        else:
            print("Sounds/song.mp3 not found...ignoring", file=sys.stderr)

    def play_sound(self, sound):
        #sound
        if os.path.isfile(sound):
            pygame.mixer.music.load(sound)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
        else:
            print("Sound file not found... ignoring", file=sys.stderr)

    def restart_game(self):
        self.player.rect.topleft = ((self.width - 56) / 2, self.height - 125)
        self.hazards.clear()
        self.score = 0
        self.h_passed = 0
        self.run = True

    def loop(self):
        while self.run:
            self.clock.tick(60)
            self.handle_events()
            if self.check_collision():
                self.game_over()
                self.restart_game()
            self.update_elements()
            self.draw_elements()
            pygame.display.update()

game = Game((800, 600), fullscreen=False)
game.loop()










