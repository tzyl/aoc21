#!/usr/bin/env python3
import os


def parse_input(f) -> tuple[str, list[list[str]]]:
    image_enhancement_algorithm = f.readline().strip()
    f.readline()
    input_image = [[c for c in line.strip()] for line in f]
    return image_enhancement_algorithm, input_image


def enhance_image(
    input_image: list[list[str]],
    image_enhancement_algorithm: str,
    infinity_is_dark: bool,
) -> list[list[str]]:
    m = len(input_image)
    n = len(input_image[0])

    # Only the pixels one level away from the input image depend on
    # the input image hence the output image contains this extra level.
    # Pixels two or more levels away will always be all dark or all
    # light depending on the image enhancement algorithm and the parity.
    # We modify the input image with one level of infinity pixels for
    # ease of indexing.
    modified_input_image = [
        ["." if infinity_is_dark else "#"] * (n + 2) for _ in range(m + 2)
    ]
    for i in range(m):
        for j in range(n):
            modified_input_image[i + 1][j + 1] = input_image[i][j]

    output_image = [
        [
            calculate_enhanced_pixel(
                modified_input_image,
                image_enhancement_algorithm,
                i,
                j,
                infinity_is_dark,
            )
            for j in range(n + 2)
        ]
        for i in range(m + 2)
    ]

    return output_image


def calculate_enhanced_pixel(
    input_image: list[list[str]],
    image_enhancement_algorithm: str,
    i: int,
    j: int,
    infinity_is_dark: bool,
) -> str:
    pixel_square = get_pixel_square(input_image, i, j, infinity_is_dark)
    index = int("".join("1" if pixel == "#" else "0" for pixel in pixel_square), 2)
    return image_enhancement_algorithm[index]


def get_pixel_square(
    input_image: list[list[str]], i: int, j: int, infinity_is_dark: bool
) -> list[str]:
    # Note order is important: left to right, top to bottom
    offsets = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 0),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]
    return [
        get_pixel(input_image, i + dx, j + dy, infinity_is_dark) for dx, dy in offsets
    ]


def get_pixel(
    input_image: list[list[str]],
    i: int,
    j: int,
    infinity_is_dark: bool,
) -> str:
    m = len(input_image)
    n = len(input_image[0])
    if 0 <= i < m and 0 <= j < n:
        return input_image[i][j]
    else:
        return "." if infinity_is_dark else "#"


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "../inputs/input20.txt")) as f:
        image_enhancement_algorithm, input_image = parse_input(f)

    enhanced = input_image
    for i in range(2):
        # The input flips infinity between dark and light
        enhanced = enhance_image(enhanced, image_enhancement_algorithm, i % 2 == 0)

    print(sum(pixel == "#" for row in enhanced for pixel in row))
