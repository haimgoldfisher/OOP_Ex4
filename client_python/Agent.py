class Agent:

    def __init__(self, k, v, src, dest, speed, loc):
        self.key = k
        self.value = v
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = loc
        self.path = []

        self.curr_node = dest
        if dest == -1:
            self.curr_node = src
        self.pokemons = []
        self.time2pokes = []
        self.time2final_dests = []
        self.time2curr_dest = 0

        # self.dests_lst = []
        # self.time2poke = 0
        # self.time2final_dest = 0
        # self.caught_pokemon = False


    def __eq__(self, other):
        # ans = True
        if self.key != other.key:
            return False
        # if self.value != other.value:
        #     return False
        # if self.src != other.src:
        #     return False
        # if self.dest != other.dest:
        #     return False
        # if self.speed != other.speed:
        #     return False
        # if self.pos != other.pos:
        #     return False
        # if self.path != other.path:
        #     return False
        # if self.time2dest != other.time2dest:
        #     return False
        return True
