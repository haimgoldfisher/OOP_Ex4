from types import SimpleNamespace
from client import Client
import json
# from pygame import gfxdraw
# import pygame
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

    def load(self):
        PORT = 6666
        HOST = '127.0.0.1'
        self.client.start_connection(HOST, PORT)
        self.load_pokemons()
        # self.load_agents()
        self.load_graph()

    def load_pokemons(self):
        pokemons_json_str = self.client.get_pokemons()
        pokemons_jobj = json.loads(pokemons_json_str)
        pokemons_lst = pokemons_jobj.get("Pokemons")
        for p in pokemons_lst:
            p_data = p.get("Pokemon")
            value = p_data.get("value")
            typ = p_data.get("type")
            pos = p_data.get("pos")
            pos = pos.split(",")
            loc = Location(pos[0], pos[1], pos[2])
            pokemon = Pokemon(value, typ, loc)
            self.pokemons.append(pokemon)

    def load_agents(self):
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
            loc = Location(pos[0], pos[1], pos[2])
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


if __name__ == '__main__':
    mg = MyGame()
    mg.load()
