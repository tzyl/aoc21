# Day 2: Dive!

For the second problem we parse through a list of commands and step through the
course of the submarine.

In Part One we simply check the command for `forward`, `up` or `down` and
modify our `position` and `depth` state accordingly.

In Part Two we make a slight modification by also keeping track of `aim`
state for `up` and `down` commands and make corresponding `position` and
`depth` changes only on `forward` commands.
