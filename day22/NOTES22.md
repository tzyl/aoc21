# Day 22: Reactor Reboot

For the twenty-second problem we implement an efficient way of tracking cuboids
being added and removed in an unbounded 3D space.

In Part One where the bounds for the space are `-50 <= x, y, z <= 50` we can
simply implement a 50x50x50 3D matrix and iterate through all coordinates in
the cuboids and turn on or off points.

In Part Two we have an unbounded 3D space so this approach would not be feasible
if the cuboids being added and removed are in an arbitrarily large space.
Instead, we need a more compact representation of the cuboids that can still
handle adding and removing other cuboids which may intersect and affect
existing cuboids.

A cuboid can be uniquely defined by 6 integers representing the min and max of
each of the x, y and z axes (as provided in the input). The tricky part is
handling adding or removing a cuboid which intersects with an existing cuboid.
The approach we take is to implement a `remove` function which splits a cuboid
into smaller cuboids representing the volume when removing a cuboid from an
existing cuboid. There may be no cuboids if the cuboid to remove completely
contains the existing cuboid or there could be up to 6 if the existing cuboid
is a proper superset of the cuboid to remove.

Imagine a sliding window approaching the cuboid moving towards the positive x
direction:

```text
  /|->
 / |->
|->|->      o-------------o
|->|->     /            / |
|->|->    /   +----+   /  |
|->|->   o---/----/|--o   |
|->|->   |  +----+ +  |   o
|->|     |  |    |/   |  /
|->|     |  +----+    | /
|->/     |  x1'  x2'  |/
| /      o------------o
|/       x1           x2
```

We have up to four breakpoints to consider at `x1`, `x1'`, `x2'` and `x2`.

If `x1'` > `x1` then we create a smaller cuboid representing the left space.

If `x2'` < `x2` then we create a smaller cuboid representing the right space.

Similarly for `y1`, `y1'`, `y2'` and `y2`.

If `y1'` > `y1` then we create a smaller cuboid representing the bottom space.

If `y2'` < `y2` then we create a smaller cuboid representing the top space.

Similarly for `z1`, `z1'`, `z2'` and `z2`.

If `z1'` > `z1` then we create a smaller cuboid representing the forward space.

If `z2'` < `z2` then we create a smaller cuboid representing the back space.

With this structure in hand we can tackle the problem:

- Iterate through the input cuboids
- If we are turning off the cuboid remove all existing cuboids and add all the
smaller cuboids from removing the cuboid from each existing cuboid
- If we are turning on the cuboid first turn it off using the above step and
then add the cuboid to guarantee that there are no overlapping cuboids

The volume of cubes on can then be simply calculated from summing the volume
of all cuboids left at the end.
