import pygame


class StopButton(object):
    def __init__(self, x, y, image, scale, screen, server):  # server = client
        WIDTH = image.get_width()
        HEIGHT = image.get_height()
        self.image = pygame.transform.scale(image, (int(WIDTH * scale), int(HEIGHT * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.screen = screen
        self.server = server # client
        self.clicked = False

    def draw(self, frame):
        clicked = False
        mouse_loc = pygame.mouse.get_pos() # the location of the mouse
        if self.rect.collidepoint(mouse_loc):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        frame.blit(self.image, (self.rect.x, self.rect.y))
        return clicked

    def start(self):
        #img = pygame.image.load('stop.png').convert_alpha()
        #stop_btn = Button(450, 200, img, 0.8, self.screen, self.server)
        #stop_btn = pygame.transform.scale(stop_btn, (int(width*self.scale()), int(height*self.scale())))
        running = True
        while running and self.server.is_running():
            self.screen.fill((202, 228, 241))
            if self.draw(self.screen):
                print('STOP')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()
        pygame.quit()