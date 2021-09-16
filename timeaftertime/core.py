from __future__ import annotations  # necessary until python 4.0 for future references
from typing import List, Tuple
from dataclasses import dataclass, field

if True:
    @dataclass
    class Block:
        coords: List[Tuple[int, int]] = field(default_factory=list)
        color: int = 0

        def __post_init__(self):
            assert self._are_connected(self.coords)

        def _is_connected(self, x: Tuple[int, int], y: Tuple[int, int]):
            cond1 = (x[0] == y[0]) & ((x[1] == y[1]-1) | (x[1] == y[1]+1))
            cond2 = (x[1] == y[1]) & ((x[0] == y[0]-1) | (x[0] == y[0]+1))
            return cond1 | cond2

        def _are_connected(self, coords: List[Tuple[int, int]]):
            if len(coords) == 1:
                return True
            for coord1 in coords:
                has_neighbor = False
                for coord2 in [coord for coord in coords if coord != coord1]:
                    if self._is_connected(coord1, coord2):
                        has_neighbor = True
                        continue
                if not has_neighbor:
                    return False
            return True
        
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
            coords = [coord_ for coord_ in self.coords if coord_ != coord]
            assert self._are_connected(coords)
            self.coords = coords
        
        def remove_coords(self, coords: List[Tuple[int, int]]):
            coords = [coord for coord in self.coords if coord not in coords]
            assert self._are_connected(coords)
            self.coords = coords
        
        def set_color(self, color: int):
            self.color = color

        def overlaps(self, other: Block):
            overlap = set(self.coords).intersection(set(other.coords))
            return len(overlap) > 0

        def neighbors(self, other: Block, overlap_allowed=False):
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
