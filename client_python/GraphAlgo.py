import math
import queue
import json
import GraphInterface
from DiGraph import DiGraph
from Loc_Node_Edge import Node, Location


class GraphAlgo:
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

    def shortest_path(self, id1: int, id2: int, agent_speed) -> (float, list):
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
                curr_weghit = edge[1]
                if visited.get(curr_dest) is not None:
                    continue
                curr_time = times.get(curr_dest)
                tmp_time = (curr_weghit / agent_speed)
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

    def dijkstra(self, src, agent_speed) -> (tuple, dict, dict):
        """
        this function is an implementation of Dijkstra's Algorithm using PriorityQueue.
        it returns 3 things:
        distances - dictionary that contains the distance of each node in the graph from the source node.
        previous - dictionary that contains the previous node of each node in the graph in the path from the source node.
        ans - tuple that contains the maximum distance from a node and the src id.
        """
        times = dict()
        visited = dict()
        previous = dict()
        keys = self.graph.key_nodes.copy()
        pq = queue.PriorityQueue()
        for key in keys.keys():
            times[key] = math.inf
        times[src] = 0
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
                curr_weghit = edge[1]
                if visited.get(curr_dest) is not None:
                    continue
                curr_time = times.get(curr_dest)
                tmp_time = (curr_weghit / agent_speed)
                new_time = times.get(curr_key) + tmp_time
                if new_time < curr_time:
                    times[curr_dest] = new_time
                    previous[curr_dest] = curr_key
                pq.put((times.get(curr_dest), curr_dest))
        maximum = -math.inf
        max_id = -1
        for key in keys.keys():
            if times.get(key) > maximum and times.get(key) != math.inf:
                maximum = times.get(key)
                max_id = key
        ans = (maximum, src)
        return ans, times, previous

    def load_from_json(self, path):
        with open(path, 'r') as graph_json_str:
            graph_jobj = json.load(graph_json_str)
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
