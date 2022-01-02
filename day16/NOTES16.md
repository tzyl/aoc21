# Day 16: Packet Decoder

For the sixteenth problem we build a packet parser to evaluate the expression
represented by the packets in the hexadecimal-encoded input.

We use `dataclasses` from Python's standard library to help create immutable
data objects to represent the packet structure and hierarchy without
boilerplate code.

After converting the hexadecimal-encoded input to bits we recursively parse
the packet hierarchy given that the full input contains a single packet. For
each recursive parse function we call we pass in the start index into the bits
and return the number of bits consumed back to the caller.

At the start of every parse call we consume the 6 bits to check the `version`
and `type_id` of the packet in the header. From here we delegate to either
parsing a literal or operator packet based on the `type_id`.

For literal packets we simply keep consuming groups of 5 bits to build the
value of the literal packet until we find the end group with a `0` bit as the
first bit of the group of 5 bits.

For operator packets we have to first consume the `length_type_id` and then
handle parsing out the subpackets according to whether the `length_type_id` is
equal to `0` or `1`.

If the `length_type_id` is equal to `0` then we consume the
`subpackets_bits_length` from the next 15 bits. We then recursively parse
packets until the bits we've consumed matches the target
`subpackets_bits_length`.

If the `length_type_id` is equal to `1` then we consume the `subpackets_length`
from the next 11 bits and recursively parse `subpackets_length` subpackets.

An illustration of the process is shown below:

```text
Outer packet:

00111000000000000110111101000101001010010001001000000000
^
|
start
bits_consumed = 0

00111000000000000110111101000101001010010001001000000000
      ^
      |
      start
bits_consumed = 6
version = 1
type_id = 6

00111000000000000110111101000101001010010001001000000000
       ^
       |
       start
bits_consumed = 7
version = 1
type_id = 6
length_type_id = 0

00111000000000000110111101000101001010010001001000000000
                      ^
                      |
                      start
bits_consumed = 22
version = 1
type_id = 6
length_type_id = 0
subpackets_bits_length = 27
subpackets_bits_consumed = 0

Subpacket 1:

00111000000000000110111101000101001010010001001000000000
                      ^
                      |
                      start
bits_consumed = 0

00111000000000000110111101000101001010010001001000000000
                            ^
                            |
                            start
bits_consumed = 6
version = 6
type_id = 4

00111000000000000110111101000101001010010001001000000000
                                 ^
                                 |
                                 start
bits_consumed = 11
version = 6
type_id = 4
value = 10

Finished parsing subpacket 1
Packet(version=6, type_id=4, value=10, subpackets=[])

Return to outer packet and check subpackets bits consumed:

00111000000000000110111101000101001010010001001000000000
                                 ^
                                 |
                                 start
bits_consumed = 33
version = 1
type_id = 6
length_type_id = 0
subpackets_bits_length = 27
subpackets_bits_consumed = 11

Subpacket 2:

00111000000000000110111101000101001010010001001000000000
                                 ^
                                 |
                                 start
bits_consumed = 0

00111000000000000110111101000101001010010001001000000000
                                       ^
                                       |
                                       start
bits_consumed = 6
version = 2
type_id = 4

00111000000000000110111101000101001010010001001000000000
                                            ^
                                            |
                                            start
bits_consumed = 11
version = 2
type_id = 4

00111000000000000110111101000101001010010001001000000000
                                                 ^
                                                 |
                                                 start
bits_consumed = 16
version = 2
type_id = 4
value = 20

Finished parsing subpacket 2
Packet(version=2, type_id=4, value=20, subpackets=[])

Return to outer packet and check subpackets bits consumed:

00111000000000000110111101000101001010010001001000000000
                                                 ^
                                                 |
                                                 start
bits_consumed = 49
version = 1
type_id = 6
length_type_id = 0
subpackets_bits_length = 27
subpackets_bits_consumed = 27

Finished parsing outer packet
Packet(
    version=1,
    type_id=6,
    value=None,
    subpackets=[
        Packet(version=6, type_id=4, value=10, subpackets=[]),
        Packet(version=2, type_id=4, value=20, subpackets=[]),
    ],
)

```

In Part One we traverse the parsed packet structure and simply sum up the
`version` in the single outer packet and all nested subpackets.

In Part Two we apply the rules based on the packet `type_id` to actually
evaluate the expression using the values from the literal packets and the
operations in the operator packets.
