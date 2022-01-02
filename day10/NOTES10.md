# Day 10: Syntax Scoring

For the tenth problem we use a [stack] to track all currently open chunks and
the order in which they were opened.

[stack]: https://en.wikipedia.org/wiki/Stack_(abstract_data_type)

In Part One to identify corrupt strings each time we encounter an open chunk
character we push it onto the top of the stack. Each time we encounter a close
chunk character we pop off the last open chunk character and hence mark it as
closed. Finally, we verify that the close chunk character matches the chunk type
of the open chunk character and if they do not match we have found a corrupt
string.

For example:

```text
{([(<{}[<>[]}>{[]{[(<()>
^
|
stack: {

...

{([(<{}[<>[]}>{[]{[(<()>
     ^
     |
stack: { ( [ ( < {

{([(<{}[<>[]}>{[]{[(<()>
      ^
      |
stack: { ( [ ( <
pop: {
verify : }

...

{([(<{}[<>[]}>{[]{[(<()>
        ^
        |
stack: { ( [ ( < [ <

{([(<{}[<>[]}>{[]{[(<()>
         ^
         |
stack: { ( [ ( < [
pop: <
verify: >

{([(<{}[<>[]}>{[]{[(<()>
          ^
          |
stack: { ( [ ( < [ [

{([(<{}[<>[]}>{[]{[(<()>
           ^
           |
stack: { ( [ ( < [
pop: [
verify : ]

{([(<{}[<>[]}>{[]{[(<()>
            ^
            |
stack: { ( [ ( <
pop: [
verify : }

Expected ] but found } instead
```

Using the illegal character scores provided we can calculate the answer after
finding the first illegal character in all of the corrupt strings.

In Part Two for the incomplete but not corrupt strings we need to find the
completion string. After following through the steps from Part One at the end
of the string we inspect the stack. If the stack is not empty then the string
is incomplete and we need to add corresponding close chunk characters for each
of the open chunk characters we pop off the final stack.

For example:

```text
[({(<(())[]>[[{[]{<()<>>
                       ^
                       |
stack: [({([[{{
completion string: }}]])})]
```

Using the autocomplete character scores provided we can calculate the answer
after finding the completion string scores in all of the incomplete strings.
