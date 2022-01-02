# Day 8: Seven Segment Search

For the eighth problem we need to unscramble the segments for the seven-segment
display using the unique patterns and finally decode the output value.

Let `u`, `ul`, `ur`, `m`, `dl`, `dr` and `d` correspond to the following
segments on the seven-segment display:

```text
   u
ul   ur
   m
dl   dr
   d
```

To display each of the digits we turn on the following segments:

```text
0 -> 6 segments -> "u", "ul", "ur", "dl", "dr", "d"
1 -> 2 segments -> "ur", "dr"
2 -> 5 segments -> "u", "ur", "m", "dl", "d"
3 -> 5 segments -> "u", "ur", "m", "dr", "d"
4 -> 4 segments -> "ul", "ur", "m", "dr"
5 -> 5 segments -> "u", "ul", "m", "dr", "d"
6 -> 6 segments -> "u", "ul", "m", "dl", "dr", "d"
7 -> 3 segments -> "u", "ur", "dr"
8 -> 7 segments -> "u", "ul", "ur", "m", "dl", "dr", "d"
9 -> 6 segments -> "u", "ul", "ur", "m", "dr", "d"
```

Ordered by number of segments:

```text
8 -> 7 segments -> "u", "ul", "ur", "m", "dl", "dr", "d"
0 -> 6 segments -> "u", "ul", "ur", "dl", "dr", "d"
6 -> 6 segments -> "u", "ul", "m", "dl", "dr", "d"
9 -> 6 segments -> "u", "ul", "ur", "m", "dr", "d"
2 -> 5 segments -> "u", "ur", "m", "dl", "d"
3 -> 5 segments -> "u", "ur", "m", "dr", "d"
5 -> 5 segments -> "u", "ul", "m", "dr", "d"
4 -> 4 segments -> "ul", "ur", "m", "dr"
7 -> 3 segments -> "u", "ur", "dr"
1 -> 2 segments -> "ur", "dr"
```

In Part One to count the digits 1, 4, 7 and 8 which have a unique number of
segments we therefore count the number of digits in the output values that
have 2, 4, 3 or 7 segments on.

In Part Two we need to actually unscramble which wire corresponds to which
segment in order to decode the output values.

Consider the unique pattern for the digit 1:

```text
1 pattern
   .
.    ur
   .
.    dr
   .
```

Let these wires be `a`/`b` so we know `a`/`b` correspond to `ur`/`dr` in some
currently unknown ordering.

Consider the unique patterns for digit 4 and 1:

```text
4 pattern       1 pattern
   .               .               .
ul   ur         .    ur         ul    .
   m        -      .        =      m
.    dr         .    dr         .     .
   .               .               .
```

If we take away the two wires appearing in the 1 pattern from the 4 pattern we
will be left with two wires. Let these be `c`/`d` so we know `c`/`d` correspond
to `ul`/`m` in some currently unknown ordering.

Consider the unique patterns for 8, 7 and 4:

```text
8 pattern       7 pattern       4 pattern
   u               u               .               .
ul   ur         .    ur         ul   ur         .     .
   m        -      .        -      m        =      .
dl    dr        .    dr         .    dr         dl    .
   d               .               .               d
```

Take away the wires appearing in the 7 and 4 patterns from the 8 pattern and we
will be left with two wires again. Let these be `e`/`f` so we know `e`/`f`
correspond to `dl`/`d` in some currently unknown ordering.

Consider the unique patterns for 7 and 1:

```text
7 pattern       1 pattern
   u               .               u
.    ur         .    ur         .     .
   .        -      .        =      .
.    dr         .    dr         .     .
   .               .               .
```

Take away the wires appearing in the 1 pattern from the 7 pattern and we will be
left with exactly one wire. Let this be `g` so we know `g` corresponds to `u`.

At this point we know the following:

```text
a/b -> ur/dr
c/d -> ul/m
e/f -> dl/d
g   -> u
```

Now consider the three patterns which have 5 segments on. These must correspond
to the digits 2, 3 and 5.

```text
2 pattern       3 pattern       5 pattern
   u               u               u
.    ur         .    ur         ul    .
   m               m               m
dl     .        .    dr         .    dr
   d               d               d
```

We can determine which of the three patterns is the digit 2 by looking for the
presence of both `dl` and `d` which we know are `e` and `f`.

We can determine which of the three patterns is the digit 3 by looking for the
presence of both `ur` and `dr` which we know are `a` and `b`.

We can determine which of the three patterns is the digit 5 by looking for the
presence of both `ul` and `m` which we know are `c` and `d`.

Now we know which pattern corresponds to which digit we can determine which of
the wires correspond to which segment in each of the unknown pairs.

To determine which of `a` and `b` is `ur` and which is `dr` we look at the
2 pattern. The wire which appears in the 2 pattern must be `ur` and the other
must be `dr`.

To determine which of `c` and `d` is `ul` and which is `m` we look at the
3 and 5 patterns. If `c` appears in the 5 pattern but not the 3 pattern it must
be `ul` otherwise it appears in both patterns and it must be `m`.

To determine which of `e` and `f` is `dl` and which is `d` we look at the
2 and 3 patterns. If `e` appears in the 2 pattern but not the 3 pattern it must
be `dl` otherwise it appears in both patterns and it must be `d`.

We now know for all seven wires which segment they correspond to and to answer
Part Two simply decode the wires to the correct segments using the mapping and
find the correct digit based on the segments which are actually turned on.
