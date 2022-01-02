# Day 6: Lanternfish

For the sixth problem we apply a programming technique called [dynamic
programming]. This technique is generally applicable when we can find a
recurrence relation to answer the problem based on smaller subproblems which
would often have exponential growth due to repeated calculation of the
subproblems.

[dynamic programming]: https://en.wikipedia.org/wiki/Dynamic_programming

Let `f(n, t)` be defined as the number of lanternfish produced from a single
starting lanternfish after number of days `t` starting from an initial timer
value of `n` where `t >= 0` and `0 <= n <= 8`. According to the rules we have
the following recurrence relation and base cases:

```text
f(n, 0) = 1                          if t = 0
f(n, t) = f(n - 1, t - 1)            if t > 0 and n >= 1
f(n, t) = f(6, t - 1) + f(8, t - 1)  if t > 0 and n = 0
```

For `t = 0` we simply have the initial lanternfish and no growth process occurs.

For `t > 0` we have two cases. If `n >= 1` then no growth process occurs and the
timer value simply decreases by one so the answer is the same as a lanternfish
which started with a timer value of one less and grows for one less day.
However, if `n = 0` then we have a new lanternfish created and so we have two
smaller subproblems to track. The existing lanternfish resets to a timer of
`n = 6` and the newly created lanternfish starts at a timer of `n = 8`.

With this recurrence relation we can now implement dynamic programming in two
ways. In the top down recursive implementation we could use memoization
(caching) to make sure we only calculate each smaller subproblem at most once.
Alternatively, the bottom up iterative implementation is done here which has
benefits of not needing to worry about recursion depth limits (1000 in Python)
and could potentially be optimized for memory to only store the previous
`t - 1` layer at a time. On the other hand, it may be preferable to keep
the full cache and persist it between executions if calling the function many
times.

```text
__________________
|.|.|.|.|.|.|.|.|.|  t = 0
|.|.|.|.|.|.|.|.|.|  t = 1   |
|.|.|.|.|.|.|.|.|.|  t = 2   v
|.|.|.|.|.|.|.|.|.|  t = 3
...
```

In Part One we sum f(n, 80) for each of the starting lanternfish in the input.

In Part Two we sum f(n, 256) for each of the starting lanternfish in the input.
