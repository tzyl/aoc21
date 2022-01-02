# Day 17: Trick Shot

For the seventeenth problem we apply some bounds on the initial x velocity `x_0`
and the initial y velocity `y_0` to narrow the search space and still guarantee
we find all valid values. We assume that the target area is below the x-axis.

Consider what the max trajectory height and y velocity when crossing the x-axis
when the initial y velocity `y_0 > 0`:

```text
y_0 = 3

   ..
  .  .

 .    .

            x
.      .   --->
```

The max trajectory height will be `3 + 2 + 1` or more generally `1 + ... + y_0`
which is the `y_0` the triangle number.

When the probe reaches back down to the x-axis it will have y velocity
`-(1 + y_0)`.

Therefore we know the max trajectory height `y_max` will be:

```text
y_max = 0                    if y_0 <= 0
y_max = y_0 * (y_0 + 1) / 2  if y_0 > 0
```

We can also derive some simple bounds on `x_0` and `y_0`:

```text
1 <= x_0 <= max_x
min_y <= y_0 < abs(min_y)
```

`x_0` must certainly be positive to reach the target area and it must also be
at most `max_x` otherwise it will overshoot the target area in a single step.

`y_0` must be no less than `min_y` otherwise it will drop below the target area
in a single step and it must be less than `abs(min_y)` as we know when `y_0` is
positive it will have y velocity `-(1 + y_0)` when crossing the x-axis and hence
would drop below the target area in one further step otherwise.

With these bounds we can simply iterate through all possible `x_0` and `y_0`
pairs within these bounds and simulate the trajectory step by step until we
either reach or overshoot the target area.

In Part One we use the max trajectory height formula on all the valid initial
velocity values (or simply use `y_0 = abs(min_y) - 1` which is the largest
possible value due to our bounds assuming their is a valid `x_0` value for it).

In Part Two we count the number of initial velocity pairs found.
