import copy
import itertools
import math

from client_python.Agent import Agent
from client_python.DiGraph import DiGraph
from client_python.GraphAlgo import GraphAlgo


class Model:

    def __init__(self):
        # self.pokemons = []
        # self.agents = []
        self.graph = DiGraph()
        self.graph_algo = GraphAlgo(self.graph)
        self.flag = 0

    def first_update(self, agents, pokemons, graph_algo):
        self.graph_algo = graph_algo
        self.graph = graph_algo.graph
        # self.update(agents, pokemons)

    def update(self, agents, pokemons):
        for pokemon in pokemons:
            if pokemon.agent_aloc == -1:
                self.allocate_agent_0___3(agents, pokemon)

    def allocate_agent_0(self, agents, pokemon):
        min_time2poke = math.inf
        time2fdest = 0
        min_path = []
        chosen_agent = None
        agent_key = -1
        min_val = math.inf
        for agent in agents:
            src, dest = self.get_poke_edge(pokemon)
            if self.bet_ag_dest(agent, pokemon, src, dest):
                t = self.calc_time_same_edge(agent, pokemon, src, dest)
                agent.time2pokes.insert(0, t)
                agent.pokemons.insert(0, pokemon)
                agent_key = agent.key
                chosen_agent = None
                break
            done = False
            for index, value in enumerate(agent.path):
                if value == src and index + 1 < len(agent.path):
                    if agent.path[index + 1] == dest:
                        tp, td = self.calc_time_on_path(agent, pokemon, src, dest)
                        i = 0
                        while i < len(agent.time2pokes):
                            if tp < agent.time2pokes[i]:
                                break
                            i += 1
                        agent.time2pokes.insert(i, tp)
                        agent.pokemons.insert(i, pokemon)
                        i = 0
                        while i < len(agent.time2final_dests):
                            if tp < agent.time2final_dests[i]:
                                break
                            i += 1
                        agent.time2final_dests.insert(i, td)
                        # agent.dests_lst.insert(i, (src, dest))
                        agent_key = agent.key
                        chosen_agent = None
                        done = True
                        break
            if done:
                break
            curr_time2poke, path, curr_time2fdest, curr_val = self.calc_time(agent, pokemon)
            # if curr_val < min_val:
            #     min_time2poke = curr_time2poke
            #     min_path = copy.copy(path)
            #     time2fdest = curr_time2fdest
            #     agent_key = agent.key
            #     chosen_agent = agent
            #     min_val = curr_val

            if curr_time2poke < min_time2poke:
                min_time2poke = curr_time2poke
                min_path = copy.copy(path)
                time2fdest = curr_time2fdest
                agent_key = agent.key
                chosen_agent = agent

        if chosen_agent is not None:
            chosen_agent.time2pokes.append(min_time2poke)
            chosen_agent.time2final_dests.append(time2fdest)
            chosen_agent.path += min_path
            chosen_agent.pokemons.append(pokemon)
            # chosen_agent.dests_lst.append((min_path[len(min_path)-2], min_path[len(min_path)-1]))
        pokemon.agent_aloc = agent_key
        return agent_key

    def allocate_agent_1(self, pokemon):
        min_time2poke = math.inf
        time2fdest = 0
        min_path = []
        chosen_agent = None
        agent_key = -1
        calc_flag = 0
        for agent in self.agents:
            src, dest = self.get_poke_edge(pokemon)
            if self.bet_ag_dest(agent, pokemon, src, dest):
                agent_key = agent.key
                chosen_agent = None
                break
            done = False
            for index, value in enumerate(agent.path):
                if value == src and index + 1 < len(agent.path):
                    if agent.path[index + 1] == dest:
                        agent_key = agent.key
                        chosen_agent = None
                        done = True
                        break
            if done:
                break
            if len(agent.pokemons) + 1 > 1:
                curr_time2poke, path, curr_time2fdest = self.calc_time_tsp(agent, pokemon)
                flag = 1
            else:
                curr_time2poke, path, curr_time2fdest = self.calc_time(agent, pokemon)
                flag = 0
            if curr_time2poke < min_time2poke:
                min_time2poke = curr_time2poke
                min_path = copy.copy(path)
                time2fdest = curr_time2fdest
                agent_key = agent.key
                chosen_agent = agent
                calc_flag = flag

        if chosen_agent is not None:
            chosen_agent.time2poke = min_time2poke
            chosen_agent.time2final_dest = time2fdest
            if calc_flag == 1:
                chosen_agent.path = min_path
                chosen_agent.pokemons = [pokemon]
            if calc_flag == 0:
                chosen_agent.path += min_path
                chosen_agent.pokemons.append(pokemon)
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
            if x1 < poke_pos.x < x2 or x1 > poke_pos.x > x2:
                if y1 < poke_pos.y < y2 or y1 > poke_pos.y > y2:
                    if pokemon.type > 0 and src < dest:
                        return True
                    if pokemon.type < 0 and src > dest:
                        return True

        return False

    def calc_time_on_path(self, agent, pokemon, src, dest):
        curr_dest = agent.curr_node  ################ maybe a problem
        path_time, path = self.graph_algo.shortest_path(curr_dest, src, agent.speed)
        path.append(dest)
        # path_time += agent.time2final_dest

        src_nd = self.graph.key_nodes.get(src)
        dest_nd = self.graph.key_nodes.get(dest)
        edge_speed = src_nd.child_weight.get(dest)

        x_squared = (pokemon.pos.x - float(src_nd.pos[0])) * (pokemon.pos.x - float(src_nd.pos[0]))
        y_squared = (pokemon.pos.y - float(src_nd.pos[1])) * (pokemon.pos.y - float(src_nd.pos[1]))
        dist_src2poke = math.sqrt(x_squared + y_squared)  # src to pokemon

        x_squared = (float(dest_nd.pos[0]) - float(src_nd.pos[0])) * (float(dest_nd.pos[0]) - float(src_nd.pos[0]))
        y_squared = (float(dest_nd.pos[1]) - float(src_nd.pos[1])) * (float(dest_nd.pos[1]) - float(src_nd.pos[1]))
        dist_src2dest = math.sqrt(x_squared + y_squared)  # src to dest

        relation = dist_src2poke / dist_src2dest
        scaled_poke_pos = relation * edge_speed
        time_to_poke = path_time + (scaled_poke_pos / agent.speed)
        time_to_fdest = path_time + (edge_speed / agent.speed)
        time_to_poke += agent.time2curr_dest
        time_to_fdest += agent.time2curr_dest
        return time_to_poke, time_to_fdest

    def calc_time_same_edge(self, agent, pokemon, src, dest):
        src_nd = self.graph.key_nodes.get(src)
        dest_nd = self.graph.key_nodes.get(dest)
        edge_speed = src_nd.child_weight.get(agent.dest)
        x_squared = (pokemon.pos.x - agent.pos.x) * (pokemon.pos.x - agent.pos.x)
        y_squared = (pokemon.pos.y - agent.pos.y) * (pokemon.pos.y - agent.pos.y)
        dist_src2poke = math.sqrt(x_squared + y_squared)  # src to pokemon

        x_squared = (float(dest_nd.pos[0]) - float(src_nd.pos[0])) * (float(dest_nd.pos[0]) - float(src_nd.pos[0]))
        y_squared = (float(dest_nd.pos[1]) - float(src_nd.pos[1])) * (float(dest_nd.pos[1]) - float(src_nd.pos[1]))
        dist_src2dest = math.sqrt(x_squared + y_squared)  # src to dest

        relation = dist_src2poke / dist_src2dest
        scaled_poke_pos = relation * edge_speed
        time_to_poke = (scaled_poke_pos / agent.speed)
        return time_to_poke


    def calc_time(self, agent, pokemon):
        src, dest = self.get_poke_edge(pokemon)
        curr_dest = agent.curr_node  ################ maybe a problem
        if len(agent.path) > 0:
            curr_dest = agent.path[len(agent.path) - 1]
        path_time, path = self.graph_algo.shortest_path(curr_dest, src, agent.speed)
        path.append(dest)
        # path_time += agent.time2final_dest

        src_nd = self.graph.key_nodes.get(src)
        dest_nd = self.graph.key_nodes.get(dest)
        edge_speed = src_nd.child_weight.get(dest)  # weghit

        x_squared = (pokemon.pos.x - float(src_nd.pos[0])) * (pokemon.pos.x - float(src_nd.pos[0]))
        y_squared = (pokemon.pos.y - float(src_nd.pos[1])) * (pokemon.pos.y - float(src_nd.pos[1]))
        dist_src2poke = math.sqrt(x_squared + y_squared)  # src to pokemon

        x_squared = (float(dest_nd.pos[0]) - float(src_nd.pos[0])) * (float(dest_nd.pos[0]) - float(src_nd.pos[0]))
        y_squared = (float(dest_nd.pos[1]) - float(src_nd.pos[1])) * (float(dest_nd.pos[1]) - float(src_nd.pos[1]))
        dist_src2dest = math.sqrt(x_squared + y_squared)  # src to dest

        relation = dist_src2poke / dist_src2dest
        scaled_poke_pos = relation * edge_speed
        time_to_poke = path_time + (scaled_poke_pos / agent.speed)
        time_to_fdest = path_time + (edge_speed / agent.speed)
        if len(agent.time2final_dests) > 0:
            time_to_poke += agent.time2final_dests[len(agent.time2final_dests)-1]
            time_to_fdest += agent.time2final_dests[len(agent.time2final_dests)-1]
        val = time_to_poke / pokemon.value

        return time_to_poke, path, time_to_fdest,val

    def calc_time_rev(self, agent, pokemon):
        tmp_agent = Agent(-1, agent.value, agent.src, agent.dest, agent.speed, agent.pos)
        tmp_agent.time2final_dests.append(agent.time2final_dests[0])
        curr_time2poke, path, curr_time2fdest, curr_val = self.calc_time(tmp_agent, pokemon)
        # curr_time2poke += agent.time2curr_dest
        # curr_time2fdest += agent.time2curr_dest
        tmp_agent.time2pokes.append(curr_time2poke)
        tmp_agent.time2final_dests.append(curr_time2fdest)
        tmp_agent.path += path
        tmp_agent.pokemons.append(pokemon)
        # tmp_agent.dests_lst.append((path[len(path) - 2], path[len(path) - 1]))
        for curr_pokemon in agent.pokemons:
            curr_time2poke, path, curr_time2fdest, curr_val = self.calc_time(tmp_agent, curr_pokemon)
            tmp_agent.time2pokes.append(curr_time2poke)
            tmp_agent.time2final_dests.append(curr_time2fdest)
            tmp_agent.path += path
            tmp_agent.pokemons.append(curr_pokemon)
            # tmp_agent.dests_lst.append((path[len(path) - 2], path[len(path) - 1]))
        return tmp_agent

    def allocate_agent_0___3(self, agents, pokemon):
        min_time2poke = math.inf
        time2fdest = 0
        min_path = []
        chosen_agent = None
        agent_key = -1
        min_val = math.inf
        min_flag = 0
        min_tmp_agent = None
        for agent in agents:
            src, dest = self.get_poke_edge(pokemon)
            if self.bet_ag_dest(agent, pokemon, src, dest):
                t = self.calc_time_same_edge(agent, pokemon, src, dest)
                agent.time2pokes.insert(0, t)
                agent.pokemons.insert(0, pokemon)
                agent_key = agent.key
                chosen_agent = None
                break
            done = False
            for index, value in enumerate(agent.path):
                if value == src and index + 1 < len(agent.path):
                    if agent.path[index + 1] == dest:
                        tp, td = self.calc_time_on_path(agent, pokemon, src, dest)
                        i = 0
                        while i < len(agent.time2pokes):
                            if tp < agent.time2pokes[i]:
                                break
                            i += 1
                        agent.time2pokes.insert(i, tp)
                        agent.pokemons.insert(i, pokemon)
                        i = 0
                        while i < len(agent.time2final_dests):
                            if tp < agent.time2final_dests[i]:
                                break
                            i += 1
                        agent.time2final_dests.insert(i, td)
                        # agent.dests_lst.insert(i, (src, dest))
                        agent_key = agent.key
                        chosen_agent = None
                        done = True
                        break
            if done:
                break
            curr_time2poke, path, curr_time2fdest, curr_val = self.calc_time(agent, pokemon)
            curr_flag = 0
            tmp_agent = None
            if len(agent.pokemons) >= 1:
                tmp_agent = self.calc_time_rev(agent,pokemon)
                if tmp_agent.time2pokes[len(tmp_agent.time2pokes)-1] < curr_time2poke:
                    curr_flag = 1
                    curr_time2poke = tmp_agent.time2pokes[len(tmp_agent.time2pokes)-1]
                    path = tmp_agent.path
                    curr_time2fdest = agent.time2final_dests
            if curr_time2poke < min_time2poke:
                min_time2poke = curr_time2poke
                min_path = copy.copy(path)
                time2fdest = curr_time2fdest
                agent_key = agent.key
                chosen_agent = agent
                if curr_flag == 0:
                    min_flag = 0
                else:
                    min_flag = 1
                    min_tmp_agent = tmp_agent

        if chosen_agent is not None:
            if min_flag == 0:
                chosen_agent.time2pokes.append(min_time2poke)
                chosen_agent.time2final_dests.append(time2fdest)
                chosen_agent.path += min_path
                chosen_agent.pokemons.append(pokemon)
                # chosen_agent.dests_lst.append((min_path[len(min_path)-2], min_path[len(min_path)-1]))
            else:
                chosen_agent.time2pokes = copy.copy(min_tmp_agent.time2pokes)
                chosen_agent.time2final_dests = copy.copy(min_tmp_agent.time2final_dests)
                chosen_agent.path = copy.copy(min_tmp_agent.path)
                chosen_agent.pokemons = copy.copy(min_tmp_agent.pokemons)
                # chosen_agent.dests_lst = copy.copy(min_tmp_agent.dests_lst)

        pokemon.agent_aloc = agent_key
        return agent_key



    # def calc_time_tsp_new(self, agent, new_pokemon):
    #     total_time2poke1, total_path1, total_path_time1, val1 = self.calc_time(agent,new_pokemon)
    #     src1, dest1 = self.get_poke_edge(new_pokemon)
    #     curr_node = agent.curr_node
    #     # if len(agent.path) > 0:
    #     #     curr_dest = agent.path[len(agent.path)-1]
    #     path_time1, path1 = self.graph_algo.shortest_path(curr_node, src1, agent.speed)
    #     path1.append(dest1)
    #
    #     src_nd1 = self.graph.key_nodes.get(src1)
    #     dest_nd1 = self.graph.key_nodes.get(dest1)
    #     edge_speed1 = src_nd1.child_weight.get(dest1)  # weghit
    #
    #     x_squared = (new_pokemon.pos.x - float(src_nd1.pos[0])) * (new_pokemon.pos.x - float(src_nd1.pos[0]))
    #     y_squared = (new_pokemon.pos.y - float(src_nd1.pos[1])) * (new_pokemon.pos.y - float(src_nd1.pos[1]))
    #     dist_src2poke1 = math.sqrt(x_squared + y_squared)  # src to pokemon
    #
    #     x_squared = (float(dest_nd1.pos[0]) - float(src_nd1.pos[0])) * (float(dest_nd1.pos[0]) - float(src_nd1.pos[0]))
    #     y_squared = (float(dest_nd1.pos[1]) - float(src_nd1.pos[1])) * (float(dest_nd1.pos[1]) - float(src_nd1.pos[1]))
    #     dist_src2dest1 = math.sqrt(x_squared + y_squared)  # src to dest
    #
    #     relation1 = dist_src2poke1 / dist_src2dest1
    #     scaled_poke_pos1 = relation1 * edge_speed1
    #     time_to_poke1 = path_time1 + (scaled_poke_pos1 / agent.speed)
    #     time_to_fdest1 = path_time1 + (edge_speed1 / agent.speed)
    #
    #
    #
    #     # src2 = agent.dests_lst[0][0]
    #     # dest2 = agent.dests_lst[0][1]
    #     pokemon2 = agent.pokemons[0]
    #
    #     path_time2, path2 = self.graph_algo.shortest_path(dest1, src2, agent.speed)
    #
    #     src_nd2 = self.graph.key_nodes.get(src2)
    #     dest_nd2 = self.graph.key_nodes.get(dest2)
    #     edge_speed2 = src_nd2.child_weight.get(dest2)
    #
    #     x_squared = (pokemon2.pos.x - float(src_nd2.pos[0])) * (pokemon2.pos.x - float(src_nd2.pos[0]))
    #     y_squared = (pokemon2.pos.y - float(src_nd2.pos[1])) * (pokemon2.pos.y - float(src_nd2.pos[1]))
    #     dist_src2poke2 = math.sqrt(x_squared + y_squared)  # src to pokemon
    #
    #     x_squared = (float(dest_nd2.pos[0]) - float(src_nd2.pos[0])) * (float(dest_nd2.pos[0]) - float(src_nd2.pos[0]))
    #     y_squared = (float(dest_nd2.pos[1]) - float(src_nd2.pos[1])) * (float(dest_nd2.pos[1]) - float(src_nd2.pos[1]))
    #     dist_src2dest2 = math.sqrt(x_squared + y_squared)  # src to dest
    #
    #     relation2 = dist_src2poke2 / dist_src2dest2
    #     scaled_poke_pos2 = relation2 * edge_speed2
    #     time_to_poke2 = time_to_fdest1 + path_time2 + (scaled_poke_pos2 / agent.speed)
    #     time_to_fdest2 = time_to_fdest1 + path_time2 + (edge_speed2 / agent.speed)
    #
    #     total_path_time2 = time_to_fdest2 + (agent.time2final_dests[len(agent.time2final_dests) - 1] - agent.time2final_dests[0])
    #     total_time2poke2 = time_to_fdest2 + (agent.time2pokes[len(agent.time2pokes) - 1] - agent.time2final_dests[0])
    #
    #
    #     rest_path = []
    #     for index, value in enumerate(agent.path):
    #         if value == src2 and index + 1 < len(agent.path):
    #             if agent.path[index + 1] == dest2:
    #                 rest_path = agent.path[index + 1:]
    #     total_path2 = path1 + path2 + rest_path
    #
    #     if total_time2poke1 < total_time2poke2:
    #         self.flag = 1
    #         return total_time2poke1, total_path1, total_path_time1
    #     else:
    #         self.flag = 2
    #         time_to_pokes = [time_to_poke1,time_to_poke2]
    #         time_to_dests = [time_to_fdest1,time_to_fdest2]
    #         pokes = [new_pokemon,pokemon2]
    #         src_dest = (src1,dest1)
    #         return total_time2poke2, total_path2, total_path_time2, src_dest, time_to_pokes, time_to_dests
    #
    # def allocate_agent_0___2(self, agents, pokemon):
    #     min_time2poke = math.inf
    #     time2fdest = 0
    #     min_path = []
    #     chosen_agent = None
    #     agent_key = -1
    #     min_val = math.inf
    #     min_flag = 1
    #     d = 0
    #     ttp = []
    #     ttd = []
    #     for agent in agents:
    #         src, dest = self.get_poke_edge(pokemon)
    #         if self.bet_ag_dest(agent, pokemon, src, dest):
    #             t = self.calc_time_same_edge(agent, pokemon, src, dest)
    #             agent.time2pokes.insert(0, t)
    #             agent.pokemons.insert(0, pokemon)
    #             agent_key = agent.key
    #             chosen_agent = None
    #             break
    #         done = False
    #         for index, value in enumerate(agent.path):
    #             if value == src and index + 1 < len(agent.path):
    #                 if agent.path[index + 1] == dest:
    #                     tp, td = self.calc_time_on_path(agent, pokemon, src, dest)
    #                     agent.time2pokes.insert(0, tp)
    #                     agent.time2final_dests.insert(0, td)
    #                     agent.pokemons.insert(0, pokemon)
    #                     # agent.dests_lst.insert(0, (src, dest))
    #                     agent_key = agent.key
    #                     chosen_agent = None
    #                     done = True
    #                     break
    #         if done:
    #             break
    #         lst = ()
    #         curr_flag = 1
    #         if len(agent.pokemons) == 0:
    #             lst = self.calc_time(agent, pokemon)
    #             curr_flag = 1
    #         else:
    #             lst = self.calc_time_tsp_new(agent, pokemon)
    #             if len(lst) == 3:
    #                 curr_flag = 1
    #             else:
    #                 curr_flag = 2
    #         if lst[0] < min_time2poke:
    #             min_time2poke = lst[0]
    #             min_path = copy.copy(lst[1])
    #             time2fdest = lst[2]
    #             agent_key = agent.key
    #             chosen_agent = agent
    #             if curr_flag == 2:
    #                 min_flag = 2
    #                 d = lst[3]
    #                 ttp = lst[4]
    #                 ttd = lst[5]
    #             else:
    #                 min_flag = 1
    #
    #     if chosen_agent is not None:
    #         if min_flag == 1:
    #             chosen_agent.time2pokes.append(min_time2poke)
    #             chosen_agent.time2final_dests.append(time2fdest)
    #             chosen_agent.path += min_path
    #             chosen_agent.pokemons.append(pokemon)
    #             # chosen_agent.dests_lst.append((min_path[len(min_path)-2], min_path[len(min_path)-1]))
    #         else:
    #             for i in range(len(chosen_agent.time2pokes)):
    #                 chosen_agent.time2pokes[i] -= chosen_agent.time2final_dests[0]
    #             chosen_agent.time2pokes.__delitem__(0)
    #             for i in range(len(chosen_agent.time2final_dests)):
    #                 chosen_agent.time2final_dests[i] -= chosen_agent.time2final_dests[0]
    #             chosen_agent.time2final_dests.__delitem__(0)
    #
    #
    #             for i in range(len(chosen_agent.time2pokes)):
    #                 chosen_agent.time2pokes[i] += ttd[1]
    #             for i in range(len(chosen_agent.time2final_dests)):
    #                 chosen_agent.time2final_dests[i] += ttd[1]
    #             chosen_agent.time2pokes = ttp + chosen_agent.time2pokes
    #             chosen_agent.time2final_dests = ttd + chosen_agent.time2final_dests
    #             chosen_agent.pokemons.insert(0, pokemon)
    #             # chosen_agent.dests_lst.insert(0, d)
    #     pokemon.agent_aloc = agent_key
    #     return agent_key

    # new_dests_lst = copy.copy(agent.dests_lst)
    # new_pokemons_lst = copy.copy(agent.pokemons)
    # new_dests_lst.insert(0,(src,dest))
    #
    # for i in range(len(new_dests_lst)-1):
    #     curr_src1 = new_dests_lst[i][0]
    #     curr_dest1 = new_dests_lst[i][1]
    #     curr_src2 = new_dests_lst[i+1][0]
    #     curr_dest2 = new_dests_lst[i+1][1]
    #     path_time2, path2 = self.graph_algo.shortest_path(curr_dest1, curr_src2, agent.speed)
    #
    #     curr_src_nd = self.graph.key_nodes.get(src)
    #     curr_dest_nd = self.graph.key_nodes.get(dest)
    #     curr_edge_speed = src_nd.child_weight.get(dest)
    #
    # x_squared = (new_pokemon.pos.x - float(src_nd.pos[0])) * (new_pokemon.pos.x - float(src_nd.pos[0]))
    #     y_squared = (new_pokemon.pos.y - float(src_nd.pos[1])) * (new_pokemon.pos.y - float(src_nd.pos[1]))
    #     dist_src2poke = math.sqrt(x_squared + y_squared)  # src to pokemon
    #
    #     x_squared = (float(dest_nd.pos[0]) - float(src_nd.pos[0])) * (float(dest_nd.pos[0]) - float(src_nd.pos[0]))
    #     y_squared = (float(dest_nd.pos[1]) - float(src_nd.pos[1])) * (float(dest_nd.pos[1]) - float(src_nd.pos[1]))
    #     dist_src2dest = math.sqrt(x_squared + y_squared)  # src to dest
    #
    #     relation = dist_src2poke / dist_src2dest
    #     scaled_poke_pos = relation * edge_speed
    #     time_to_poke = path_time + (scaled_poke_pos / agent.speed)
    #     time_to_fdest = path_time + (edge_speed / agent.speed)

    # if len(agent.time2final_dests) > 0:
    #     time_to_poke += agent.time2final_dests[len(agent.time2final_dests) - 1]
    #     time_to_fdest += agent.time2final_dests[len(agent.time2final_dests) - 1]
    # val = time_to_poke / new_pokemon.value

    # new_dests_lst = copy.copy(agent.dests_lst)
    # new_dests_lst.insert(0,(src,dest))
    # new_pokemons_lst = copy.copy(agent.pokemons)
    # new_time2final_dests = agent.time2final_dests
    # new_time2pokes = agent.time2pokes








    #
    #
    # def calc_time_tsp(self, agent, new_pokemon):
    #     id_distances = {}
    #     id_previous = {}
    #     srcs = []
    #     dests = []
    #     curr_dest = agent.curr_node
    #
    #     ans, curr_distances, curr_previous = self.graph_algo.dijkstra(curr_dest, agent.speed)
    #     id_distances[curr_dest] = curr_distances
    #     id_previous[curr_dest] = curr_previous
    #
    #     pokemons = copy.copy(agent.pokemons)
    #     pokemons.append(new_pokemon)
    #
    #     for pokemon in pokemons:
    #         src, dest = self.get_poke_edge(pokemon)
    #         srcs.append(src)
    #         dests.append(dest)
    #         ans, curr_distances, curr_previous = self.graph_algo.dijkstra(dest, agent.speed)
    #         id_distances[dest] = curr_distances
    #         id_previous[dest] = curr_previous
    #
    #     min_time2all = math.inf
    #     min_time2last_poke = math.inf
    #     min_perm = []
    #     all_perms = itertools.permutations(
    #         [i for i in range(len(srcs))])  # shuffle indecies that when we call src[perm[i]] we will get different src
    #     for perm in all_perms:
    #         index = perm[0]
    #         curr_time2all = id_distances.get(curr_dest).get(srcs[index])
    #         curr_time2last_poke = id_distances.get(curr_dest).get(srcs[index])
    #
    #         curr_speed = float(self.graph.key_nodes.get(srcs[index]).child_weight.get(dests[index]))
    #         # x_squared = (float(self.graph.key_nodes.get(srcs[index]).pos[0]) - float(self.graph.key_nodes.get(dests[index]).pos[0])) ** 2
    #         # y_squared = (float(self.graph.key_nodes.get(srcs[index]).pos[1]) - float(self.graph.key_nodes.get(dests[index]).pos[1])) ** 2
    #         # dist_src2dest = math.sqrt(x_squared + y_squared)
    #         tmp_time = (curr_speed / agent.speed)
    #
    #         curr_time2all += tmp_time
    #         curr_time2last_poke += tmp_time
    #
    #         for i in range(len(perm) - 1):
    #             index1 = perm[i]
    #             index2 = perm[i + 1]
    #             curr_time2all += id_distances.get(dests[index1]).get(srcs[index2])
    #             curr_time2last_poke += id_distances.get(dests[index1]).get(srcs[index2])
    #
    #             curr_speed = float(self.graph.key_nodes.get(srcs[index2]).child_weight.get(dests[index2]))
    #             # x_squared = (float(self.graph.key_nodes.get(srcs[index2]).pos[0]) - float(self.graph.key_nodes.get(dests[index2]).pos[0])) ** 2
    #             # y_squared = (float(self.graph.key_nodes.get(srcs[index2]).pos[1]) - float(self.graph.key_nodes.get(dests[index2]).pos[1])) ** 2
    #             # dist_src2dest = math.sqrt(x_squared + y_squared)
    #             tmp_time = (curr_speed / agent.speed)
    #
    #             curr_speed = float(self.graph.key_nodes.get(srcs[index2]).child_weight.get(dests[index2]))
    #             # x_squared = (float(self.graph.key_nodes.get(srcs[index2]).pos[0]) - float(pokemons[index2].pos.x)) ** 2
    #             # y_squared = (float(self.graph.key_nodes.get(srcs[index2]).pos[1]) - float(pokemons[index2].pos.y)) ** 2
    #             # dist_src2dest = math.sqrt(x_squared + y_squared)
    #             time2poke = (curr_speed / agent.speed)
    #
    #             curr_time2all += tmp_time
    #             if i == len(perm) - 2:
    #                 curr_time2last_poke += time2poke
    #             else:
    #                 curr_time2last_poke += tmp_time
    #         if curr_time2last_poke < min_time2last_poke:
    #             min_time2all = curr_time2all
    #             min_time2last_poke = curr_time2last_poke
    #             min_perm = perm
    #
    #     full_min_path = []
    #
    #     index = min_perm[0]
    #     id1 = curr_dest
    #     id2 = srcs[index]
    #     curr_previous = id_previous.get(id1)
    #     curr = id2
    #     ppath = []
    #     while curr != id1:
    #         ppath.insert(0, curr)
    #         curr = curr_previous.get(curr)
    #     ppath.insert(0, id1)
    #     full_min_path += ppath
    #
    #     for i in range(len(min_perm) - 1):
    #         index1 = min_perm[i]
    #         index2 = min_perm[i + 1]
    #         id1 = dests[index1]
    #         id2 = srcs[index2]
    #         curr_previous = id_previous.get(id1)
    #         curr = id2
    #         ppath = []
    #         while curr != id1:
    #             ppath.insert(0, curr)
    #             curr = curr_previous.get(curr)
    #         ppath.insert(0, id1)
    #         full_min_path += ppath
    #     full_min_path.append(dests[min_perm[len(min_perm) - 1]])
    #
    #     return min_time2last_poke, full_min_path, min_time2all

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
