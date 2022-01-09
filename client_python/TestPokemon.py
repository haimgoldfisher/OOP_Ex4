import unittest

from client_python.Loc_Node_Edge import Location
from client_python.Pokemon import Pokemon


class MyTestCase(unittest.TestCase):
    def test_agent(self):
        loc = Location(31, 46, 0)
        value = 15
        t = 1
        pokemon = Pokemon(value, t, loc)
        self.assertEqual(pokemon.type, t)
        self.assertEqual(pokemon.type, 1)



    def test_pokemon(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
