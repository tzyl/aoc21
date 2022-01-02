# Day 7: The Treachery of Whales

For the seventh problem we use some mathematical intuition for the optimal
position to minimize fuel cost.

In Part One the best position is the median. As we can only take an integer
position if there are an even number of positions we need to check the two
nearest positions around the median and take the best of the two.

The intuition behind why the median is the best position is that from any other
position we can achieve a net decrease in fuel cost by moving to the left or
the right as there are more crabs in that direction. The median is therefore a
local minimum and given it is the only position that satisfies this it is also
the global minimum.

```text
x1 x2 x3 x4 x5
<- *  -> -> ->

x1 x2 x3 x4 x5
<- <- <- *  ->

x1 x2 x3 x4 x5
<- <- *  -> ->
```

In Part Two the fuel cost is equal to summing `1 + 2 + ... + abs(x_i - x)` over
each of the positions `x_i` or equivalently `sum(triangle_number(x_i - x))`. We
could simply brute force check the fuel cost over all the possible positions in
`min(x_i) <-> max(x_i)` and choose the best one.

However, following similar ideas in Part One we find that the best position is
actually around the mean. The intuition behind this can be seen by taking the
looking at the rate of change of the fuel cost and finding a minimum where this
is zero.

Consider the rate of change of the fuel cost for a particular `x_i` as we vary
the position `x` to the right by one. We have:

```text
-abs(x_i - x) if x_i > x (moving closer to positions on the right)
abs(x_i - x)  if x_i < x (moving closer to positions on the left)
= x - x_i
```

If we sum over all `x_i` where `n` is the total number of positions and try to
find a minimum we have:

```text
sum(x - x_i) = 0
=> n*x - sum(x_i) = 0
=> x = sum(x_i) / n = mean(x_i)
```

As we can only take an integer position we need to check the two nearest
positions around the mean and take the best of the two.
