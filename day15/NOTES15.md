# Day 15: Chiton

For the fifteenth problem we apply [Dijkstra's algorithm] to find the shortest
path in a 2D matrix where the weight of the edge is the risk level.

[Dijkstra's algorithm]: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

We use `heapq` from Python's standard library to implement the priority queue
for efficiently finding the next node to visit. The neighbors of a node in the
2D matrix are the four up/down/left/right directions and the weight of the edge
is the risk level of the neighbor.

For example the node with risk level `5` in the middle of the block has the four
edges to its neighbors with weights:

```text
123
456
789

^            4     6
| 2   | 8   <--   -->
      v
```

Once Dijkstra's algorithm terminates we can rebuild the shortest path by
following through the `previous` matrix which tracks for each node which
node is the previous node on the shortest path to it. Once we have the shortest
path we sum up all the risk levels to get lowest total risk level (or just
return the distance).

In Part One we run Dijkstra's algorithm on the 100x100 input matrix.

In Part Two we take the 100x100 input matrix as a single tile of the full
500x500 matrix and generate the remaining risk level tiles by incrementing the
risk levels in the original tile. Once this is generated we run Dijkstra's
algorithm again as before.
