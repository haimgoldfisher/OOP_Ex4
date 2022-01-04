from client_python.Loc_Node_Edge import Location


class Pokemon:

    def __init__(self, v, t, loc):
        self.value = v
        self.type = t
        self.pos = loc
        self.agent_aloc = -1
        # self.time2catch

    def __eq__(self, other):
        if self.value != other.value:
            return False
        if self.type != other.type:
            return False
        if self.pos != other.pos:
            return False
        return True

if __name__ == '__main__':
    loc = Location(0,0,0)
    p1 = Pokemon(0,0,loc)
    p2 = Pokemon(0,0,loc)
    print(p1==p2)
    lst = [p1]
    print(p2 not in lst)