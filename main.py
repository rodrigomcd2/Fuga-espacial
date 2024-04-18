import pygame

class Background:
    image = None
    margin_left = None
    margin_right = None

    def __init__(self):
        background_fig = pygame.image.load("images/background.png")
        background_fig = background_fig.convert()
        self.image = background_fig

    def update(self, dt):
        pass
    
    def draw(self, screen):
        screen.blit(self.image, (0,0))

class Game:
    screen = None
    screen_size = None
    width = 800
    height = 600
    run = True
    background = None

    def __init__(self, size, fullscreen):
        pygame.init()
        
        if fullscreen:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height))
        
        self.screen_size = self.screen.get_size()
        pygame.mouse.set_visible(0)
        pygame.display.set_caption("Título do Seu Jogo")
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
        
    def elements_update(self, dt):
        self.background.update(dt)

    def elements_draw(self):
        self.background.draw(self.screen)
    
    def loop(self):
        self.background = Background()
        clock = pygame.time.Clock()
        dt = 16

        while self.run:
            clock.tick(1000 / dt)
            self.handle_events()
            self.elements_update(dt)
            self.elements_draw()

            pygame.display.update()
            clock.tick(60)  # Limitar a taxa de quadros para 60 FPS

game = Game((800, 600), fullscreen=False)
game.loop()

