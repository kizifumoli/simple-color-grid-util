#!/usr/bin/env python3

from typing import Dict, Any, List
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from pathlib import Path

def color_string_to_tuple(color: str, color_type: str):
    # color_type is unused for now
    return (int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16))


class ColorGrid:
    # TODO: Add HSV / other kinds of color representation support
    def __init__(self, n_rows: int, n_cols: int, data: List[str], color_type: str):
        self.n_rows = n_rows
        self.n_cols = n_cols

        self.n_colors = self.n_rows * self.n_cols

        # Unused
        self.color_type = color_type

        self.color_strings = data
        n_colors = self.n_rows * self.n_cols
        if len(self.color_strings) < self.n_colors:
            self.color_strings.extend(["ffffff"] * (self.n_colors - len(self.color_strings)))

        self.color_values = [color_string_to_tuple(color, self.color_type) for color in self.color_strings]

    @staticmethod
    def from_json(data: Dict[str, Any]) -> "ColorGrid":
        return ColorGrid(data["n_rows"], data["n_cols"], data["data"], data.get("color_type", "RGB"))


    def to_image(self, output_filepath: Path):
        text_font = ImageFont.truetype("/home/hydra/.local/share/fonts/FiraCode-Regular.ttf", 10)

        square_length = 100

        image_width = self.n_cols * square_length
        image_height = self.n_rows * square_length


        colors = self.color_values[:self.n_colors]
        # Draw every color in the image
        image = Image.new(mode="RGB", size=(image_width, image_height))
        draw = ImageDraw.Draw(image)

        color_index = 0
        for row in range(self.n_rows):
            for col in range(self.n_cols):
                # Draw the color
                color_coordinates = [(col * square_length, row * square_length),
                                     ((col + 1) * square_length), (row + 1) * square_length ]
                draw.rectangle(color_coordinates, colors[color_index])

                # Now draw some text on top of the color
                text_proportion = 0.2 # What fraction of the height should be a white text box
                textbox_coordinates = [
                    ((col * square_length), ((row + 1) * square_length) - (text_proportion * square_length)),
                    ((col + 1) * square_length), (row + 1) * square_length
                ]
                draw.rectangle(textbox_coordinates, (255, 255, 255), outline=(0,0,0), width = 2)

                color_text = self.color_type.lower() + "(" + self.color_strings[color_index] + ")"

                # Figure out where to place the text such that it's centered horizontally.
                color_text_width = text_font.getlength(color_text)
                text_coordinates = [
                    ((col * square_length) + (100 - color_text_width) / 2,
                     ((row + 1) * square_length) - (text_proportion * square_length) + 4),
                ]

                draw.text(text_coordinates[0], color_text, (0, 0, 0), font_size = "10px", font=text_font)

                color_index += 1

        image.show(output_filepath)
