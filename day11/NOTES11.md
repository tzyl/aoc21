# Day 11: Dumbo Octopus

For the eleventh problem we simulate the octopus flash chain reaction process
in a 2D matrix.

When simulating the flashes we need to take care to coordinate the order in
which octopuses flash and increment the energy levels of their neighbors. The
general ordering of a single step is as follows:

1. Initialize the set of all octopuses that have flashed in this step `flashed`.
2. Begin a new round in this step and initialize the set of all octopuses that
have flashed in this round of this step `new_flashes`.
3. Iterate through all octopuses.
4. If an energy level is greater than 9 and the octopus hasn't flashed yet in
this step by checking `flashed` mark it as flashed in this round by adding to
`new_flashes`.
5. For all octopuses which flashed in this round increment their neighboring
octopus energy levels by 1.
6. Add the set of octopuses that flashed in this round `new_flashes` to the
overall set of octopuses `flashed`.
7. If `new_flashes` was not empty go back to 2. and repeat another round to
check if there are any more flashes from chain reactions.
8. If `new_flashes` was empty then the step is complete. We return the size of
`flashed` which is the number of flashes that happened in this step.

In Part One we simulate through 100 steps and count the total number of flashes.

In Part Two we simulate through steps until we find the energy levels of the
octopuses are synchronized (all equal to zero).
