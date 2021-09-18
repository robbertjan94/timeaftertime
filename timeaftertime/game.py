from __future__ import annotations
from timeaftertime.core import Coord, Block, Board
from typing import List, Tuple, Hashable, Generator
from dataclasses import dataclass, field

from random import choice, sample
from math import floor, ceil

class GameBoard:

    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.num_colors = 5
        self.max_block_size = 6
        self.num_attributes = {'dice': 5, 'star': 13}
        self.start_column = 0
        self.board = None

    def initialize(self):
        self.board = Board(self.height, self.width)

    def generate(self):
        while not self.board.is_full():
            self.draw_block()
        self.draw_start_column()
        self.draw_attributes()
    
    def draw_block(self):
        available_coords = []
        colors_list = list(range(self.num_colors))
        while len(available_coords) == 0:
            color = choice(colors_list)
            available_coords = self.board.coords_available_color(color)
            colors_list.remove(color)
        length = choice(range(self.max_block_size))
        length = min(length, len(available_coords))
        start_coord = available_coords.pop(0)
        coords = self._draw_connected_coords(start_coord, available_coords, length)
        self.board.add_block(Block(coords, color))

    def draw_attributes(self):
        for attribute, num in self.num_attributes.items():
            coords = []
            for idx in sample(range(len(self.board.blocks)),k=num):
                coords.append(choice(self.board.blocks[idx].coords))
            self.board.add_attribute(attribute, coords)

    def draw_start_column(self):
        self.start_column = choice(range(ceil(self.width*1/3),floor(self.width*2/3)))

    def _draw_connected_coords(self, origin, coords, length):
        stop_loop = False
        connected_coords = [origin]
        while (not stop_loop) and (len(connected_coords) < length):
            neighboring_coords_list = []
            for coord in connected_coords:
                neighboring_coords = [c for c in coords if coord.distance(c) == 1]
                neighboring_coords_list.extend(neighboring_coords)
            if len(neighboring_coords_list) == 0:
                stop_loop = True
            else:
                neighboring_coord = choice(neighboring_coords_list)
                connected_coords.append(neighboring_coord)
                coords.remove(neighboring_coord)
        return connected_coords

game_board = GameBoard(20,13)
game_board.initialize()
game_board.generate()
print(game_board.board)
