from __future__ import annotations
from timeaftertime.core import Coord, Block, Board
from typing import List, Tuple, Hashable, Generator, Dict
from dataclasses import dataclass, field

from random import choice, sample
from math import floor, ceil

class GameBoard:

    def __init__(self, height: int = 7, width: int = 15):
        self.height = height
        self.width = width
        self.num_colors = 5
        self.num_dice = 5
        self.num_star = 13
        self.max_block_size = 6
        self.layout = {}
        self.board = None
    
    def __str__(self):
        return self.board.__str__()

    def initialize(self):
        self.board = Board(self.height, self.width)

    def generate(self):
        while not self.board.is_full():
            self.draw_block()
        self.draw_layout()
    
    def add_layout(self, name, values):
        self.layout[name] = values
    
    def draw_block(self):
        available_coords = []
        colors_list = list(range(1,self.num_colors+1))
        while len(available_coords) == 0:
            color = choice(colors_list)
            available_coords = self.board.coords_available_color(color)
            colors_list.remove(color)
        length = choice(range(self.max_block_size))
        length = min(length, len(available_coords))
        start_coord = available_coords.pop(0)
        coords = self._draw_connected_coords(start_coord, available_coords, length)
        self.board.add_block(Block(coords, color))

    def draw_attributes(self, attributes):
        coords = []
        for attribute, num in attributes.items():
            blocks = self.board.blocks.copy()
            coords_attribute = []
            while len(coords_attribute) < num:
                candidates = range(len(blocks))
                block = blocks[sample(candidates, k=1)[0]]
                valid_coords = [c for c in block.coords if c not in coords]
                if len(valid_coords) > 0:
                    coords_attribute.append(sample(valid_coords,k=1)[0])
                blocks.remove(block)
            self.add_layout(attribute, coords_attribute)
            coords.extend(coords_attribute)

    def draw_layout(self):
        # start column
        start_column = choice(range(ceil(self.width*1/3),floor(self.width*2/3)))
        self.add_layout('start_column', start_column)
        
        # row/col names
        col_names = list(range(self.width))
        self.add_layout('col_names', col_names)
        self.add_layout('row_names', list(range(col_names[-1]+1, col_names[-1]+1+self.height)))

        # row/col scores
        self.add_layout('row_scores', [5]*self.height)
        col_scores_top = []
        for (n, i) in enumerate([x - start_column for x in range(self.width+1)]):
            if i != 0:
                col_scores_top.append(2 + floor((abs(i)-1)/3))
        col_scores_top[0] = col_scores_top[1] + 2
        col_scores_top[-1] = col_scores_top[-2] + 2
        col_scores_top[start_column] = 0
        self.add_layout('col_scores_top', col_scores_top)
        col_scores_bottom = [ceil(x/2) for x in col_scores_top]
        col_scores_bottom[start_column] = 0
        self.add_layout('col_scores_bottom', col_scores_bottom)

        # row attributes
        row_attributes = ([1,2,3]*ceil(self.height/3))[:self.height]
        self.add_layout('row_attributes', sample(row_attributes, k=self.height))

        # field attributes
        self.draw_attributes({'dice': self.num_dice,
                              'star': self.num_star})

    def shape(self):
        return (self.height, self.width)

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

# game_board = GameBoard(7,15)
# game_board.initialize()
# game_board.generate()
# print(game_board)
