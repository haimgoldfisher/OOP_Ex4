import copy
import itertools
import math
import queue
from random import random, randrange
from typing import List
import json
from matplotlib import patheffects
import GraphInterface
from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph
from Loc_Node_Edge import Node, Location
import matplotlib.pyplot as plt


class GraphAlgo(GraphAlgoInterface):
    """
    this class represent a set of algorithms of graphs. it contains only 1 thing:
    graph - the graph the algorithms will be used on.
    """
    def __init__(self, *args) -> None:
        if len(args) == 1:
            self.graph = args[0]
        else:
            self.graph = DiGraph()

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
        """
        try:
            if not file_name.endswith('.json'):
                file_name += ".json"
            with open(file_name, 'r') as json_file:
                jobj = json.load(json_file)
                edges = jobj.get("Edges")
                nodes = jobj.get("Nodes")
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
                return True
        except FileExistsError as err:
            print(err)
            return False

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """
        try:
            if not file_name.endswith('.json'):
                file_name += ".json"
            with open(file_name, "w") as output_file:
                edge_node_dicts = {"Edges": [], "Nodes": []}
                for src in self.graph.key_nodes:
                    node = self.graph.key_nodes.get(src)
                    if node.pos is not None:  # for T0 case
                        loc = str(node.pos[0]) + "," + str(node.pos[1]) + "," + str(node.pos[2])
                        edge_node_dicts["Nodes"].append({"pos": loc, "id": node.key})
                    else:
                        edge_node_dicts["Nodes"].append({"id": src})
                    for dest, weight in self.graph.all_out_edges_of_node(src).items():
                        edge_node_dicts["Edges"].append({"src": src, "w": weight, "dest": dest})
                json_size = len(edge_node_dicts)
                output = json.dumps(edge_node_dicts, indent=json_size)
                output_file.write(output)
                output_file.close()
                return True
        except IOError as err:
            print(err)
            output_file.close()
            return False

    def reverse(self, graph) -> DiGraph:
        """
        this function create a new graph which is the reverse the given graph.
        its used as helper function for isConnected function.
        @return - new reversed graph
        """
        ans = copy.deepcopy(graph)
        new_edges_list = list()
        for nd in ans.key_nodes.values():
            for edge_data in nd.child_weight.items():
                x = (edge_data[0], nd.key, edge_data[1])
                new_edges_list.append(x)
            nd.child_weight.clear()
            nd.parent_weight.clear()
        ans.edge_counter = 0
        for edge_data in new_edges_list:
            ans.add_edge(edge_data[0], edge_data[1], edge_data[2])
        return ans

    def isConnected(self) -> bool:
        """
        this function checks if the graph is strongly connected by running dfs on the graph
        and on its reversed graph if in each dfs the amount of nodes visited equals to the
        amount of node in this graph then the graph is connected.
        @return - True if it is and False otherwise.
        """
        keys = list(self.graph.key_nodes.keys())
        key = keys[0]
        visited = self.graph.my_dfs(key)
        if visited != self.graph.v_size():
            return False
        g_copy = copy.deepcopy(self.graph)
        reversed_g = self.reverse(g_copy)
        visited = reversed_g.my_dfs(key)
        if visited != self.graph.v_size():
            return False
        return True

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
        distances = dict()
        visited = dict()
        keys = self.graph.key_nodes.copy()
        pq = queue.PriorityQueue()
        for key in keys.keys():
            distances[key] = math.inf
        distances[id1] = 0
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
                weight = edge[1]
                if visited.get(curr_dest) is not None:
                    continue
                curr_weight = distances.get(curr_dest)
                new_weight = distances.get(curr_key) + weight
                if new_weight < curr_weight:
                    distances[curr_dest] = new_weight
                    previous[curr_dest] = curr_key
                pq.put((distances.get(curr_dest), curr_dest))
        if distances.get(id2) == math.inf:
            return math.inf, []
        curr = id2
        while curr != id1:
            path.insert(0, curr)
            curr = previous.get(curr)
        path.insert(0, id1)
        dist = distances.get(id2)
        return dist, path  # distance

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """
       Finds the shortest path that visits all the nodes in the list.
       this function runs Dijkstra's Algorithm for each node in the list and saves its results.
       then it creates all the permutations of the given list and checks which permutation
       gives the minimum weight.
       :param node_lst: A list of nodes id's
       :return: A list of the nodes id's in the path, and the overall distance
       """
        id_distances = {}
        id_previous = {}
        for node_id in node_lst:
            ans, curr_distances, curr_previous = self.dijkstra(node_id)
            id_distances[node_id] = curr_distances
            id_previous[node_id] = curr_previous
        min_path_dist = math.inf
        min_path = []
        all_perms = itertools.permutations(node_lst)
        for perm in all_perms:
            curr_path_weight = 0
            for i in range(len(perm) - 1):
                curr_path_weight += id_distances.get(perm[i]).get(perm[i + 1])
            if curr_path_weight < min_path_dist:
                min_path_dist = curr_path_weight
                min_path = perm
        full_min_path = []
        for i in range(len(min_path) - 1):
            id1 = min_path[i]
            id2 = min_path[i + 1]
            curr_previous = id_previous.get(id1)
            curr = id2
            ppath = []
            while curr != id1:
                ppath.insert(0, curr)
                curr = curr_previous.get(curr)
            full_min_path += ppath
        full_min_path.insert(0, min_path[0])
        return full_min_path, min_path_dist

    def centerPoint(self) -> (int, float):
        """
       Finds the node that has the shortest distance to it's farthest node.
       :return: The nodes id, min-maximum distance
       """
        if not self.isConnected():
            return None, float('inf')
        e = dict()
        lst = []
        for src in self.graph.key_nodes.keys():
            curr_maximum_src, distances, previous = self.dijkstra(src)
            lst.append(curr_maximum_src)
        max_min = min(lst)
        max_min_dist = max_min[0]
        key = max_min[1]
        # nd = self.graph.key_nodes.get(key)
        return key, max_min_dist

    def dijkstra(self, src) -> (tuple, dict, dict):
        """
        this function is an implementation of Dijkstra's Algorithm using PriorityQueue.
        it returns 3 things:
        distances - dictionary that contains the distance of each node in the graph from the source node.
        previous - dictionary that contains the previous node of each node in the graph in the path from the source node.
        ans - tuple that contains the maximum distance from a node and the src id.
        """
        distances = dict()
        visited = dict()
        previous = dict()
        keys = self.graph.key_nodes.copy()
        pq = queue.PriorityQueue()
        for key in keys.keys():
            distances[key] = math.inf
        distances[src] = 0
        pq.put((0, src))
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
                weight = edge[1]
                if visited.get(curr_dest) is not None:
                    continue
                curr_weight = distances.get(curr_dest)
                new_weight = distances.get(curr_key) + weight
                if new_weight < curr_weight:
                    distances[curr_dest] = new_weight
                    previous[curr_dest] = curr_key
                pq.put((distances.get(curr_dest), curr_dest))
        maximum = -math.inf
        max_id = -1
        for key in keys.keys():
            if distances.get(key) > maximum and distances.get(key) != math.inf:
                maximum = distances.get(key)
                max_id = key
        ans = (maximum, src)
        return ans, distances, previous

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        nodes = list(self.get_graph().get_all_v().values())
        for node in nodes:
            x1, y1 = float(node.pos[0]), float(node.pos[1])
            plt.plot(x1, y1, marker='o', markersize=20,  color='c')
            edge_nodes = list(self.graph.all_out_edges_of_node(node.key).keys())
            for key in edge_nodes:
                dest_node = self.graph.key_nodes.get(key)
                x2, y2 = float(dest_node.pos[0]), float(dest_node.pos[1])
                plt.annotate(None, xy=[x2, y2], xytext=[x1, y1], arrowprops=dict(facecolor='black', shrink=0.04, width=0.5, headwidth=8, headlength=6))
            plt.text(x1, y1, str(node.key), color='r', fontsize=16, path_effects=[patheffects.withStroke(linewidth=3, foreground='black')])
        plt.show()

    def init_random(self, zeroes: int) -> None:
        """
        Init a random graph with 10^n nodes
        each node has 10 edges which go from it, so we
        can say that the average degree of the nodes is 20 (in+out)
        @return: None
        """
        num_of_nodes = int(math.pow(10, zeroes))
        rand_g = DiGraph()
        for i in range(num_of_nodes):
            x, y = 35+random(), 32 + random()
            loc = (x, y, 0)
            rand_g.add_node(i, loc)
        for n in range(num_of_nodes):
            scale = 2
            if zeroes > 1:
                scale = 10
            rand_g.add_edge(n, (n+1) % num_of_nodes, 1 + random()) # for connected graph
            for e in range(1, scale):
                dest = randrange(0, num_of_nodes)
                w = 1 + random()
                while n == dest or rand_g.all_out_edges_of_node(n).get(dest) is not None:
                    dest = randrange(0, num_of_nodes) # so n is not e
                rand_g.add_edge(n, dest, w)
        self.graph = rand_g


if __name__ == '__main__':
    g = GraphAlgo()
    g.load_from_json("../data/A0.json")
    print(g.graph)
    print(g.isConnected())
    print(g.centerPoint())
    g.plot_graph()
    #print(g.shortest_path(0,42))
    print(g.TSP([0, 5,4,9]))
    print("H")
    g.save_to_json("out")