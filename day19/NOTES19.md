# Day 19: Beacon Scanner

For the nineteenth problem we rotate and translate 3D coordinates to try to
match the beacon positions from scanners on top of each other and build up the
full map of beacons and scanners.

Our strategy is to start from scanner 0 and match scanners one at a time to
points in the existing map. For each scanner there are 24 different possible
orientations in 3D which can be thought of as facing positive / negative in
each of the x, y and z axes (6 orientations) and the four rotations about the
axis (4 orientations) for each of these directions.

To match one new scanner to the existing map we follow the steps:

1. Loop through all unmatched scanners.
2. For each scanner try all 24 different orientations by applying rotations.
3. For each orientation loop through all the scanner's points.
4. For each existing map point try to fit the scanner's points such that the
chosen scanner point fits on top of the chosen existing map point by applying
a fixed translation to all of the scanner's points.
5. If there are at least 12 points overlapping between the existing map and the
scanner's points in this arrangement we have found the correct position for the
scanner and can add it to the existing map.
6. Repeat until all scanners matched.

To visualize this process consider the simpler 2D case. There are 4 different
possible orientations in 2D which are rotations in the plane:

```text
S - scanner
. - beacon

                     .
  ..         .       S        .
    .     .S .      .        . S.
   S        .        ..      .
   .
```

Consider the existing map:

```text
E - existing scanner
# - existing beacon

  ##     #
  ## E  #
  ##    #
```

Here are three attempts at trying to find 3 overlapping points from the scanner
on the existing map:

```text
E - existing scanner
# - existing beacon
S - scanner
. - beacon
x - beacon overlap

  Attempt 1       Attempt 2       Attempt 3

  ##     x.       ##     #        ##     #
  ## E  #  .      ## E  x.        ## E  #
  ##    # S       ##    # .       ##    x.
          .              S                .
                         .               S
                                         .
```

We eventually find the correct scanner orientation and translation:

```text
E - existing scanner
# - existing beacon
S - scanner
. - beacon
x - beacon overlap

  Correct attempt

  ##     x
  ## E  x S.
  ##    x
```

Our new map becomes:

```text
E - existing scanner
# - existing beacon

  ##     #
  ## E  # E#
  ##    #
```

We repeat the process until all scanners have been matched onto the map.

In Part One we return the number of beacons found in the full map.

In Part Two we compare all pairs of scanners in the full map and return the
largest Manhattan distance (L1-distance) found between a pair.

The matching process takes a few minutes on my machine and could likely be
optimized a lot further for example by using a library like `numpy` optimized
for matrix multiplication.
