from pygame import gfxdraw
import pygame
import math

from client_python.DiGraph import DiGraph
import Pokemon
import Agent


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


class GUI:
    def __init__(self):
        self.graph = DiGraph()
        # self.pokemons = []
        # self.agents = []

        pygame.init()
        WIDTH, HEIGHT = 1080, 720
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), depth=32, flags=pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        pygame.font.init()
        pygame.display.set_caption("Pokémon Game")
        self.FONT = pygame.font.SysFont('Arial', 20, bold=True)
        self.radius = 15
        self.min_x = math.inf
        self.min_y = math.inf
        self.max_x = -math.inf
        self.max_y = -math.inf

    def first_update(self, agents, pokemons, graph, points, moves, time_left):
        self.graph = graph
        for n in self.graph.key_nodes.values():
            self.min_x = min(self.min_x, float(n.pos[0]))
            self.min_y = min(self.min_y, float(n.pos[1]))
            self.max_x = max(self.max_x, float(n.pos[0]))
            self.max_y = max(self.max_y, float(n.pos[1]))
        self.update(agents, pokemons, points, moves, time_left)

    # decorate scale with the correct values

    def my_scale(self, data, x=False, y=False):
        if x:
            return scale(data, 50, self.screen.get_width() - 50, self.min_x, self.max_x)
        if y:
            return scale(data, 50, self.screen.get_height() - 50, self.min_y, self.max_y)

    def update(self, agents, pokemons, points, moves, time_left):
        """
        updates the gui
        """
        # refresh surface
        self.screen.fill(pygame.Color(0, 0, 0))
        # texts
        pygame.font.init()
        # p, m, t = self.get_params()
        points = self.FONT.render("Points: " + points, False, (248, 248, 255))
        moves = self.FONT.render("Moves: " + moves, False, (248, 248, 255))
        time_left = self.FONT.render("Time Left: " + time_left, False, (248, 248, 255))
        self.screen.blit(points, (5, 0))
        self.screen.blit(moves, (5, 25))
        self.screen.blit(time_left, (5, 50))

        # stop button
        img = pygame.image.load('stop.png').convert_alpha()
        img2 = pygame.image.load('stop_on.png').convert_alpha()
        rect = img.get_rect(topleft=(5, 75))
        pos = pygame.mouse.get_pos()
        if rect.collidepoint(pos):
            self.screen.blit(img2, (5, 75))
        else:
            self.screen.blit(img, (5, 75))

        # draw edges
        for nd in self.graph.key_nodes.values():
            for child in nd.child_weight.keys():
                src = nd
                dest = self.graph.key_nodes.get(child)

                # scaled positions
                src_x = self.my_scale(float(src.pos[0]), x=True)
                src_y = self.my_scale(float(src.pos[1]), y=True)
                dest_x = self.my_scale(float(dest.pos[0]), x=True)
                dest_y = self.my_scale(float(dest.pos[1]), y=True)

                # draw the line
                pygame.draw.line(self.screen, pygame.Color(61, 72, 126),
                                 (src_x, src_y), (dest_x, dest_y))
        # draw nodes
        for n in self.graph.key_nodes.values():
            x = self.my_scale(float(n.pos[0]), x=True)
            y = self.my_scale(float(n.pos[1]), y=True)

            # its just to get a nice antialiased circle
            gfxdraw.filled_circle(self.screen, int(x), int(y),
                                  self.radius, pygame.Color(64, 80, 174))
            gfxdraw.aacircle(self.screen, int(x), int(y),
                             self.radius, pygame.Color(255, 255, 255))

            # draw the node id
            id_srf = self.FONT.render(str(n.key), True, pygame.Color(255, 255, 255))
            rect = id_srf.get_rect(center=(x, y))
            self.screen.blit(id_srf, rect)

        # draw agents
        for agent in agents:
            pygame.draw.circle(self.screen, pygame.Color(122, 61, 23),
                               (int((self.my_scale(agent.pos.x, x=True))), int((self.my_scale(agent.pos.y, y=True)))),
                               10)
            # ball = pygame.image.load('pokeball.png')
            # ball = pygame.transform.scale(ball, (40, 40))
            # # ball.set_colorkey((163, 73, 164))
            # self.screen.blit(ball,(int((self.my_scale(agent.pos.x, x=True)))-20, int((self.my_scale(agent.pos.y, y=True)))-20))
        # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
        for p in pokemons:
            if p.type < 0:
                # pygame.draw.circle(self.screen, pygame.Color(0, 255, 255),
                #                    (int((self.my_scale(p.pos.x, x=True))), int((self.my_scale(p.pos.y, y=True)))), 10)
                pokemon = pygame.image.load('pokemon1.jpg')
                pokemon = pygame.transform.scale(pokemon, (40, 40))
                # pokemon.set_colorkey((163, 73, 164))
                self.screen.blit(pokemon, (
                    int((self.my_scale(p.pos.x, x=True))) - 20, int((self.my_scale(p.pos.y, y=True))) - 20))
            else:
                # pygame.draw.circle(self.screen, pygame.Color(67, 89, 65),
                #                    (int((self.my_scale(p.pos.x, x=True))), int((self.my_scale(p.pos.y, y=True)))), 10)
                pokemon = pygame.image.load('pokemon2.jpg')
                pokemon = pygame.transform.scale(pokemon, (40, 40))
                pokemon.set_colorkey((163, 73, 164))
                self.screen.blit(pokemon, (
                    int((self.my_scale(p.pos.x, x=True))) - 20, int((self.my_scale(p.pos.y, y=True))) - 20))
            pokemon_val = self.FONT.render(str(p.value), False, (255, 0, 0))
            self.screen.blit(pokemon_val,
                             (int((self.my_scale(p.pos.x, x=True))), int((self.my_scale(p.pos.y, y=True))) + 12))
        # update screen changes
        pygame.display.update()

        # refresh rate
        # self.clock.tick(self.refresh_time)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
