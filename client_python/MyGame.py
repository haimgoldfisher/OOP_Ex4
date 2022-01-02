import math
from types import SimpleNamespace
from client import Client
import json
from pygame import gfxdraw
import pygame
# from pygame import *
from DiGraph import DiGraph
from GraphAlgo import GraphAlgo
from Pokemon import Pokemon
from Agent import Agent
from client_python.Loc_Node_Edge import Location


class MyGame:

    def __init__(self):
        self.pokemons = []
        self.agents = []
        self.graph = DiGraph()
        self.score = 0
        self.move_counter = 0
        self.client = Client()
        pygame.init()
        WIDTH, HEIGHT = 1080, 720
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), depth=32, flags=pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.FONT = pygame.font.SysFont('Arial', 20, bold=True)
        self.radius = 15
        self.min_x = math.inf
        self.min_y = math.inf
        self.max_x = -math.inf
        self.max_y = -math.inf

    def load(self):
        PORT = 6666
        HOST = '127.0.0.1'
        self.client.start_connection(HOST, PORT)
        self.load_pokemons()
        # self.load_agents()
        self.load_graph()
        for n in self.graph.key_nodes.values():
            self.min_x = min(self.min_x, float(n.pos[0]))
            self.min_y = min(self.min_y, float(n.pos[1]))
            self.max_x = max(self.max_x, float(n.pos[0]))
            self.max_y = max(self.max_y, float(n.pos[1]))
        self.update_gui()

    def update(self):
        """
        updates the game status
        """
        pass

    def load_pokemons(self):
        self.pokemons = []
        pokemons_json_str = self.client.get_pokemons()
        pokemons_jobj = json.loads(pokemons_json_str)
        pokemons_lst = pokemons_jobj.get("Pokemons")
        for p in pokemons_lst:
            p_data = p.get("Pokemon")
            value = p_data.get("value")
            typ = p_data.get("type")
            pos = p_data.get("pos")
            pos = pos.split(",")
            loc = Location(float(pos[0]), float(pos[1]), float(pos[2]))
            pokemon = Pokemon(value, typ, loc)
            self.pokemons.append(pokemon)

    def load_agents(self):
        self.agents = []
        agents_json_str = self.client.get_agents()
        agents_jobj = json.loads(agents_json_str)
        agents_lst = agents_jobj.get("Agents")
        for a in agents_lst:
            a_data = a.get("Agent")
            key = a_data.get("id")
            value = a_data.get("value")
            src = a_data.get("src")
            dest = a_data.get("dest")
            speed = a_data.get("speed")
            pos = a_data.get("pos")
            pos = pos.split(",")
            loc = Location(float(pos[0]), float(pos[1]), float(pos[2]))
            agent = Agent(key, value, src, dest, speed, loc)
            self.agents.append(agent)

    def load_graph(self):
        graph_json_str = self.client.get_graph()
        graph_jobj = json.loads(graph_json_str)
        edges = graph_jobj.get("Edges")
        nodes = graph_jobj.get("Nodes")
        for d in nodes:
            node_id = d.get("id")
            pos = d.get("pos")
            if pos is not None:
                pos = pos.split(",")
                new_loc = Location(pos[0], pos[1], pos[2])
                self.graph.add_node(node_id, new_loc.pos)
            else:
                self.graph.add_node(node_id, None)

        for d in edges:
            src = d["src"]
            w = d["w"]
            dest = d["dest"]
            self.graph.add_edge(src, dest, w)

    def add_agents(self, num):
        for x in range(num):
            fnd = self.graph.key_nodes.get(0)
            loc = Location(float(fnd.pos[0]), float(fnd.pos[1]), float(fnd.pos[2]))
            agent = Agent(x, 0, 0, -1, 1, loc)
            self.client.add_agent("{\"id\":%d}" % x)
            self.agents.append(agent)

    def simple_move_agents(self):
        for agent in self.agents:
            if agent.dest == -1:
                next_node = (agent.src - 1) % self.graph.v_size()
                self.client.choose_next_edge(
                    '{"agent_id":' + str(agent.key) + ', "next_node_id":' + str(next_node) + '}')
                ttl = self.client.time_to_end()
                print(ttl, self.client.get_info())

        self.client.move()

    def scale(self, data, min_screen, max_screen, min_data, max_data):
        """
        get the scaled data with proportions min_data, max_data
        relative to min and max screen dimentions
        """
        return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen

    # decorate scale with the correct values

    def my_scale(self, data, x=False, y=False):
        if x:
            return self.scale(data, 50, self.screen.get_width() - 50, self.min_x, self.max_x)
        if y:
            return self.scale(data, 50, self.screen.get_height() - 50, self.min_y, self.max_y)

    def update_gui(self):
        """
        updates the gui
        """
        # refresh surface
        self.screen.fill(pygame.Color(0, 0, 0))

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

        # draw agents
        for agent in self.agents:
            pygame.draw.circle(self.screen, pygame.Color(122, 61, 23),
                               (int((self.my_scale(agent.pos.x, x=True))), int((self.my_scale(agent.pos.y, y=True)))),
                               10)
        # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
        for p in self.pokemons:
            pygame.draw.circle(self.screen, pygame.Color(0, 255, 255),
                               (int((self.my_scale(p.pos.x, x=True))), int((self.my_scale(p.pos.y, y=True)))), 10)

        # update screen changes
        pygame.display.update()

        # refresh rate
        self.clock.tick(60)

    def start(self):
        self.client.start()
        while self.client.is_running():
            self.load_pokemons()
            self.load_agents()
            self.simple_move_agents()
            self.update_gui()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)


if __name__ == '__main__':
    mg = MyGame()
    mg.load()
    mg.add_agents(1)
    mg.start()
    # mg.update_gui()
    #
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             exit(0)
