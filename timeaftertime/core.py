from __future__ import annotations  # necessary until python 4.0 for future references

import numpy as np

from typing import List, Tuple
from dataclasses import dataclass, field

def invert_list_of_tuples(coords):
    return list(map(list, zip(*coords)))

def get_neighbors(coord):
    x, y = coord
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

def flatten_list(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]

if True:
    @dataclass
    class Block:
        coords: List[Tuple[int, int]] = field(default_factory=list)
        color: int = 0

        def __post_init__(self):
            assert self.is_empty(self.coords) | self._is_connected(self.coords)

        def __str__(self):
            if self.is_empty(self.coords):
                return np.arary([]).__str__()
            row_idx, col_idx = invert_list_of_tuples(self.coords)
            arr = [["-" for _ in range(max(col_idx)+1)] for _ in range(max(row_idx)+1)]
            arr = np.asarray(arr, dtype=object)
            for coord in self.coords:
                arr[coord] = self.color
            return arr.__str__().replace('\'', '')

        def _is_connected(self, coords: List[Tuple[int, int]]):
            """Use a depth-first search (DFS) algorithm to check if all coordinates are connected.
            
            See: https://stackoverflow.com/questions/20583878/python-check-if-coordinates-of-values-in-a-grid-connect-to-one-another/20583999
            """

            if self.is_empty(coords):
                return False
            if len(set(coords)) == 1:
                return True

            def find_neighbors(coord, coords):
                candidates = get_neighbors(coord)    
                return [c for c in candidates if c in coords]

            seen = set()
            frontier = [coords[0]]
            while not len(frontier) == 0:
                coord = frontier.pop()
                seen.add(coord)
                frontier.extend([n for n in find_neighbors(coord, coords) if not n in seen])
            return len(seen) == len(set(coords))
        
        def is_empty(self, coords):
            return len(coords) == 0
        
        def add_coord(self, coord: Tuple[int, int]):
            assert coord not in self.coords
            coords_extended = self.coords + [coord]
            assert self._is_connected(coords_extended)
            self.coords = coords_extended
        
        def add_coords(self, coords: List[Tuple[int, int]]):
            coords_extended = self.coords + coords
            assert len(coords_extended) == len(set(coords_extended))
            assert self._is_connected(coords_extended)
            self.coords = coords_extended

        def remove_coord(self, coord):
            coords = [c for c in self.coords if c != coord]
            assert self.is_empty(coords) | self._is_connected(coords)
            self.coords = coords
        
        def remove_coords(self, coords: List[Tuple[int, int]]):
            coords = [c for c in self.coords if c not in coords]
            assert self.is_empty(coords) | self._is_connected(coords)
            self.coords = coords
        
        def set_color(self, color: int):
            self.color = color

        def overlaps(self, other: Block):
            overlap = set(self.coords).intersection(set(other.coords))
            return len(overlap) > 0

        def neighbors(self, other: Block, overlap_allowed=False, same_color=False):
            if self.is_empty(self.coords) | self.is_empty(other.coords):
                return False
            if same_color & (self.color != other.color):
                return False
            are_neighbors = self._is_connected(self.coords + other.coords)
            are_neighbors &= self.coords != other.coords
            if not overlap_allowed:
                are_neighbors &= not self.overlaps(other)
            return are_neighbors

if True:
    @dataclass
    class Board:
        height: int
        width: int
        blocks: List[Block] = field(default_factory=list)
        
        def add_block(self, other: Block):
            assert not self._overlaps(other)
            assert not self._neighbors_same_color(other)
            assert self._within_bounds(other)
            self.blocks.append(other)
        
        def is_empty(self):
            if len(self.blocks) == 0:
                return True
            for block in self.blocks:
                if len(block.coords) > 0:
                    return False
            return True

        def is_full(self):
            if len(self.blocks) == 0:
                return False
            coords = []
            for block in self.blocks:
                coords.append(block.coords)
            return len(set(coords)) == self.width * self.height

        def coords_available(self):
            coords = [[(i,j) for i in range(self.width)] for j in range(self.height)]
            coords = flatten_list(coords)
            for block in self.blocks:
                coords = [c for c in coords if c not in block.coords]
            return coords

        def coords_available_color(self, color):
            available_coords = self.coords_available()
            color_coords = [block.coords for block in self.blocks if block.color == color]
            color_coords = flatten_list(color_coords)
            color_neighbor_coords = [get_neighbors(coord) for coord in color_coords]
            color_neighbor_coords = flatten_list(color_neighbor_coords)
            return [coord for coord in available_coords if coord not in color_neighbor_coords]
        
        def _overlaps(self, other):
            for block in self.blocks:
                if block.overlaps(other):
                    return True
            return False

        def _neighbors_same_color(self, other):
            for block in self.blocks:
                if block.neighbors(other, same_color=True):
                    return True
            return False

        def _within_bounds(self, other):
            row_idx, col_idx = invert_list_of_tuples(other.coords)
            return ((max(row_idx) < self.height) &
                    (max(col_idx) < self.width))
