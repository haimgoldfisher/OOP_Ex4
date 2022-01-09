class Agent:
    """
    this class represent an agent in the game, it contains the following fields:
    key - the id of this agent
    value - the total value of all the pokemons this agent caught
    src - the key of the source node this agent went out of.
    dest - the kry of the destination node of this agent.
    speed - the speed of this agent.
    pos - Location object represent the location of the agent
    curr_node - if the agent is not moving it will show the "src" value otherwise it will show the "dest" value
    pokemons - a list contains all the pokemons this agent is going to catch
    time2pokes - a list contains all arrival time to the pokemons this agent is going to catch
    time2final_dests - a list contains all arrival time to the first destinations nodes after the pokemons.
    time2curr_dest - a float that shows the arrival time to the closest node
    """

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

    def __eq__(self, other):
        if self.key != other.key:
            return False
        return True
