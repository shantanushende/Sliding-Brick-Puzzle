Name: Shantanu Shende
Files contained : SBP.py(the program!), hw1.sh(running this will generate a plain text file with output (twice for some reason))

Run the hw1.sh file in order to get the required output as a text file in output-hw1.txt

This program was written in python
SBP.py contents:-
1.a) State representation - I wrote a function which loads gamestate from the file and defines the class for game state.
         As mentioned in the HW1.Html we clone the state apply the move and return the state with move applied to it
         CLone a game state for ease for getting a clone of the state while running the program
         Print- prints the game state 

1. b) as per requirement of 1b we need to check whether the game is solved or not(useful while performing search algorithms)

1.c) Move generation- Multiple functions:-
                        getallpossiblemoves gets all the possible moves for a given state
                       applymove takes in the move we have calculated(using bfs,dfs,ids) and applies it to the peice/brick
                        class Move defines the move that needs to be performed and returns the string with the move(for printing out the move list)
                         we Define a move


1.d) State comparision - checks whether states are equal or not .just simple comparision of integers

1.e) Normalization - applied the algorithms in the instructions
                     rearranging the brick number in incremental order
                      swapping the brick numbers of two bricks

1.f) Random walks- we getallpossiblemoves that can be applied (i.e weed out walls, other bricks/pieces etc) once we get that we chose one at random using random.choice()
                   apply that move and normalize it using the normalize function we created above.


2) we apply the algorithms same as we do while solving bfs,dfs,DLS to the states of the puzzle

a) BFS-we start at first node and all nodes to outgoing edges are added to the queue
1  procedure BFS(G, start_v) is
2      let Q be a queue
3      label start_v as discovered
4      Q.enqueue(start_v)
5      while Q is not empty do
6          v := Q.dequeue()
7          if v is the goal then
8              return v
9          for all edges from v to w in G.adjacentEdges(v) do
10             if w is not labeled as discovered then
11                 label w as discovered
12                 w.parent := v
13                 Q.enqueue(w)

b) DFS uses
procedure DFS(G, v) is
    label v as discovered
    for all directed edges from v to w that are in G.adjacentEdges(v) do
        if vertex w is not labeled as discovered then
            recursively call DFS(G, w)


c)
// Returns true if target is reachable from
// src within max_depth
bool IDDFS(src, target, max_depth)
    for limit from 0 to max_depth
       if DLS(src, target, limit) == true
           return true
    return false   

bool DLS(src, target, limit)
    if (src == target)
        return true;

    // If reached the maximum depth, 
    // stop recursing.
    if (limit <= 0)
        return false;   

    foreach adjacent i of src
        if DLS(i, target, limit?1)             
            return true

    return false

(BFS,DFS, IDS from wikipedia)