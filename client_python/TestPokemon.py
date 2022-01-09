import unittest


class MyTestCase(unittest.TestCase):
    def test_agent(self):
        self.assertEqual(True, True)

    def test_pokemon(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
