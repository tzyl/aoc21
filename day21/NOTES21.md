# Day 21: Dirac Dice

For the twenty-first problem we apply [dynamic programming] again to avoid
performing repeated calculation when simulating the Dirac Dice game in
exponential numbers of universes.

[dynamic programming]: https://en.wikipedia.org/wiki/Dynamic_programming

In Part One we play with a deterministic die and can simply play through the
game once and calculate the answer with the final state of the game.

In Part Two the quantum die means that the number of universes grows
exponentially and it would be intractable to simulate the game in every single
universe separately.

The key observation is that for a given starting state of player1 and player2's
start position and score the number of universes in which each player wins is
deterministic and can be expressed in terms of the number of universes in which
each player wins in each of the outcomes of the quantum die one turn further.

For the quantum die which is rolled three times it creates `3!` new universes
and the distribution of the sum of the rolls in those 27 universes is as
follows:

```text
sum | universes | roll combinations
3   | 1         | 1-1-1             => 3C0
4   | 3         | 1-1-2             => 3C1
5   | 6         | 1-1-3, 1-2-2      => 3C1 + 3C1
6   | 7         | 1-2-3, 2-2-2      => 3C1 * 2C1 + 3C0
7   | 6         | 1-3-3, 2-2-3      => 3C1 + 3C1
8   | 3         | 2-3-3             => 3C1
9   | 1         | 3-3-3             => 3C0
```

Let `f(p1, s1, p2, s2)` be the number of universes in which player1 and player2
each win when playing with the quantum die where player1 starts from position
`p1` with score `s1` and player2 starts from position `p2` with score `s2` where
`1 <= p1, p2 <= 10` and `0 <= s1, s2 <= 21 (or 30 if we allow moving past 21)`
and player1 is next to play. Then we have the following recurrence relation:

```text
f(p1, s1, p2, s2) = (1, 0)                                        if s1 >= 21
f(p1, s1, p2, s2) = (0, 1)                                        if s2 >= 21
f(p1, s1, p2, s2) = 1 * f(p2, s2, move(p1, 3), s1 + move(p1, 3))  if s1, s2 < 21
                  + 3 * f(p2, s2, move(p1, 4), s1 + move(p1, 4))
                  + 6 * f(p2, s2, move(p1, 5), s1 + move(p1, 5))
                  + 7 * f(p2, s2, move(p1, 6), s1 + move(p1, 6))
                  + 6 * f(p2, s2, move(p1, 7), s1 + move(p1, 7))
                  + 3 * f(p2, s2, move(p1, 8), s1 + move(p1, 8))
                  + 3 * f(p2, s2, move(p1, 9), s1 + move(p1, 9))
```

where `move(p, x) = ((p - 1 + x) % 10) + 1` moves the player's position forward
around the track by `x` spaces.

Note that we always assume player1 is next to play as we can reverse the roles
of player1 and player2 in the next turn to simplify things.

If `s1 >= 21` or `s2 >= 21` then the game is already over and one of the players
has won the single universe.

Otherwise if `s1, s2 < 21` then player1 plays the game and rolls the quantum die
three times producing the 27 different universes with sum of rolls distributed
as outlined previously. For each of these universes we have a smaller subproblem
where the score of player1 (swapped to player2 in the next turn) has increased
and their position has changed.

We implement a top down recursive implementation using `cache` from `functools`
in Python's standard library to handle the memoization so that we only compute
each subproblem exactly once.

The answer for Part Two can now be computed by running `f(p1_0, 0, p2_0, 0)`
where `p1_0` and `p2_0` are the initial positions for player1 and player2
respectively in the input.
