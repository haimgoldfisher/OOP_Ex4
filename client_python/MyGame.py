import copy
import math
import queue
import time
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
import networkx as nx


class MyGame:

    def __init__(self):
        self.pokemons = []
        self.agents = []
        self.graph = DiGraph()
        self.graph_alog = GraphAlgo(self.graph)
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

        self.refresh_time = int((1 / 10) / 0.001)

    def load(self):
        PORT = 6666
        HOST = '127.0.0.1'
        self.client.start_connection(HOST, PORT)
        self.load_pokemons()
        # self.load_agents()
        self.load_graph()
        self.load_info()
        self.graph_alog = GraphAlgo(self.graph)
        self.client.get_info()

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
        # self.pokemons = []
        pokemons_json_str = self.client.get_pokemons()
        pokemons_jobj = json.loads(pokemons_json_str)
        pokemons_lst = pokemons_jobj.get("Pokemons")
        new_pokemon_lst = []
        for p in pokemons_lst:
            p_data = p.get("Pokemon")
            value = p_data.get("value")
            typ = p_data.get("type")
            pos = p_data.get("pos")
            pos = pos.split(",")
            loc = Location(float(pos[0]), float(pos[1]), float(pos[2]))
            pokemon = Pokemon(value, typ, loc)
            new_pokemon_lst.append(pokemon)
        for np in new_pokemon_lst:
            if np not in self.pokemons:
                self.pokemons.append(np)
        for p in self.pokemons:
            if p not in new_pokemon_lst:
                self.pokemons.remove(p)

    def load_agents(self):
        # self.agents = []
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
            if agent in self.agents:
                indx = self.agents.index(agent)
                self.agents[indx].pos = loc
                self.agents[indx].src = src
                self.agents[indx].dest = dest
                self.agents[indx].speed = speed
                self.agents[indx].value = value
            else:
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

    def load_info(self):
        info_json_str = self.client.get_info()
        info_jobj = json.loads(info_json_str)
        info_dict = info_jobj.get("GameServer")
        num = info_dict.get("agents")
        self.add_agents(num)

    def add_agents(self, num):
        for x in range(num):
            fnd = self.graph.key_nodes.get(0)
            loc = Location(float(fnd.pos[0]), float(fnd.pos[1]), float(fnd.pos[2]))
            agent = Agent(x, 0, 0, -1, 1, loc)
            self.client.add_agent("{\"id\":%d}" % x)
            self.agents.append(agent)

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

    def my_scale2(self, data, x=False, y=False):
        if x:
            return (data - self.min_x) / (self.max_x - self.min_x)
        if y:
            return (data - self.min_y) / (self.max_y - self.min_y)

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
        # self.clock.tick(self.refresh_time)

    def simple_move_agents(self):
        for agent in self.agents:
            if agent.dest == -1:
                next_node = (agent.src - 1) % self.graph.v_size()
                self.client.choose_next_edge(
                    '{"agent_id":' + str(agent.key) + ', "next_node_id":' + str(next_node) + '}')
                ttl = self.client.time_to_end()
                print(ttl, self.client.get_info())

        self.client.move()

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

    def start2(self):
        self.client.start()
        while self.client.is_running():
            self.load_pokemons()
            self.load_agents()
            for pokemon in self.pokemons:
                if pokemon.agent_aloc == -1:
                    self.allocate_agent(pokemon)
            self.complex_move_agents()
            pygame.time.wait(100)
            # self.clock.tick(10)
            self.client.move()
            self.update_gui()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

    def complex_move_agents(self):  ################ maybe a problem
        for agent in self.agents:
            if len(agent.path) > 0:
                if agent.curr_node == agent.path[0]:
                    agent.path.__delitem__(0)
            if agent.dest == -1 and len(agent.path) > 0:
                # if agent.src == agent.path[0]:
                #     agent.path.__delitem__(0)
                next_node = agent.path[0]

                src_nd = self.graph.key_nodes.get(agent.curr_node)
                dest_nd = self.graph.key_nodes.get(next_node)
                edge_speed = src_nd.child_weight.get(next_node)
                # x_squared = (float(dest_nd.pos[0]) - float(src_nd.pos[0])) * (float(dest_nd.pos[0]) - float(src_nd.pos[0]))
                # y_squared = (float(dest_nd.pos[1]) - float(src_nd.pos[1])) * (float(dest_nd.pos[1]) - float(src_nd.pos[1]))
                x_squared = (self.my_scale2(float(dest_nd.pos[0]), x=True) - self.my_scale2(float(src_nd.pos[0]),
                                                                                            x=True)) ** 2
                y_squared = (self.my_scale2(float(dest_nd.pos[1]), y=True) - self.my_scale2(float(src_nd.pos[1]),
                                                                                            y=True)) ** 2
                dist_src2dest = math.sqrt(x_squared + y_squared)  # src to pokemon
                time_to_dest = (dist_src2dest / edge_speed)

                agent.curr_node = next_node
                agent.time2curr_dest = time_to_dest
                agent.path.__delitem__(0)

                self.client.choose_next_edge(
                    '{"agent_id":' + str(agent.key) + ', "next_node_id":' + str(next_node) + '}')
                ttl = self.client.time_to_end()
                print(ttl, self.client.get_info())
        min_time2dest = 100
        for agent in self.agents:
            if agent.time2curr_dest > agent.time2poke:
                min_time2dest = min(min_time2dest, agent.time2poke)
            else:
                min_time2dest = min(min_time2dest, agent.time2curr_dest)
        for agent in self.agents:
            agent.time2poke -= min_time2dest
            agent.time2curr_dest -= min_time2dest
            agent.time2final_dest -= min_time2dest
        # self.clock.tick(min_time2dest * 10)
        # time.sleep(min_time2dest*60)
        self.refresh_time = int(min_time2dest * 1000)
        # self.client.move()

    def allocate_agent(self, pokemon):
        min_time2poke = math.inf
        time2fdest = 0
        min_path = []
        chosen_agent = None
        agent_key = -1
        for agent in self.agents:
            src, dest = self.get_poke_edge(pokemon)
            if self.bet_ag_dest(agent, pokemon, src, dest):
                agent_key = agent.key
                chosen_agent = None
                break
            for index, value in enumerate(agent.path):
                if value == src and index + 1 < len(agent.path):
                    if agent.path[index + 1] == dest:
                        agent_key = agent.key
                        chosen_agent = None
                        break
            if agent_key != -1:
                break
            curr_time2poke, path, curr_time2fdest = self.calc_time(agent, pokemon)

            if curr_time2poke < min_time2poke:
                min_time2poke = curr_time2poke
                min_path = copy.copy(path)
                time2fdest = curr_time2fdest
                agent_key = agent.key
                chosen_agent = agent

        if chosen_agent is not None:
            chosen_agent.time2poke = min_time2poke
            chosen_agent.path += min_path
            chosen_agent.time2final_dest = time2fdest  ##### need to allocate time to time2dest
        pokemon.agent_aloc = agent_key
        return agent_key

    def bet_ag_dest(self, agent, pokemon, src, dest):
        if agent.dest != dest or agent.src != src:
            return False
        agent_pos = agent.pos
        poke_pos = pokemon.pos
        dest_nd = self.graph.key_nodes.get(dest)
        x1 = float(agent_pos.x)
        y1 = float(agent_pos.y)
        x2 = float(dest_nd.pos[0])
        y2 = float(dest_nd.pos[1])
        m = (y1 - y2) / (x1 - x2)
        n = y1 - m * x1
        a = poke_pos.x * m + n
        eps = 0.000000000001
        if a - eps < poke_pos.y < a + eps:
            return True
        return False
    def calc_time(self, agent, pokemon):
        src, dest = self.get_poke_edge(pokemon)
        curr_dest = agent.curr_node  ################ maybe a problem
        if len(agent.path) > 0:
            curr_dest = agent.path[len(agent.path) - 1]
        path_time, path = self.shortest_path(curr_dest, src)
        path.append(dest)
        path_time += agent.time2final_dest

        src_nd = self.graph.key_nodes.get(src)
        dest_nd = self.graph.key_nodes.get(dest)
        edge_speed = src_nd.child_weight.get(dest)  # weghit

        # x_squared = (pokemon.pos.x - float(src_nd.pos[0])) * (pokemon.pos.x - float(src_nd.pos[0]))
        # y_squared = (pokemon.pos.y - float(src_nd.pos[1])) * (pokemon.pos.y - float(src_nd.pos[1]))
        x_squared = (self.my_scale2(pokemon.pos.x, x=True) - self.my_scale2(float(src_nd.pos[0]), x=True)) ** 2
        y_squared = (self.my_scale2(pokemon.pos.y, y=True) - self.my_scale2(float(src_nd.pos[1]), y=True)) ** 2
        dist_src2poke = math.sqrt(x_squared + y_squared)  # src to pokemon
        time_to_poke = path_time + (dist_src2poke / edge_speed)

        # x_squared = (float(dest_nd.pos[0]) - float(src_nd.pos[0])) * (float(dest_nd.pos[0]) - float(src_nd.pos[0]))
        # y_squared = (float(dest_nd.pos[1]) - float(src_nd.pos[1])) * (float(dest_nd.pos[1]) - float(src_nd.pos[1]))
        x_squared = (self.my_scale2(float(dest_nd.pos[0]), x=True) - self.my_scale2(float(src_nd.pos[0]), x=True)) ** 2
        y_squared = (self.my_scale2(float(dest_nd.pos[1]), y=True) - self.my_scale2(float(src_nd.pos[1]), y=True)) ** 2
        dist_src2dest = math.sqrt(x_squared + y_squared)  # src to dest
        time_to_fdest = path_time + (dist_src2dest / edge_speed)

        return time_to_poke, path, time_to_fdest

    def get_poke_edge(self, pokemon):
        poke_pos = pokemon.pos
        for nd in self.graph.key_nodes.values():
            for child in nd.child_weight.keys():
                ch_nd = self.graph.key_nodes.get(child)
                src = nd.pos
                dest = ch_nd.pos
                x1 = float(src[0])
                y1 = float(src[1])
                x2 = float(dest[0])
                y2 = float(dest[1])
                m = (y1 - y2) / (x1 - x2)
                n = y1 - m * x1
                a = poke_pos.x * m + n
                eps = 0.000000000001
                if a - eps < poke_pos.y < a + eps:
                    if x1 < poke_pos.x < x2 or x1 > poke_pos.x > x2:
                        if y1 < poke_pos.y < y2 or y1 > poke_pos.y > y2:
                            if pokemon.type > 0 and nd.key < ch_nd.key:
                                return nd.key, ch_nd.key
                            if pokemon.type < 0 and nd.key > ch_nd.key:
                                return nd.key, ch_nd.key

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm.
        this function use Dijkstra's Algorithm with PriorityQueue.
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        """
        path = []
        if id1 == id2:
            path.append(id1)
            return 0, path
        previous = dict()
        times = dict()
        visited = dict()
        keys = self.graph.key_nodes.copy()
        pq = queue.PriorityQueue()
        for key in keys.keys():
            times[key] = math.inf
        times[id1] = 0
        pq.put((0, id1))
        while visited.__len__() != keys.__len__():
            if pq.qsize() == 0:
                break
            curr_key = pq.get()[1]
            if visited.get(curr_key) is not None:
                continue
            visited[curr_key] = True
            curr_nd = keys.get(curr_key)
            for edge in curr_nd.child_weight.items():
                curr_dest = edge[0]
                curr_speed = edge[1]
                if visited.get(curr_dest) is not None:
                    continue
                curr_time = times.get(curr_dest)
                # x_squared = (float(keys.get(curr_dest).pos[0]) - float(curr_nd.pos[0])) * (float(keys.get(curr_dest).pos[0]) - float(curr_nd.pos[0]))
                # y_squared = (float(keys.get(curr_dest).pos[1]) - float(curr_nd.pos[1])) * (float(keys.get(curr_dest).pos[1]) - float(curr_nd.pos[1]))
                x_squared = (self.my_scale2(float(keys.get(curr_dest).pos[0]), x=True) - self.my_scale2(
                    float(curr_nd.pos[0]), x=True)) ** 2
                y_squared = (self.my_scale2(float(keys.get(curr_dest).pos[1]), y=True) - self.my_scale2(
                    float(curr_nd.pos[1]), y=True)) ** 2
                dist_src2dest = math.sqrt(x_squared + y_squared)
                tmp_time = dist_src2dest / curr_speed
                new_time = times.get(curr_key) + tmp_time
                if new_time < curr_time:
                    times[curr_dest] = new_time
                    previous[curr_dest] = curr_key
                pq.put((times.get(curr_dest), curr_dest))
        if times.get(id2) == math.inf:
            return math.inf, []
        curr = id2
        while curr != id1:
            path.insert(0, curr)
            curr = previous.get(curr)
        path.insert(0, id1)
        ti = times.get(id2)
        return ti, path


if __name__ == '__main__':
    mg = MyGame()
    mg.load()
    mg.start2()

    # mg.update_gui()
    #
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             exit(0)
    # s = set()
    # s.
    # s =[]
    # s.
