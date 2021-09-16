import numpy as np

from typing import List, Tuple
from dataclasses import dataclass

# class TimeAfterTime:
#     """Custom 'Keer op Keer 2' object"""

#     def __init__(self, width: int, height: int):
        
#         # playing field dimensions
#         self.width = width
#         self.height = height

#         # blocks
#         self.max_block_size = 6
#         self.num_colors = 5

#         # special attributes
#         self.num_stars = 13
#         self.num_dices = 5

#         self.is_generated = False

#     def _initialize():
#         pass
        
#     def generate() -> None:
        

#     def visualize() -> None:
#         if not board_is_generated:
#             pass
#         board.visualize()


class Field:
    """Main field object"""

    def __init__(self, width: int, height: int, max_block_size: int, num_colors: int):
        self.max_block_size = max_block_size
        self.num_colors = num_colors

        self.field_blocks = np.zeros([width, height], dtype=int)
        self.field_colors = np.zeros([width, height], dtype=int)
        self.is_covered = np.zeros([width, height], dtype=bool)

    def _update_coverage(self):
        self.is_covered = self.field_blocks != 0
    
    def _pick_anchor_point(self, randomized: bool=False) -> Tuple[int, int]:
        rows, cols = np.where(~self.field_is_covered)
        if randomized:
            idx = np.random.choice(range(len(rows)))
        else:
            idx = 0
        return ([rows[idx], cols[idx]])

    def _get_distance_matrix(self, anchor_point: Tuple[int, int]):
        indices = np.indices(self.field_blocks.shape, sparse=True)
        return np.linalg.norm(indices-np.asarray(anchor_point), ord=1)
    
    def _get_neighbors(self, anchor_point: Tuple[int, int]) -> np.ndarray:
        distance_matrix = self._get_distance_matrix(anchor_point)
        return np.where(distance_matrix == 1)
    
    def _get_neighbors_cond(self, anchor_point: Tuple[int, int], cond: np.ndarray) -> np.ndarray:
        return self._get_neighbors(anchor_point) & cond

    def _draw_block_color(self, anchor_point: Tuple[int, int]) -> int:
        neighbors = self._get_neighbors(anchor_point)
        neighboring_colors = self.field_colors[neighbors]
        color_candidates = [x for x in range(1,self.num_colors+1) if x not in set(neighboring_colors)]
        return np.random.choice(color_candidates,1)[0]

    def _get_color_neighbors(self, block_color: int) -> np.ndarray:
        is_color_neighbor = np.zeros(self.playing_field.shape, dtype=bool)
        rows, cols = np.where(self.playing_field == block_color)
        for row, col in zip(rows, cols):
            neighbors = self.__get_neighbors(np.array([row, col]))
            is_color_neighbor[neighbors] = True
        return is_color_neighbor

if True:
    @dataclass
    class Block:
        coords: List[Tuple[int, int]]
        color: int
        is_star: bool = False
        is_dice: bool = False

        def __post_init__(self):
            assert(self._are_neighbors(self.coords))

        def _is_neighbor(self, x: Tuple[int, int], y: Tuple[int, int]):
            cond1 = (x[0] == y[0]) & ((x[1] == y[1]-1) | (x[1] == y[1]+1))
            cond2 = (x[1] == y[1]) & ((x[0] == y[0]-1) | (x[0] == y[0]+1))
            return cond1 | cond2

        def _are_neighbors(self, coords: List[Tuple[int, int]]):
            if len(coords) == 1:
                return True
            for coord1 in coords:
                has_neighbor = False
                for coord2 in [coord for coord in coords if coord != coord1]:
                    if self._is_neighbor(coord1, coord2):
                        has_neighbor = True
                        continue
                if not has_neighbor:
                    return False
            return True
        
        def add_coord(self, coord: Tuple[int, int]):
            assert(self._are_neighbors(self.coords + [coord]))
            self.coords.append(coord)
        
        def add_coords(self, coords: List[Tuple[int, int]]):
            assert(self._are_neighbors(self.coords + coords))
            for coord in coords:
                self.add_coord(coord)

        def remove_coord(self, coord):
            coords = [coord_ for coord_ in self.coords if coord_ != coord]
            assert(self._are_neighbors(coords))
            self.coords = coords
        
        def remove_coords(self, coords: List[Tuple[int, int]]):
            coords = [coord for coord in self.coords if coord not in coords]
            assert(self._are_neighbors(coords))
            for coord in coords:
                self.remove_coord(coord)
        
        def set_color(self, color: int):
            self.color = color
        
        def set_star(self, flag: bool):
            self.is_star = flag
        
        def set_dice(self, flag: bool):
            self.is_dice = flag

if True:
    @dataclass
    class Board:
        width: int
        height: int
        blocks: List[Block]

@dataclass
class Starship:
    hitpoints: int = 50


@dataclass
class InventoryItem:
    """Class for keeping track of an item in inventory."""
    name: str
    unit_price: float
    quantity_on_hand: int = 0

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand

print(Block([(0,1), (1,1)], 1, False, False))

block1 = Block([(0,1), (1,1)], 1, False, False)
block2 = Block([(0,1), (3,1)], 1, False, False)
block3 = Block([(0,1), (1,1)], 1)

