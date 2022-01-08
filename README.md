# OOP Ex4 - Pokémon Game

<p align="center">
<img align="center" src="https://www.pocketmonsters.co.il/wp-content/uploads/2019/04/fd18c6d26d4d9d26a0bd9d1a2fb2bd04.png" height=300 />
</p>

### @ Or Yitshak & Haim Goldfisher
---------
## 1. Introduction:

1. <ins>**GraphInterface**</ins> - Contains the following functions that we must implement:
    * `v_size()` - It returns the amount of nodes in this graph.
    * `e_size()` - It returns the amount of edges in this graph. 
    * `get_all_v()` - It returns a dictionary of all the key_node + nodes in this graph.
    * `all_in_edges_of_node(int)` - It returns a dictionary of all the edges which are directed to the selected vertex.
    * `all_out_edges_of_node(int)` - It returns a dictionary of all the edges coming out of the selected vertex.
    * `get_mc()` - It returns the number of actions which we did on this graph so far.
    * `add_node(int, tuple)` - It adds a new node to this graph.
    * `add_edge(int, int, float)` - It adds a new edge to this graph.
    * `remove_node(int)` - It removes a node from this graph (If it exists).
    * `remove_edge(int, int)` - It removes an edge from this graph (If it exists).
    
2. <ins>**GraphAlgoInterface**</ins> - Contains the following functions that we must implement:
    * `get_graph()` - It returns the graph that the algorithm loaded.
    * `load_from_json(str)` - It loads a new graph from the Json file.
    * `save_to_json(str)` - It saves the graph that works on it into a Json file.
    * `shortest_path(int, int)` - It returns the distance and the path (list) of the shortest path between two vertices.
    *  `TSP(List[int])` - It returns the shortest path that visits all the nodes in the list as a list and the overall distance.
    *  `centerPoint()` - It return the vertex that has the shortest distance to it's farthest node.
    *  `plot_graph()` - It plots the graph. 

---------
## 2. The Thoughts Behind The Classes:

---------
## 3. UML Diagram:

* We chose to present only the name of the classes in the project:

 <p align="center">
<img align="center" src="https://github.com/haimgoldfisher/OOP_Ex4/blob/master/diagram.png?raw=true" height=500 weight=1000/>
</p>
  
  
---------
## 4. Testing Class:

As required, we will write two test units. The TestDiGraph unit will test the graph methods including location, nodes, edges and MC. Graphs will be built, we will add and remove edges and vertices and then we will ensure that the class works properly. Of course we would like to see that after each operation, the MC value increases as expected. The TestGraphAlgo unit will be performed, but most of the work in it is outside the computer. That is, since we want to verify that the output is correct, we will need to verify this using the algorithmic tools at our disposal. We will check that the desired output is obtained for each of the algorithms. In addition, we would like to see that the auxiliary functions (reverse, isConnected...) are correct as required.

---------
## 5. Results:

| **Case**   | **Graph**   | **Pokemons** | **Time**   | **Agents**  | **Grade**   | **Moves**  |
|------------|-------------|--------------|------------|-------------|-------------|------------|
| 0          | A0          |  1           |  30 sec    |  1          |             |            |
| 1          | A0          |  2           |  1 min     |  1          |             |            |
| 2          | A0          |  3           |  30 sec    |  1          |             |            |
| 3          | A0          |  4           |  1 min     |  1          |             |            |
| 4          | A1          |  5           |  30 sec    |  1          |             |            |
| 5          | A1          |  6           |  1 min     |  1          |             |            |
| 6          | A1          |  1           |  30 sec    |  1          |             |            |
| 7          | A1          |  2           |  1 min     |  1          |             |            |
| 8          | A2          |  3           |  30 sec    |  1          |             |            |
| 9          | A2          |  4           |  1 min     |  1          |             |            |
| 10         | A2          |  5           |  30 sec    |  1          |             |            |
| 11         | A2          |  6           |  1 min     |  3          |             |            |
| 12         | A3          |  1           |  30 sec    |  1          |             |            |
| 13         | A3          |  2           |  1 min     |  2          |             |            |
| 14         | A3          |  3           |  30 sec    |  3          |             |            |
| 15         | A3          |  4           |  1 min     |  1          |             |            |


## A very detailed performence report can be found in our WIKI page: 

---------
## 6. GUI Interface:

If we look at the graphical interface we will notice that there is an agent represented by a brown dot. The agent moves from vertex to vertex by passing over the edges of the graph. Each vertex contains a number so it ID number can be seen. The edge is represented by a simple line. The graph is filled with two types of Pokemon:

<code><img height="50" width="50" src="https://github.com/haimgoldfisher/OOP_Ex4/blob/master/client_python/pokemon1.jpg?raw=true" title="Pikachu" /></code>
<code><img height="50" width="50" src="https://github.com/haimgoldfisher/OOP_Ex4/blob/master/client_python/pokemon2.jpg?raw=true" title="Charmander"/></code> 

Next to each Pokemon will appear the score value it holds. The type of Pokemon is determined by the direction of the edge on which it stands. In addition, the top left corner of the screen lists some important things: points the agent has accumulated so far, number of moves made so far and time left until the game is over. Moreover, there is a red button which causes the program to stop. For example:

---------
## 7. How to Download, Run and Use The Project:

Before Running this project, install the above packages:
```
Pygame Version 2.1.0.
```

Download the whole project and export it by the above actions:
```
Click Code (Green Button) -> Click Download ZIP -> Choose Extract to Folder in Zip -> Run: Main.py
```

Run the Server from cmd, choose one of the 16 cases ([0,15]):
```
java -jar Ex4_Server_v0.0.jar [0,15]
```
---------

This project was done by using Python Interpreter: Python 3.8

---------
## 8. Info & Resources:

- Directed Graphs : https://en.wikipedia.org/wiki/Directed_graph
- Connectivity : https://en.wikipedia.org/wiki/Connectivity_(graph_theory)
- DFS Algorithm : https://en.wikipedia.org/wiki/Depth-first_search
- Priority Queue : https://en.wikipedia.org/wiki/Priority_queue
- Dijkstra's Algorithm : https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
- TSP : https://en.wikipedia.org/wiki/Travelling_salesman_problem
- Pygame: https://www.pygame.org/news

---------
## 9. Languages & Tools: 

<p align="left">
<a href="https://www.python.org/" title="Python"> <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Python.svg/2048px-Python.svg.png" alt="Python" width="40" height="40"/></a>
<a href="https://www.jetbrains.com/pycharm/" title="Pycharm"> <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/PyCharm_Icon.svg/1024px-PyCharm_Icon.svg.png" alt="Pycharm" width="40" height="40"/></a>  
<a href="https://www.json.org/json-en.html" title="JSON"> <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/JSON_vector_logo.svg/2048px-JSON_vector_logo.svg.png" alt="JSON" width="40" height="40"/></a> 
  <a href="https://www.pygame.org/news" title="Pygame"> <img src="https://www.pygame.org/ftp/pygame-head-party.png" alt="Pygame" width="40" height="40"/></a> 
 

