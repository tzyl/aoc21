# Day 25: Sea Cucumber

For the twenty-fifth problem we simulate a two step process of the east and
south facing herds of sea cucumbers.

Our approach is to initialize the empty new state of the sea cucumbers and
place the new positions of the east facing herd in a first pass and then place
the new positions of the south facing herds in a second pass.

Consider the following example:

```text
.......v..
.>v....v..
.......>..
..........
```

We initialize the empty new state of the sea cucumbers.

```text
..........
..........
..........
..........
```

For each sea cucumber in the east facing herd we check in the original state if
it is able to move right or not being careful to handle wrapping around the end
of the grid. An east facing sea cucumber will be able to move if there is no
other east facing sea cucumber `>` or south facing sea cucumber `v` immediately
to the right of it in the original state. In the example only the east facing
sea cucumber on the right moves:

```text
..........
.>........
........>.
..........
```

For each sea cucumber in the south facing herd we check in the original state if
it is blocked from moving down by another south facing sea cucumber `v` in the
original state or if it is blocked from moving down by an east facing sea
cucumber `>` in the new state after they have potentially moved. In the example
only two of the three south facing sea cucumbers move:

```text
.......v..
.>........
..v....v>.
..........
```

In Part One we repeat this process and count the number of steps until the sea
cucumbers no longer move.

In Part Two we're already finished as all previous stars have been solved!
