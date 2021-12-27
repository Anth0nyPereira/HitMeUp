from panda3d.core import Vec4
import enum, random


class Color(enum.Enum):
    red = Vec4(1, 0, 0, 1)
    green = Vec4(0, 1, 0, 1)
    blue = Vec4(0, 0, 1, 1)
    purple = Vec4(1, 0, 1, 1)
    yellow = Vec4(1, 1, 0, 1)

    @classmethod
    def generate_2_random_colors(cls):
        list_of_colors = list(Color)
        print(list_of_colors)
        first_color = random.choice(list_of_colors)
        list_of_colors.remove(first_color)
        random.shuffle(list_of_colors)
        second_color = random.choice(list_of_colors)
        return first_color, second_color
