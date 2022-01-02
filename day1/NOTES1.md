# Day 1: Sonar Sweep

For the first problem we maintain a sliding window and compare whether the sum
of the window increases or not as we move the window through the input.

In Part One we only need to keep track of the current and previous elements as
we loop through the input (sliding window of length 2).

```text
x1 x2 x3 x4 x5 x6
|__|

x1 x2 x3 x4 x5 x6
   |__|

x1 x2 x3 x4 x5 x6
      |__|

x1 x2 x3 x4 x5 x6
         |__|

x1 x2 x3 x4 x5 x6
            |__|
```

In Part Two we keep track of three elements at a time as we loop through the
input (sliding window of length 3).

```text
x1 x2 x3 x4 x5 x6
|______|

x1 x2 x3 x4 x5 x6
    |______|

x1 x2 x3 x4 x5 x6
        |______|
```
