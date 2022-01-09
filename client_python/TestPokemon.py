import unittest

from client_python.Agent import Agent
from client_python.Loc_Node_Edge import Location
from client_python.Pokemon import Pokemon


class MyTestCase(unittest.TestCase):
    def test_agent(self):
        key = 1
        value = 15
        src = 0
        dest = -1
        speed = 2
        loc = Location(31, 46, 0)
        agent1 = Agent(key, value, src, dest, speed, loc)
        agent2 = Agent(5, value, src, dest, speed, loc)
        agent3 = Agent(key, 21, 5, 7, 1, Location(15, 0, 0))
        self.assertEqual(agent1.key, key)
        self.assertEqual(agent1.pos, loc)
        self.assertEqual(agent1.src, src)
        self.assertEqual(agent1.dest, dest)
        self.assertEqual(agent1.value, value)
        self.assertEqual(agent1.value, 15)
        self.assertNotEqual(agent1, agent2)
        self.assertEqual(agent1, agent3)




    def test_pokemon(self):
        loc = Location(31, 46, 0)
        value = 15
        t = 1
        pokemon = Pokemon(value, t, loc)
        pokemon2 = Pokemon(12, 15, loc)
        pokemon3 = Pokemon(value, t, loc)
        self.assertEqual(pokemon.type, t)
        self.assertEqual(pokemon.type, 1)
        self.assertEqual(pokemon.pos, loc)
        self.assertEqual(pokemon.value, value)
        self.assertEqual(pokemon.value, 15)
        self.assertNotEqual(pokemon, pokemon2)
        self.assertEqual(pokemon, pokemon3)


if __name__ == '__main__':
    unittest.main()
