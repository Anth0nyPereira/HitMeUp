from panda3d.core import Vec4
import enum, random


class Color(enum.Enum):
    red = Vec4(10, 0, 0, 1)
    green = Vec4(0, 10, 0, 1)
    blue = Vec4(0, 0, 10, 1)
    purple = Vec4(10, 0, 10, 1)
    yellow = Vec4(10, 10, 3, 1)
    white = Vec4(10, 10, 10, 1)
    gold = Vec4(10, 8.43, 0, 1)

    @classmethod
    def generate_random_color(cls):
        list_of_colors = list(Color)
        color = random.choice(list_of_colors)
        return color

    @classmethod
    def generate_2_random_colors(cls):
        list_of_colors = list(Color)
        # print(list_of_colors)
        first_color = random.choice(list_of_colors)
        list_of_colors.remove(first_color)
        random.shuffle(list_of_colors)
        second_color = random.choice(list_of_colors)
        return first_color, second_color


