# Day 4: Giant Squid

For the fourth problem we represent a bingo board and logic to mark and
determine whether a board has won.

To do this we use a 2D matrix (list of lists) which will also be commonly used
in the later problems. In order to track whether numbers on the board have been
called out we use a matching 2D matrix. We can then iterate through the numbers
in the input as they are called out and mark the board in the position with the
matching number.

In Part One we simply iterate through the numbers until we find the first
winning board (assumed to be unique in the winning round).

In Part Two we do a slightly more complicated iteration to get the last winning
board. Each board has its winning score tracked on the round in which it wins
and so the last winning score is simply the final winning score that we find.
