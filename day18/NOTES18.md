# Day 18: Snailfish

For the eighteenth problem we represent the snailfish number in a binary tree
like structure and implement the explode and split steps to get the reduced form
after adding snailfish numbers together.

The general idea to reduce a snailfish number is to repeatedly try to explode
or split until no more changes are made taking care that new explode moves may
be created from split changes.

Taking one of the examples in the problem statement:

```text
[[[[4,3],4],4],[7,[[8,4],9]]] + [1,1]

            /-4
         /-|
      /-|   \-3
     |  |
   /-|   \-4
  |  |
  |   \-4                   /-1
--|                 +    --|
  |   /-7                   \-1
  |  |
   \-|      /-8
     |   /-|
      \-|   \-4
        |
         \-9
```

Results in the following unreduced snailfish number:

```text
[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]

               /-4
            /-|
         /-|   \-3
        |  |
      /-|   \-4
     |  |
     |   \-4
   /-|
  |  |   /-7
  |  |  |
  |   \-|      /-8
  |     |   /-|
--|      \-|   \-4
  |        |
  |         \-9
  |
  |   /-1
   \-|
      \-1
```

We see that there are two pairs `[4,3]` and `[8,4]` at depth 4 so by
recursively exploding from the root of the tree and traversing the left node
first we explode `[4,3]` first by incrementing the nearest left and right
numbers if they exist and replacing the pair with a `0` value.

```text
[[[[0,7],4],[7,[[8,4],9]]],[1,1]]

            /-0
         /-|
      /-|   \-7
     |  |
     |   \-4
   /-|
  |  |   /-7
  |  |  |
  |   \-|      /-8
  |     |   /-|
--|      \-|   \-4
  |        |
  |         \-9
  |
  |   /-1
   \-|
      \-1
```

We see that `[8,4]` is still at depth 4 we again increment its nearest left
and right numbers if they exist and replace the pair with a `0` regular number.

```text
[[[[0,7],4],[15,[0,13]]],[1,1]]

            /-0
         /-|
      /-|   \-7
     |  |
   /-|   \-4
  |  |
  |  |   /-15
  |   \-|
--|     |   /-0
  |      \-|
  |         \-13
  |
  |   /-1
   \-|
      \-1
```

Now we see that there are no pairs at depth 4 so we move on to splitting. We see
that there are two regular values `15` and `13` that are 10 or greater. By
recursively traversing the left node before the right node in the tree we find
the left most value of the two is `15`. We split it into a new pair `[7,8]`
following the rules.

```text
[[[[0,7],4],[[7,8],[0,13]]],[1,1]]

            /-0
         /-|
      /-|   \-7
     |  |
     |   \-4
   /-|
  |  |      /-7
  |  |   /-|
  |  |  |   \-8
  |   \-|
--|     |   /-0
  |      \-|
  |         \-13
  |
  |   /-1
   \-|
      \-1
```

We see that `13` is still a regular number that is 10 or greater and there are
no pairs at depth 4 or more to explode so we again split the number into a new
pair `[6,7]`.

```text
[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]

            /-0
         /-|
      /-|   \-7
     |  |
     |   \-4
   /-|
  |  |      /-7
  |  |   /-|
  |  |  |   \-8
  |   \-|
  |     |   /-0
--|      \-|
  |        |   /-6
  |         \-|
  |            \-7
  |
  |   /-1
   \-|
      \-1
```

Repeating the checks again we see that the new pair we created from splitting
has created a pair at depth 4 so we must explode it.

```text
[[[[0,7],4],[[7,8],[6,0]]],[8,1]]

            /-0
         /-|
      /-|   \-7
     |  |
     |   \-4
   /-|
  |  |      /-7
  |  |   /-|
  |  |  |   \-8
  |   \-|
--|     |   /-6
  |      \-|
  |         \-0
  |
  |   /-8
   \-|
      \-1
```

Finally, running the checks again shows no changes when looking for pairs to
explode or regular numbers to split so we are done.

In Part One we add the snailfish numbers in the input together in order and
calculate the magnitude of the resulting snailfish number.

In Part Two we add all possible pairs of different snailfish numbers and find
the maximum magnitude of the added snailfish numbers.
