# Day 13: Transparent Origami

For the thirteenth problem we perform careful 2D matrix manipulation in order to
simulate folding a piece of paper on itself.

First we create a new empty matrix with new dimensions matching the fold
instruction.

Next we iterate through each of the positions in the new empty matrix and check
the two corresponding positions on both sides of the fold line in the original
matrix to see whether this position should be a visible dot.

```text
fold x

...1|..        ...1
..2.|..        ..2.
....|3.        ...3
....|.4   ->   ..4.
.5..|..        .5..
6...|..        6...
....|..        ....

fold y

.....6.        .....6.
....5..        ....5..
.2.....        .2.4...
1......   ->   1.3....
-------
..3....
...4...
```

Extra care should be taken for positions such as 5 and 6 in the diagram above
which don't have a corresponding position on the other side of the fold line
due to an unbalanced fold.
