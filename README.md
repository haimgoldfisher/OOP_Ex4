# OOP Ex4 - Pokémon Game

<p align="center">
<img align="center" src="https://www.pocketmonsters.co.il/wp-content/uploads/2019/04/fd18c6d26d4d9d26a0bd9d1a2fb2bd04.png" height=300 />
</p>

### @ Or Yitshak & Haim Goldfisher
---------
## 1. Introduction:

We want to design an efficient algorithm for capturing Pokemons on a directed and weighted graph. The algorithm includes the following variables:

1. <ins>Agent - </ins> Each agent is defined to be a player in the game. Please note that the agent's behavior does not change by any user. The agent is basically the product of algorithms designed to capture as many Pokemons as possible, in as short a time as possible. That is, we will need to design a smart algorithm so that the agent will always go to the ideal Pokemon or do the ideal route that will maximize the score he will accumulate during it. The fact that the agent has speed must be taken into account. This speed will increase as a result of capturing Pokemons. Also, the agent will have to change his trajectory as a result of a new Pokemon popping up (which is closer to the agent or has a higher score than the existing path).
2. <ins>Pokemon - </ins> The item the agent must collect. Note that Pokemon can only be on edges and not on vertices. Also, Pokemon can be on the edge in one direction. That is, when there is a forward and backward edge between two vertices, the Pokemon will be on one of them. Also, each Pokemon holds a value, a score that as a result of capturing the Pokemon becomes a score in the game. Also, the agent's speed increases when he catches a Pokemon. The higher the value of the Pokemon, the greater the agent's speed.
3. <ins>Graph - </ins> The playground. The agents and Pokemon are on the graph. Women notice that agents can move from vertex to vertex through the edges. In addition, each Pokemon will appear on the edge. When an agent moves from end to end that has a Pokemon on it - he will collect it. As a result the score will be updated accordingly (and so will the agent's speed). Instead of the collected Pokemon, a new Pokemon will appear in a different position on the graph.
4. <ins>Client (Server) - </ins> The server of the game. In general we will not touch on its code but will only get information from it and use it to update the game status. That is, the server defines the game, the time, the amount of agents, the amount of Pokemon, etc. On its basis we will build the algorithms and implement the necessary objects.

---------
## 2. The Thoughts Behind The Classes:

From a simplistic point of view, it is easy to see that this task is a kind of combination of the elevator task (online) and the graph task. The significant differences between an agent and an elevator are that an elevator can go up and down, but an agent can travel from vertex to vertex more freely and with more options. Also, the agent's speed changes while playing. The significant differences between a passenger and a Pokemon are that the Pokemon is captured and disappears, while the passenger has a starting floor and a destination floor. Also, Pokemon holds a value, while in the elevator task each passenger is equal among equals. We would like to use our graph task that will form the basis for the graph and algorithms needed to solve the problem. That is, it should be noted that we will need TSP and shortest path algorithms from that task. Of course we would like to make such and such changes depending on the game (e.g. different Pokemon values). Therefore, for a start, it would be effective to implement a Pokemon class as well as an Agent class. From there we will want to connect the agent action depending on what is going on in the game, as well as depending on the amount of agents participating in the game. This will be the main challenge. Introduce to each agent the way that maximizes the overall benefit of all agents together. In addition, we would like to reflect what is happening in the game through a GUI interface that clearly shows what is happening in the game. We would like to build a class that will get the necessary information from the server, respond accordingly (update the agents path efficiently to that moment), and also update the GUI. We will have to define some threads for this

---------
## 3. UML Diagram:

* We chose to present only the name of the classes in the project:

 <p align="center">
<img align="center" src="https://github.com/haimgoldfisher/OOP_Ex4/blob/master/diagram.png?raw=true" height=500 weight=1000/>
</p>
  
  
## A detailed explanation of the code structure, classes and algorithms can be found in our WIKI page: 
  
---------
## 4. Testing Class:

As required, we will write test units for each logic function. The first two test classes were taken from the previous task because they test the same functions. The TestDiGraph unit will test the graph methods including location, nodes, edges and MC. Graphs will be built, we will add and remove edges and vertices and then we will ensure that the class works properly. Of course we would like to see that after each operation, the MC value increases as expected. The TestGraphAlgo unit will be performed, but most of the work in it is outside the computer. That is, since we want to verify that the output is correct, we will need to verify this using the algorithmic tools at our disposal. We will check that the desired output is obtained for each of the algorithms. In addition, we would like to see that the auxiliary functions are correct as required. In addition, we would like to check that the agent's time calculations from Pokemon are indeed correct. To do this we will set up a test unit called TestPokemon. It is important to remember that there are many functions that can be tested just by activating the server. Therefore they are not suitable to unit tests. In addition, when it comes to testing the efficiency of our algorithms, this is done by looking at the GUI interface and checking whether the agent is doing the most correct action for that given moment. In addition, the most effective tool we have is the comparison tool. That is, we run our interface and check if the given grade is good compared to the other scores that go up to Google Sheets. This is basically something that can not really be done in a practical way in a standard testing class. It's important to mention that the purpose of the visual interface (GUI) is precisely for the purpose of testing. That is, we do not really need the interface except for ornamental purposes and also for self-examination of what the agent is actually doing.

---------
## 5. Results:

| **Case**   | **Graph**   | **Pokemons** | **Time**   | **Agents**  | **Grade**   | **Moves**  |
|------------|-------------|--------------|------------|-------------|-------------|------------|
| 0          | A0          |  1           |  30 sec    |  1          |  152        | 52         |
| 1          | A0          |  2           |  1 min     |  1          |  526        | 188        |
| 2          | A0          |  3           |  30 sec    |  1          |  284        | 85         |
| 3          | A0          |  4           |  1 min     |  1          |  569        | 194        |
| 4          | A1          |  5           |  30 sec    |  1          |  105        | 44         |
| 5          | A1          |  6           |  1 min     |  1          |  472        | 186        |
| 6          | A1          |  1           |  30 sec    |  1          |  79         | 31         |
| 7          | A1          |  2           |  1 min     |  1          |  312        | 155        |
| 8          | A2          |  3           |  30 sec    |  1          |  73         | 35         |
| 9          | A2          |  4           |  1 min     |  1          |  325        | 153        |
| 10         | A2          |  5           |  30 sec    |  1          |  65         | 32         |
| 11         | A2          |  6           |  1 min     |  3          | 1429        | 566        |
| 12         | A3          |  1           |  30 sec    |  1          | 40          | 26         |
| 13         | A3          |  2           |  1 min     |  2          | 201         | 184        |
| 14         | A3          |  3           |  30 sec    |  3          | 115         | 123        |
| 15         | A3          |  4           |  1 min     |  1          | 234         | 117        |


## A very detailed performence report can be found in our WIKI page: 

---------
## 6. GUI Interface:

 <p align="center">
<img align="center" src="https://github.com/haimgoldfisher/OOP_Ex4/blob/master/game_video/game_gif.gif?raw=true" height=500 weight=1000/>
</p>

If we look at the graphical interface we will notice that there is an agent represented by a brown dot. The agent moves from vertex to vertex by passing over the edges of the graph. Each vertex contains a number so it ID number can be seen. The edge is represented by a simple line. The graph is filled with two types of Pokemon:

<code><img height="50" width="50" src="https://github.com/haimgoldfisher/OOP_Ex4/blob/master/client_python/pokemon1.jpg?raw=true" title="Pikachu" /></code>
<code><img height="50" width="50" src="https://github.com/haimgoldfisher/OOP_Ex4/blob/master/client_python/pokemon2.jpg?raw=true" title="Charmander"/></code> 

Next to each Pokemon will appear the score value it holds. The type of Pokemon is determined by the direction of the edge on which it stands. In addition, the top left corner of the screen lists some important things: points the agent has accumulated so far, number of moves made so far and time left until the game is over. Moreover, there is a red button which causes the program to stop. For example: 

 <p align="center">
<img align="center" src="https://github.com/haimgoldfisher/OOP_Ex4/blob/master/client_python/screen_shot.PNG?raw=true" height=500 weight=1000/>
</p>

## Link to a better quality video of the graphical interface on YouTube: https://www.youtube.com/watch?v=v6mJB2sEmvg

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

Run the Server from cmd in the folder which contains 'Ex4_Server_v0.0.jar', choose one of the 16 cases ([0,15]):
```
java -jar Ex4_Server_v0.0.jar [0,15]
```
---------

This project was done by using Python Interpreter: Python 3.9

---------
## 8. Info & Resources:

- Directed Graphs : https://en.wikipedia.org/wiki/Directed_graph
- Connectivity : https://en.wikipedia.org/wiki/Connectivity_(graph_theory)
- DFS Algorithm : https://en.wikipedia.org/wiki/Depth-first_search
- Shortest Path Problem : https://en.wikipedia.org/wiki/Shortest_path_problem
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
 

