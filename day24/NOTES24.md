# Day 24: Arithmetic Logic Unit

For the twenty-fourth problem we reverse engineer the ALU program to understand
the constraints required for a model number to be valid and then be easily able
to construct the highest and lowest valid model numbers.

Let the model number be `w1, w2, ..., w14` where `w_i` is the ith digit of the
model number and `1 <= w_i <= 9`. Inspecting the ALU program we see fourteen
similar blocks of instructions with two main types which we call shift and
unshift here:

```text
 shift         unshift

 inp w         inp w
 mul x 0       mul x 0
 add x z       add x z
 mod x 26      mod x 26
*div z 1*     *div z 26*
 add x 12      add x -16
 eql x w       eql x w
 eql x 0       eql x 0
 mul y 0       mul y 0
 add y 25      add y 25
 mul y x       mul y x
 add y 1       add y 1
*mul z y*     *mul z y*
 mul y 0       mul y 0
 add y w       add y w
 add y 6       add y 7
 mul y x       mul y x
*add z y*     *add z y*
```

Out of the fourteen blocks there are seven shift blocks and seven unshift
blocks. Reading through the instructions step by step we notice that the general
modifications to `z` made by each block are:

1. Set `x = 1` if `(z % 26) + x_i != w_i` otherwise `x = 0`.
2. Divide `z` by 1 (identity) or 26.
3. Multiply `z` by 26 if `x = 1` otherwise by 1 (identity).
4. Add `w_i + y_i` to `z` if `x = 1`.

where `x_i` and `y_i` are constants on the 6th and 16th lines of the block
respectively. Note that because `1 <= w_i <= 9` we have `1 <= w_i + y_i < 26`
for the provided constants `y_i` in the input.

This implies that the format of `z` is in base 26 and in a shift block we always
shift `z` to the left by one and add a new term. In an unshift block we always
shift `z` to the right by one and then shift to the left by one and add a new
term if we satisfy the constraint.

In order for `z` to be zero at the end of the program we therefore need every
term in the base 26 representation to be zero. This requires:

- The final block is an unshift block and must not add a new term
- The first block is a shift block and for the term added in it to be zero we
must unshift at least as many times as we shift. As there are seven shift blocks
and seven unshift blocks the ordering of them in the input requires that every
unshift block has its constraint equal to true.

The seven unshift blocks then give us seven different constraints for seven
different pairs of digits in the model number that must be satisfied.

In Part One we choose the highest possible values which satisfy the constraints.

In Part Two we choose the lowest possible values which satisfy the constraints.
