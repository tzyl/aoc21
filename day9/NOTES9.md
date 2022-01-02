# Day 9: Smoke Basin

For the ninth problem we apply [depth-first search (DFS)] to a graph
represented by a 2D matrix.

[depth-first search (DFS)]: https://en.wikipedia.org/wiki/Depth-first_search

In Part One we iterate through all the points and check its four neighbors. If
all of the neighbors have a higher value then we have found a low point.

In Part Two we need to start from the low points and expand the region to the
full basin to find the basin sizes. We have a guarantee that all points will
be in exactly one basin except for locations of height 9 which are not part of
any basin so we don't need to worry about double counting basins.

We use an iterative DFS implementation using a Python list as a stack using its
`pop`/`append` methods and a Python set to mark the seen points which make up
the full basin once the search completes.
