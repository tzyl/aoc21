# Day 5: Hydrothermal Venture

For the fifth problem we build a mapping between coordinates and number of
lines crossing them. This allows us to store only the coordinates that are
relevant (sparse matrix) rather than tracking the whole 2D space.

In Part One we only need to consider horizontal and vertical lines which we
detect by checking if the x-coordinate or y-coordinate stays the same on the
line. We then iterate through the values of the other coordinate taking care to
loop from the minimum value to the maximum value.

```text
y1 == y2:

-------------------------------
min(x1, x2)         max(x1, x2)


x1 == x2:

            | max(y1, y2)
            |
            |
            |
            |
            |
            | min(y1, y2)
```

In Part Two we need to consider diagonal lines which we handle similarly with
extra care to account for the different directions of the diagonal.

```text
x1 != x2 and y1 != y2:

\ (x1, y1)    \ (x2, y2)                    / (x1, y1)    / (x2, y2)
 \             \                           /             /
  \             \                         /             /
   \   \         \   ^                   /   /         /   ^
    \   v         \   \                 /   v         /   /
     \             \                   /             /
      \             \                 /             /
       \             \               /             /
        \ (x2, y2)    \ (x1, y1)    / (x2, y2)    / (x1, y1)
```

Once we have the mapping we simply loop through the coordinates and count those
which have two or more lines crossing through them.
