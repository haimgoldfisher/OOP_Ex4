import unittest
from Loc_Node_Edge import Location, Node
from DiGraph import DiGraph


class MyTestCase(unittest.TestCase):

    def test_node(self):
        g = DiGraph()
        g.add_node(0, (1, 2, 3))
        g.add_node(1, (2, 3, 4))
        self.assertTrue(g.key_nodes.get(0) is not g.key_nodes.get(1))
        g.add_node(2, (3, 4, 0))
        self.assertEqual(len(g.get_all_v().values()), 3)
        g.remove_node(1)
        self.assertEqual(len(g.get_all_v().values()), 2)
        self.assertTrue(g.key_nodes.keys().__contains__(0))
        self.assertTrue(g.key_nodes.keys().__contains__(2))
        self.assertFalse(g.key_nodes.keys().__contains__(1))

    def test_edge(self):
        g = DiGraph()
        g.add_node(0, (1, 2, 3))
        g.add_node(1, (2, 3, 4))
        g.add_node(2, (3, 4, 0))
        g.add_edge(0, 1, 23.11)
        g.add_edge(1, 2, 0.9807)
        g.add_edge(2, 0, 14.0054)
        self.assertEqual(g.edge_counter, 3)
        self.assertFalse(g.e_size() != 3)
        g.add_edge(1, 0, 6.0352)
        g.add_edge(2, 1, 1.48)
        g.add_edge(0, 2, 9.871)
        self.assertEqual(g.edge_counter, 6)
        self.assertEqual(len(g.all_out_edges_of_node(0).keys()), 2) # 0 -> 1, 0 -> 2
        self.assertEqual(g.all_in_edges_of_node(0).get(2), 14.0054) # w
        self.assertEqual(g.all_out_edges_of_node(0).get(1), 23.11) # w
        g.remove_edge(1, 2)
        g.remove_edge(2, 1)
        self.assertEqual(g.e_size(), 4)

    def test_my_dfs(self):
        g = DiGraph()
        g.add_node(0, (1, 2, 3))
        g.add_node(1, (2, 3, 4))
        g.add_node(2, (3, 4, 0))
        g.add_edge(0, 1, 23.11)
        g.add_edge(1, 2, 0.9807)
        g.add_edge(2, 0, 14.0054)
        self.assertEqual(g.my_dfs(0), 3)
        self.assertEqual(g.my_dfs(1), 3)
        self.assertEqual(g.my_dfs(2), 3)
        g.remove_edge(0, 1)
        self.assertEqual(g.my_dfs(1), 3)
        self.assertEqual(g.my_dfs(0), 1)

    def test_mc(self):
        g = DiGraph()
        g.add_node(0, (1, 2, 3))
        g.add_node(1, (2, 3, 4))
        g.add_node(2, (3, 4, 0))
        g.add_edge(0, 1, 23.11)
        g.add_edge(1, 2, 0.9807)
        g.add_edge(2, 0, 14.0054)
        self.assertEqual(6, g.get_mc())
        g.remove_edge(0, 1)
        g.remove_node(2)
        self.assertEqual(8, g.get_mc())


if __name__ == '__main__':
    unittest.main()
