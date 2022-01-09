import copy
import json
import math
import threading
import time

import pygame

from GUI import GUI
from Model import Model
from DiGraph import DiGraph
from client_python.Agent import Agent
from client_python.GraphAlgo import GraphAlgo
from client_python.Loc_Node_Edge import Location
from client_python.Pokemon import Pokemon
from client_python.client import Client


class Control:
    """
    this class is the class that communicate with the server, that mean that all the calls to the server like:
    move, get_info, get_agents etc. will be here.
    this class holds the following fields:
    gui - an gui object that manege the visualisation of the project
    model - an object that responsible of the algorithmic side of this project
    client - client object that communicate with the server.
    graph - the graph of the game
    graph_algo - a set of algorithms that can be use on the graph
    pokemons - a list of all the pokemons on the graph at specific moment
    agents - a list of all the agents in this game
    flag - a flag that tells the model what algorithm is better for this case
    """

    def __init__(self):
        self.gui = GUI()
        self.model = Model()
        self.client = Client()
        self.graph = DiGraph()
        self.graph_algo = GraphAlgo(self.graph)

        self.pokemons = []
        self.agents = []

        # self.score = 0
        # self.move_counter = 0
        self.flag = 0

    def load(self):
        """
        this function is called once before the starts its loading the necessary information such as the graph,
        the agents, the pokemons, etc. it also calls the load info function that add the agents.
        after loading the information it tells the model object and the gui object to make thier first update.
        """
        PORT = 6666
        HOST = '127.0.0.1'
        self.client.start_connection(HOST, PORT)
        self.load_pokemons()
        # self.load_agents()
        self.load_graph()
        self.graph_algo = GraphAlgo(self.graph)
        self.model.graph = self.graph
        self.model.graph_algo = self.graph_algo
        self.load_info()
        self.load_agents()
        # self.client.get_info()

        p, m, t = self.get_params()
        self.gui.first_update(self.agents, self.pokemons, self.graph, p, m, t)
        self.model.first_update(self.agents, self.pokemons, self.graph_algo, self.flag)

    def load_pokemons(self):
        """
        this function ask from the client the pokemons information and than load it it into a list of pokemons.
        then it initialize the "pokemons" field with this list.
        """
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
                self.pokemons.append(copy.copy(np))
        for p in self.pokemons:
            if p not in new_pokemon_lst:
                self.pokemons.remove(copy.copy(p))

    def load_agents(self):
        """
        this function ask from the client the agents information and than load it into a list of agents.
        then it initialize the "agents" field with this list.
        """
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
            new_agent = Agent(key, value, src, dest, speed, loc)
            if new_agent in self.agents:
                indx = self.agents.index(new_agent)
                agent = self.agents[indx]
                self.agents[indx].pos = loc
                self.agents[indx].src = src
                self.agents[indx].dest = dest
                self.agents[indx].value = value
                if self.agents[indx].speed != new_agent.speed:
                    old_speed = self.agents[indx].speed
                    ratio = speed / old_speed
                    for i in range(len(self.agents[indx].time2pokes)):
                        self.agents[indx].time2pokes[i] /= ratio
                    for i in range(len(self.agents[indx].time2final_dests)):
                        self.agents[indx].time2final_dests[i] /= ratio
                    self.agents[indx].time2curr_dest /= ratio
                    self.agents[indx].speed = speed

            else:
                self.agents.append(new_agent)

    def load_graph(self):
        """
       this function ask from the client the graph information and than load it into a DiGraph object.
       """
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
        """
        this function ask from the client the information of the game to get the number of agents in this level.
        then it adding the new agents to the game using the add_agents function and change the the flag according to the
        number of agents in this level. flag == 1 means there is only 1 agent in this case, flag == 0 means there is more
        than 1 agent.
        """
        info_json_str = self.client.get_info()
        info_jobj = json.loads(info_json_str)
        info_dict = info_jobj.get("GameServer")
        num = info_dict.get("agents")
        self.add_agents(num)
        if num == 1:
            self.flag = 1

    def add_agents(self, num):
        """
        this function add the agents to the server, if there is 1 agent it will find the pokemon with the biggest value
        than it will find the source of the edge he is lying on and will add the agent there.
        if there is more than 1 agent it will add them to the node match to their key number.
        """
        if num == 1:
            pokes_lst = copy.copy(self.pokemons)
            while num > 0 and len(pokes_lst) > 0:
                poke, max_value = -1, -math.inf
                for pokemon in pokes_lst:
                    if pokemon.value > max_value:
                        max_value = pokemon.value
                        poke = pokemon
                pokes_lst.remove(poke)
                src, dest = self.model.get_poke_edge(poke)
                fnd = self.graph.key_nodes.get(src)
                loc = Location(float(fnd.pos[0]), float(fnd.pos[1]), float(fnd.pos[2]))
                agent = Agent(num - 1, 0, src, -1, 1, loc)
                booly = self.client.add_agent("{\"id\":%d}" % src)
                # self.agents.append(agent)
                num -= 1
            while num > 0:
                fnd = self.graph.key_nodes.get(num)
                loc = Location(float(fnd.pos[0]), float(fnd.pos[1]), float(fnd.pos[2]))
                agent = Agent(num - 1, 0, num - 1, -1, 1, loc)
                self.client.add_agent("{\"id\":%d}" % num - 1)
                # self.agents.append(agent)
                num -= 1
        else:
            for x in range(num):
                fnd = self.graph.key_nodes.get(x)
                loc = Location(float(fnd.pos[0]), float(fnd.pos[1]), float(fnd.pos[2]))
                agent = Agent(x, 0, x, -1, 1, loc)
                self.client.add_agent("{\"id\":%d}" % x)
                self.agents.append(agent)

    def get_params(self):
        """
        this function ask from the server the information of the game and extract from this information the
         following details:
         the current score, the number of moves made until now and the remaining time to this game.
        """
        string = self.client.get_info()
        string = string[14:len(string) - 1]
        client_dict = json.loads(string)
        points, moves = str(client_dict.get("grade")), str(client_dict.get("moves"))
        time_left = str(int(int(self.client.time_to_end()) / 1000))
        return points, moves, time_left

    def button_control(self):
        img = pygame.image.load('stop.png').convert_alpha()
        img2 = pygame.image.load('stop_on.png').convert_alpha()
        rect = img.get_rect(topleft=(5, 75))
        while 1 == 1:  # self.client.is_running():
            # pos = self.gui.pygame.mouse.get_pos()
            pos = pygame.mouse.get_pos()
            # print(pos)
            if rect.collidepoint(pos):
                print("on the stop button")
                self.gui.screen.blit(img2, (5, 75))
                if pygame.mouse.get_pressed()[0] == 1:
                    print("clicked stop")
                    pygame.time.wait(250)
                    pygame.quit()
                    self.client.stop_connection()
                    exit(0)
            else:
                self.gui.screen.blit(img, (5, 75))

    def start_control(self):
        while self.client.is_running():
            self.load_pokemons()
            self.load_agents()
            self.model.update(self.agents, self.pokemons, self.flag)
            p, m, t = self.get_params()
            self.gui.update(self.agents, self.pokemons, p, m, t)
            self.complex_move_agents()
            time.sleep(self.refresh_time)
            self.client.move()

    def start_reg(self):
        """
         this function start the game and in a while loop it asks from the server for the updated data and pass it
         to the model (to allocate new agents if we need to) and to the gui.
         then its waiting the amount of time needed until the next update have to be made and move the agents.
         """
        self.client.start()
        thread1 = threading.Thread(target=self.start_control)
        thread2 = threading.Thread(target=self.button_control)
        thread1.start()
        # thread2.start()

    def tmp_start(self):
        self.client.start()
        while self.client.is_running():
            self.load_pokemons()
            self.load_agents()
            self.model.update(self.agents, self.pokemons, self.flag)
            p, m, t = self.get_params()
            self.gui.update(self.agents, self.pokemons, p, m, t)
            self.complex_move_agents()
            time.sleep(self.refresh_time)
            self.client.move()

    def complex_move_agents(self):
        """
       this function go over the agent list and tell them what is their next destination if they are waiting for
       instructions.
       then it calculates the time the program have to wait untill the next call to "move" by going over the
       agents and check which one will arrive to his next node or his pokemon the fastest. than it updates the
       times of each agent.
       """
        for agent in self.agents:
            # if len(agent.path) == 0 or agent.time2poke <= 0:
            #     agent.pokemons = []
            if len(agent.path) > 0:
                if agent.curr_node == agent.path[0]:
                    agent.path.__delitem__(0)
            if agent.dest == -1 and len(agent.path) > 0:
                next_node = agent.path[0]

                src_nd = self.graph.key_nodes.get(agent.src)
                edge_speed = src_nd.child_weight.get(next_node)
                time_to_dest = (edge_speed / agent.speed)

                agent.curr_node = next_node
                agent.time2curr_dest = time_to_dest
                agent.path.__delitem__(0)

                self.client.choose_next_edge(
                    '{"agent_id":' + str(agent.key) + ', "next_node_id":' + str(next_node) + '}')
                ttl = self.client.time_to_end()
                print(ttl, self.client.get_info())

        min_time2dest = math.inf
        for agent in self.agents:
            lst = [agent.time2curr_dest]
            if len(agent.time2pokes) > 0:
                lst.append(agent.time2pokes[0])
            if len(agent.time2final_dests) > 0:
                lst.append(agent.time2final_dests[0])
            min_measure = min(lst)
            min_time2dest = min(min_time2dest, min_measure)
        print()
        if min_time2dest <= 0:
            min_time2dest = 0.100
        for agent in self.agents:
            for i in range(len(agent.time2pokes)):
                # if len(agent.time2pokes) == len(agent.time2final_dests):
                agent.time2pokes[i] -= min_time2dest
            while len(agent.time2pokes) > 0 and agent.time2pokes[0] <= 0.0000000000001:
                agent.time2pokes.__delitem__(0)
                agent.pokemons.__delitem__(0)
            for i in range(len(agent.time2final_dests)):
                agent.time2final_dests[i] -= min_time2dest
            while len(agent.time2final_dests) > 0 and agent.time2final_dests[0] <= 0.0000000000001:
                agent.time2final_dests.__delitem__(0)
                # agent.dests_lst.__delitem__(0)
            agent.time2curr_dest -= min_time2dest
        self.refresh_time = min_time2dest

    # def start_reg(self):
    #     self.client.start()
    #     thread1 = threading.Thread(target=self.start_control)
    #     thread2 = threading.Thread(target=self.gui.update)
    #     thread1.start()
    #     thread2.start()
    #
    # def start_control(self):
    #     while self.client.is_running():
    #         self.load_pokemons()
    #         self.load_agents()
    #         self.model.update(self.agents, self.pokemons, self.flag)
    #         self.model.update(self.agents, self.pokemons, self.flag)

    # def start3(self):  # with stop button
    #     self.client.start()
    #     img = pygame.image.load('stop.png').convert_alpha()
    #     rect = img.get_rect(topleft=(5, 75))
    #     while self.client.is_running():
    #         pos = pygame.mouse.get_pos()
    #         # print(pos)
    #         if rect.collidepoint(pos):
    #             # print("on the stop button")
    #             while pygame.mouse.get_pressed()[0] == 1:
    #                 print("clicked stop")
    #                 pygame.time.wait(250)
    #                 pygame.quit()
    #                 exit(0)
    #         # if pygame.mouse.get_pressed()[0] == 0:
    #         # clicked = False
    #         # running = False
    #         self.load_pokemons()
    #         self.load_agents()
    #         for pokemon in self.pokemons:
    #             if pokemon.agent_aloc == -1:
    #                 if self.flag == 1:
    #                     self.allocate_agent_1(pokemon)
    #                 else:
    #                     self.allocate_agent_0(pokemon)
    #         self.complex_move_agents()
    #         pygame.time.wait(1400)
    #         # self.clock.tick(10)
    #         self.client.move()
    #         self.update_gui()
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 exit(0)


if __name__ == '__main__':
    c = Control()
    c.load()
    c.tmp_start()
