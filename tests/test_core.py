import pytest

from timeaftertime.core import Coord, Block, Board

# Coord tests
def test_coord_initialization():
    coord = Coord(0,0)
    assert (coord.x == 0) & (coord.y == 0)

def test_coord_eq():
    coord1 = Coord(1,2)
    coord2 = Coord(3,3)
    assert coord1 == coord1
    assert coord1 != coord2

def test_coord_iterable():
    coord = Coord(1,2)
    assert [x for x in coord] == [1,2]

def test_coord_get_neighbors():
    coord = Coord(0,0)
    neighbors = coord.get_neighbors()
    assert neighbors == [Coord(-1,0), 
                         Coord(1,0),
                         Coord(0,-1),
                         Coord(0,1)]

# Block tests

def test_block_empty_initialization():
    block = Block()
    assert ((block.coords == []) &
             block.color == 0)

def test_block_initialization():
    block = Block()
    block = Block([Coord(0,0)], 1)
    assert ((block.coords == [Coord(0,0)]) &
             block.color == 1)

def test_block_add_coord():
    block = Block([Coord(0,0)])
    block.add_coord(Coord(0,1))
    assert block.coords == [Coord(0,0), Coord(0,1)]

def test_block_add_duplicate_coord():
    block = Block([Coord(0,0)])
    with pytest.raises(AssertionError):
        block.add_coord(Coord(0,0))

def test_block_add_non_neighboring_coord_far_away():
    block = Block([Coord(0,0)])
    with pytest.raises(AssertionError):
        block.add_coord(Coord(3,3))

def test_block_add_non_neighboring_coord_diagonal():
    block = Block([Coord(3,3)])
    # all diagonal positions
    with pytest.raises(AssertionError):
        block.add_coord(Coord(4,4))
    with pytest.raises(AssertionError):
        block.add_coord(Coord(2,2))
    with pytest.raises(AssertionError):
        block.add_coord(Coord(2,4))
    with pytest.raises(AssertionError):
        block.add_coord(Coord(4,2))

def test_block_add_coords():
    block = Block([Coord(0,0)])
    block.add_coords([Coord(0,1), Coord(0,2)])
    assert block.coords == [Coord(0,0), Coord(0,1), Coord(0,2)]

def test_block_add_duplicate_coords():
    block = Block([Coord(0,0)])
    # all duplicate coords
    with pytest.raises(AssertionError):
        block.add_coords([Coord(0,0), Coord(0,0)])
    # some duplicate coords (but not all)
    with pytest.raises(AssertionError):
        block.add_coords([Coord(0,0), Coord(0,0), Coord(0,1)])

def test_block_add_non_neighboring_coords():
    block = Block([Coord(0,0)])
    # no neighboring coords
    with pytest.raises(AssertionError):
        block.add_coords([Coord(0,3), Coord(1,5), Coord(4,2)])
    # some neighboring coords (but not all)
    with pytest.raises(AssertionError):
        block.add_coords([Coord(0,1), Coord(0,2), Coord(4,2)])

def test_block_remove_coord():
    block = Block([Coord(0,0)])
    block.remove_coord(Coord(0,0))
    assert block.coords == []

def test_block_remove_coord_not_in_coords():
    block = Block([Coord(0,0)])
    block.remove_coord(Coord(0,1))
    assert block.coords == [Coord(0,0)]

def test_block_remove_coords():
    block = Block([Coord(0,0), Coord(0,1)])
    block.remove_coords([Coord(0,0), Coord(0,1)])
    assert block.coords == []

def test_block_remove_coords_some_in_coords():
    block = Block([Coord(0,0), Coord(0,1)])
    block.remove_coords([Coord(0,0), Coord(0,2)])
    assert block.coords == [Coord(0,1)]

def test_block_set_color():
    block = Block([Coord(0,0)], 1)
    assert block.color == 1
    block.set_color(3)
    assert block.color == 3

def test_block_overlaps():
    # some overlap
    block1 = Block([Coord(0,0), Coord(0,1)])
    block2 = Block([Coord(0,0), Coord(1,0)])
    assert block1.overlaps(block2)
    # no overlap
    block3 = Block([Coord(0,2), Coord(0,3)])
    assert not block1.overlaps(block3)

def test_block_overlaps_itself():
    block = Block([Coord(0,0), Coord(0,1)])
    assert block.overlaps(block)

def test_block_not_overlaps_with_empty():
    block = Block([Coord(0,0), Coord(0,1)])
    assert not block.overlaps(Block())

def test_block_neighbors():
    # no overlap
    block1 = Block([Coord(0,0), Coord(0,1)])
    block2 = Block([Coord(2,0), Coord(1,0)])
    assert block1.neighbors(block2)
    # some overlap (not allowed)
    block3 = Block([Coord(0,1), Coord(0,2)])
    assert not block1.neighbors(block3)
    # some overlap (allowed)
    assert block1.neighbors(block3, overlap_allowed=True)

def test_block_not_neighbors_far_away():
    block1 = Block([Coord(0,0), Coord(0,1)])
    block2 = Block([Coord(4,4), Coord(4,5)])
    assert not block1.neighbors(block2)

def test_block_not_neighbors_itself():
    block = Block([Coord(0,0), Coord(0,1)])
    assert not block.neighbors(block)
    assert not block.neighbors(block, overlap_allowed=True)

def test_block_not_neighbors_with_empty():
    block = Block([Coord(0,0), Coord(0,1)])
    assert not block.neighbors(Block())

# Board tests

def test_board_initialization():
    board = Board(15,7)
    assert ((board.height == 15) &
            (board.width == 7) &
            (board.blocks == []))

def test_board_add_block():
    board = Board(15,7)
    block = Block([Coord(0,0), Coord(0,1)], 1)
    board.add_block(block)
    assert len(board.blocks) == 1
    assert board.blocks[0].coords == [Coord(0,0), Coord(0,1)]
    assert board.blocks[0].color == 1

def test_board_add_blocks():
    board = Board(15,7)
    block1 = Block([Coord(0,0)], 1)
    board.add_block(block1)
    block2 = Block([Coord(2,2), Coord(3,2)], 2)
    board.add_block(block2)
    assert len(board.blocks) == 2
    assert board.blocks[1].coords == [Coord(2,2), Coord(3,2)]
    assert board.blocks[1].color == 2

def test_board_add_block_overlap():
    board = Board(15,7)
    block1 = Block([Coord(0,0)], 1)
    board.add_block(block1)
    block2 = Block([Coord(0,0), Coord(0,1)], 2)
    with pytest.raises(AssertionError):
        board.add_block(block2)

def test_board_add_block_same_color_neighbor():
    board = Board(15,7)
    block1 = Block([Coord(0,0)], 1)
    board.add_block(block1)
    block2 = Block([Coord(0,1), Coord(0,2)], 1)
    with pytest.raises(AssertionError):
        board.add_block(block2)

def test_board_add_block_outside_bounds():
    board = Board(15,7)
    block1 = Block([Coord(0,0)], 1)
    board.add_block(block1)
    block2 = Block([Coord(20,20), Coord(20,21)], 1)
    with pytest.raises(AssertionError):
        board.add_block(block2)

def test_board_remove_block():
    board = Board(15,7)
    block = Block([Coord(0,0)], 1)
    board.add_block(block)
    board.remove_block(block)
    assert len(board.blocks) == 0

def test_board_remove_blocks():
    board = Board(15,7)
    block1 = Block([Coord(0,0)], 1)
    board.add_block(block1)
    block2 = Block([Coord(2,2), Coord(3,2)], 2)
    board.add_block(block2)
    board.remove_block(block2)
    assert len(board.blocks) == 1
    board.remove_block(block1)
    assert len(board.blocks) == 0

def test_board_is_empty():
    # empty
    board = Board(2,2)
    assert board.is_empty()
    # partially filled
    block1 = Block([Coord(0,0), Coord(0,1)], 1)
    board.add_block(block1)
    assert not board.is_empty()
    # full
    block2 = Block([Coord(1,0), Coord(1,1)], 2)
    board.add_block(block2)
    assert not board.is_empty()

def test_board_is_full():
    # empty
    board = Board(2,2)
    assert not board.is_full()
    # partially filled
    block1 = Block([Coord(0,0), Coord(0,1)], 1)
    board.add_block(block1)
    assert not board.is_full()
    # full
    block2 = Block([Coord(1,0), Coord(1,1)], 2)
    board.add_block(block2)
    assert board.is_full()

def test_board_coords_available():
    board = Board(2,2)
    block = Block([Coord(0,0)], 1)
    board.add_block(block)
    available_coords = board.coords_available()
    assert len(available_coords) == 2*2-1
    assert Coord(0,0) not in available_coords

def test_board_coords_available_color_same_color():
    board = Board(2,2)
    block = Block([Coord(0,0)], 1)
    board.add_block(block)
    available_coords1 = board.coords_available_color(1)
    assert len(available_coords1) == 2*2-3
    assert available_coords1 == [Coord(1,1)]

def test_board_coords_available_color_different_color():
    board = Board(2,2)
    block = Block([Coord(0,0)], 1)
    board.add_block(block)
    available_coords2 = board.coords_available_color(2)
    assert len(available_coords2) == 2*2-1
    assert Coord(0,0) not in available_coords2
    available_coords = board.coords_available()
    assert available_coords == available_coords2