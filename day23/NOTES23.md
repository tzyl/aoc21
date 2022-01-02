# Day 23: Amphipod

For the twenty-third problem we apply [Dijkstra's algorithm] again to find the
shortest path in the amphipod burrow to organize the amphipods where the nodes
are states of the amphipod burrow and the edges are possible amphipod moves
with the energy cost of the move as the weight.

[Dijkstra's algorithm]: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

Consider the state of the hallway and rooms in the amphipod burrow as a node in
a graph. By moving amphipods out of or in to rooms we transition to another node
in the graph. The moves are therefore edges of the graph and have corresponding
weight equal to the energy cost of moving the amphipod.

For example here are three example nodes and two example edges in the graph:

```text
#############          #############          #############
#.....C.B...#   3000   #.....C.B..D#   200    #.......B.D.#
###B#.#.#D###   --->   ###B#.#.#.###   --->   ###B#.#C#.###
  #A#D#C#A#              #A#D#C#A#              #A#D#C#A#
  #########              #########              #########
```

The first edge has weight `3 * 1000 = 3000` as the `D` amphipod moves 3 steps.

The second edge has weight `2 * 100 = 200` as the `C` amphipod moves 2 steps.

With this graph representation we can calculate the possible moves from a given
amphipod burrow and apply Dijkstra's algorithm to get the shortest path from the
initial amphipod burrow to the completed amphipod burrow.

In Part One we apply Dijkstra's algorithm as described and return the distance
of the shortest path which is the least energy required to organize the
amphipods.

In Part Two we make a slight modification to the amphipod burrow state to make
the amphipod rooms contain four amphipods rather than two. The same Dijkstra's
algorithm approach still works.

Further optimizations could be made to prune the search space early for example
when we know the amphipod burrow is in an unsolvable state if the amphipods are
in deadlock and cannot ever enter their rooms.
