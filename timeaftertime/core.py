import numpy as np

from __future__ import annotations  # necessary until python 4.0 for future references
from typing import List, Tuple
from dataclasses import dataclass, field

if True:
    @dataclass
    class Block:
        coords: List[Tuple[int, int]] = field(default_factory=list)
        color: int = 0

        def __post_init__(self):
            assert self._are_connected(self.coords) | self.is_empty(self.coords)

        def __str__(self):
            if self.is_empty(self.coords):
                return np.arary([]).__str__()
            row_idx, col_idx = list(map(list, zip(*self.coords)))
            arr = [["-" for _ in range(max(col_idx)+1)] for _ in range(max(row_idx)+1)]
            arr = np.asarray(arr, dtype=object)
            for coord in self.coords:
                arr[coord] = self.color
            return arr.__str__().replace('\'', '')
            
        def _is_connected(self, x: Tuple[int, int], y: Tuple[int, int]):
            cond1 = (x[0] == y[0]) & (abs(x[1] - y[1])==1)
            cond2 = (x[1] == y[1]) & (abs(x[0] - y[0])==1)
            return cond1 | cond2

        def _are_connected(self, coords: List[Tuple[int, int]]):
            """Use a depth-first search (DFS) algorithm to check if all coordinates are connected.
            
            See: https://stackoverflow.com/questions/20583878/python-check-if-coordinates-of-values-in-a-grid-connect-to-one-another/20583999
            """

            if self.is_empty(coords):
                return False
            if len(set(coords)) == 1:
                return True

            def neighbors(coord, coords):
                x, y = coord
                candidates = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                return [c for c in candidates if c in coords]

            seen = set()
            frontier = [coords[0]]
            while not len(frontier) == 0:
                coord = frontier.pop()
                seen.add(coord)
                frontier.extend([n for n in neighbors(coord, coords) if not n in seen])
            return len(seen) == len(set(coords))
        
        def is_empty(self, coords):
            return len(coords) == 0
        
        def add_coord(self, coord: Tuple[int, int]):
            assert coord not in self.coords
            coords_extended = self.coords + [coord]
            assert self._are_connected(coords_extended)
            self.coords = coords_extended
        
        def add_coords(self, coords: List[Tuple[int, int]]):
            coords_extended = self.coords + coords
            assert len(coords_extended) == len(set(coords_extended))
            assert self._are_connected(coords_extended)
            self.coords = coords_extended

        def remove_coord(self, coord):
            coords = [c for c in self.coords if c != coord]
            assert self._are_connected(coords) | self.is_empty(coords)
            self.coords = coords
        
        def remove_coords(self, coords: List[Tuple[int, int]]):
            coords = [c for c in self.coords if c not in coords]
            assert self._are_connected(coords) | self.is_empty(coords)
            self.coords = coords
        
        def set_color(self, color: int):
            self.color = color

        def overlaps(self, other: Block):
            overlap = set(self.coords).intersection(set(other.coords))
            return len(overlap) > 0

        def neighbors(self, other: Block, overlap_allowed=False):
            if self.is_empty(self.coords) | self.is_empty(other.coords):
                return False
            are_neighbors = self._are_connected(self.coords + other.coords)
            are_neighbors &= self.coords != other.coords
            if not overlap_allowed:
                are_neighbors &= not self.overlaps(other)
            return are_neighbors

if True:
    @dataclass
    class Board:
        height: int = 15
        width: int = 7
        blocks: List[Block] = field(default_factory=list)
