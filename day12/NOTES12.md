# Day 12: Passage Pathing

For the twelfth problem we use [depth-first search (DFS)] again but this time to
find all possible valid paths in a graph. This is an example of a [backtracking]
algorithm.

[depth-first search (DFS)]: https://en.wikipedia.org/wiki/Depth-first_search
[backtracking]: https://en.wikipedia.org/wiki/Backtracking

We use a similar iterative DFS implementation as in Day 9 except with a
different check on neighbor nodes. The stack of nodes to visit this time
contains not only the node to visit but also the history of the path up till
visiting the node. Once we visit the end node we add the full path to the
overall return list.

In Part One when checking neighbor nodes instead of the usual "seen" check we
allow visiting the neighbor if it is a big cave or if it is a small cave and
not in the current path.

In Part Two we make a slight modification to also pass around the small cave on
the current path that we have chosen to visit twice or `None` if we haven't
visited a small cave twice yet. The check for neighbor nodes is then the same
as Part One with an extra condition to allow visiting a small cave neighbor
node that we have already visited once in the current path if we haven't
visited a small cave twice yet and it is not the start or end node.
