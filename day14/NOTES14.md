# Day 14: Extended Polymerization

For the fourteenth problem we apply [dynamic programming] again to avoid
performing repeated calculation when building the polymer which would otherwise
cause exponential runtime.

[dynamic programming]: https://en.wikipedia.org/wiki/Dynamic_programming

Suppose we had a polymer template and single pair insertion rule as follows:

```text
AA
AA -> A
```

If we naively performed pair insertion to build the polymer we would quickly
hit problems with time and memory due to the polymer size growing by `O(2^n)`.

An important observation is that we don't care what the polymer actually looks
like, only the counts of the pairs within it. With this observation we can build
up a recurrence relation as follows:

Let `f(p, n)` be defined as the count of the number of times the pair `p`
appears in the polymer starting with the initial polymer template `P_0` and pair
insertion rules `R` after repeating pair insertion `n` times. Let `p_0` be the
number of times the pair `p` occurs in the initial polymer template which
is a fixed constant given the template. The recurrence relation and base cases
are:

```text
f(p, 0) = p_0                                      if n = 0
f(p, n) = sum(f(p_a, n - 1)) + sum(f(p_b, n - 1))  if n >= 1 if p is in R
f(p, n) = sum(f(p_a, n - 1)) + sum(f(p_b, n - 1))  if n >= 1 if p is not in R
          + f(p, n - 1)
```

where the first sum is over all `p_a` in `R` where `R[p_a] = p[0]` and the
second sum is over all `p_b` in `R` where `R[p_b] = p[1]` so that
`p[0] + R[p_a] = p` and `R[p_b] + p[1] = p`.

For `n = 0` we simply have the initial count in the initial template `P_0`.

For `n >= 1` we are looking for all pairs at `n - 1` steps which are in `R` and
after the pair insertion process either the newly created left pair or the newly
created right pair are equal to `p`. If `p` itself is not in `R` then any
existing pairs will continue to exist at step `n`.

With this recurrence relation we can now implement dynamic programming. The
simpler way is to start from step `n` and build up the counts for step `n + 1`
rather than looking back.

1. Initialize pair counts for `n = 0` with `p_0` for each pair `p` in `P_0`.
2. Repeat for each `n >= 1`.
3. For each pair `p` check if it is in `R` or not.
4. If it is not in `R` then no pair insertion occurs so increment the pair
count for `p` in `n + 1` by the current count for `p`.
5. If it is in `R` then perform the pair insertion process to get the newly
created left and right pairs. Increment the pair count for these pairs `p_a`
and `p_b` in `n + 1` by the current count for `p`.

The final step to get the individual letter counts in the final polymer is to
note that every letter will appear in exactly two pairs except for the first and
last letter in `P_0` which only appear in one pair each. Therefore, we count the
number of each letter in all the pair counts, increment the first and last
letter in `P_0` by one and then divide all letter counts by two.

```text
polymer
ABCD

pair counts
AB: 1
BC: 1
CD: 1

letter counts from pairs
A: 1
B: 2
C: 2
D: 1
```

In Part One we apply the pair insertion process 10 times.

In Part Two we apply the pair insertion process 40 times.
