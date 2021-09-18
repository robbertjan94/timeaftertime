from __future__ import annotations  # necessary until python 4.0 for future references
from typing import List, Tuple, Hashable, Generator, Dict
from dataclasses import dataclass, field

import numpy as np

def invert_list_of_coords(coords: List[Coord]) -> Tuple[List[int],List[int]]:
    return list(map(list, zip(*coords)))

def flatten_list(list_of_lists: List[List]) -> List:
    return [item for sublist in list_of_lists for item in sublist]

if True:
    @dataclass
    class Coord:
        x: int
        y: int

        def __hash__(self) -> Hashable:
            return hash(str(self))

        def __eq__(self, other: Coord) -> bool:
            return (self.x == other.x) & (self.y == other.y)
        
        def __iter__(self) -> Generator[int, int, None]:
            yield self.x
            yield self.y

        def to_tuple(self) -> Tuple[int,int]:
            return (self.x, self.y)

        def get_neighbors(self) -> List[Coord]:
            return  [Coord(self.x - 1, self.y), 
                     Coord(self.x + 1, self.y), 
                     Coord(self.x, self.y - 1), 
                     Coord(self.x, self.y + 1)]
        
        def distance(self, other):
            return abs(self.x-other.x) + abs(self.y-other.y)

if True:
    @dataclass
    class Block:
        coords: List[Coord] = field(default_factory=list)
        color: int = 0

        def __post_init__(self):
            assert self.is_empty(self.coords) | self._is_connected(self.coords)

        def __str__(self) -> str:
            if self.is_empty(self.coords):
                return np.arary([]).__str__()
            row_idx, col_idx = invert_list_of_coords(self.coords)
            arr = [["-" for _ in range(max(col_idx)+1)] for _ in range(max(row_idx)+1)]
            arr = np.asarray(arr, dtype=object)
            arr[self.to_tuple()] = self.color
            return arr.__str__().replace('\'', '')
        
        def to_tuple(self):
            return [c.to_tuple() for c in self.coords]

        def _is_connected(self, coords: List[Coord]) -> bool:
            """Use a depth-first search (DFS) algorithm to check if all coordinates are connected.
            
            See: https://stackoverflow.com/questions/20583878/python-check-if-coordinates-of-values-in-a-grid-connect-to-one-another/20583999
            """

            if self.is_empty(coords):
                return False
            if len(set(coords)) == 1:
                return True

            def find_neighbors(coord, coords):
                candidates = coord.get_neighbors()  
                return [c for c in candidates if c in coords]

            seen = set()
            frontier = [coords[0]]
            while not len(frontier) == 0:
                coord = frontier.pop()
                seen.add(coord)
                frontier.extend([n for n in find_neighbors(coord, coords) if not n in seen])
            return len(seen) == len(set(coords))
        
        def is_empty(self, coords) -> bool:
            return len(coords) == 0
        
        def add_coord(self, coord: Coord) -> List[Coord]:
            assert coord not in self.coords
            coords_extended = self.coords + [coord]
            assert self._is_connected(coords_extended)
            self.coords = coords_extended
        
        def add_coords(self, coords: List[Coord]) -> List[Coord]:
            coords_extended = self.coords + coords
            assert len(coords_extended) == len(set(coords_extended))
            assert self._is_connected(coords_extended)
            self.coords = coords_extended

        def remove_coord(self, coord: Coord) -> List[Coord]:
            coords = [c for c in self.coords if c != coord]
            assert self.is_empty(coords) | self._is_connected(coords)
            self.coords = coords
        
        def remove_coords(self, coords: List[Coord]) -> List[Coord]:
            coords = [c for c in self.coords if c not in coords]
            assert self.is_empty(coords) | self._is_connected(coords)
            self.coords = coords
        
        def set_color(self, color: int) -> None:
            self.color = color

        def overlaps(self, other: Block) -> bool:
            overlap = set(self.coords).intersection(set(other.coords))
            return len(overlap) > 0

        def neighbors(self, other: Block, overlap_allowed: bool=False, same_color: bool=False) -> bool:
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

        def __str__(self) -> str:
            arr = [["-" for _ in range(self.width)] for _ in range(self.height)]
            arr = np.asarray(arr, dtype=object)
            for block in self.blocks:
                for coord in block.coords:
                    arr[coord.to_tuple()] = block.color
            return arr.__str__().replace('\'', '')
        
        def add_block(self, other: Block) -> None:
            assert not self._overlaps(other)
            assert not self._neighbors_same_color(other)
            assert self._within_bounds(other)
            self.blocks.append(other)

        def remove_block(self, other: Block) -> None:
            self.blocks.remove(other)
        
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
                coords.extend(block.coords)
            return len(set(coords)) == self.width * self.height

        def coords_available(self) -> List[Coord]:
            coords = self._get_board_coords()
            for block in self.blocks:
                coords = [c for c in coords if c not in block.coords]
            return coords

        def coords_available_color(self, color: int) -> List[Coord]:
            available_coords = self.coords_available()
            color_coords = self._get_color_coords(color)
            color_neighbor_coords = flatten_list([coord.get_neighbors() for coord in color_coords])
            return [coord for coord in available_coords if coord not in color_neighbor_coords]
        
        def _get_board_coords(self) -> List[Coord]:
            coords = [[Coord(i,j) for i in range(self.height)] for j in range(self.width)]
            return flatten_list(coords)

        def _get_color_coords(self, color: int) -> List[Coord]:
            color_coords = [block.coords for block in self.blocks if block.color == color]
            return flatten_list(color_coords)

        def _overlaps(self, other: Block) -> bool:
            for block in self.blocks:
                if block.overlaps(other):
                    return True
            return False

        def _neighbors_same_color(self, other: Block) -> bool:
            for block in self.blocks:
                if block.neighbors(other, same_color=True):
                    return True
            return False

        def _within_bounds(self, other: Block) -> bool:
            row_idx, col_idx = invert_list_of_coords(other.coords)
            return (((max(row_idx) < self.height) & 
                     (max(col_idx) < self.width)) &
                    ((min(row_idx) >= 0) & 
                    (min(col_idx) >= 0)))
