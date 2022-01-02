# Day 20: Trench Map

For the twentieth problem we apply the image enhancement algorithm which
increases the size of the image over time and requires careful consideration
of the infinity boundary.

Consider the example input image in the problem statement:

```text
#..#.
#....
##..#
..#..
..###
```

Let `m` be the number of rows and `n` be the number of columns in the input
image. Consider the layers of infinity around the input image:

```text
@ - first layer of infinity
x - rest of infinity

xxxxxxxxxxx
xxxxxxxxxxx
xx@@@@@@@xx
xx@#..#.@xx
xx@#....@xx
xx@##..#@xx
xx@..#..@xx
xx@..###@xx
xx@@@@@@@xx
xxxxxxxxxxx
xxxxxxxxxxx
```

Observe that only the points in the first layer of infinity shown with `@` can
depend on the values in the input image. All other points of infinity shown
with `x` only depend on other values of infinity whose value is already known.

```text
Enhancing @     Enhancing x

[xxx]   [x@#]   [xxx]   [xx@]
[x@@]   [x@#]   [xxx]   [xx@]
[x@#]   [x@.]   [xx@]   [xx@]
```

This means that our output image after applying image enhancement will have size
one layer greater, `m + 1` rows and `n + 1` columns.

The final observation is that in the input the first character of the image
enhancement algorithm string is `#` and the last character is `.` which means
that the value of infinity outside of the output image will alternate between
`#` and `.`.

Putting this all together to apply the image enhancement algorithm to an input
image we create a new `m + 1` by `n + 1` 2D matrix and compute the elements
using the value of infinity as `#` or `.` depending on if the number of times
we've applied the image enhancement algorithm so far is odd or even
respectively.

In Part One we apply the image enhancement algorithm twice and count the lit
pixels.

In Part Two we apply the image enhancement algorithm 50 times and count the lit
pixels.
