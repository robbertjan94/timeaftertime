import pytest

from timeaftertime.core import Block, Board

# Block tests

def test_block_empty_initialization():
    block = Block()
    assert ((block.coords == []) &
             block.color == 0)

def test_block_add_coord():
    block = Block([(0,0)], 1)
    block.add_coord((0,1))
    assert block.coords == [(0,0), (0,1)]

def test_block_add_duplicate_coord():
    block = Block([(0,0)], 1)
    with pytest.raises(AssertionError):
        block.add_coord((0,0))

def test_block_add_non_neighboring_coord_far_away():
    block = Block([(0,0)], 1)
    with pytest.raises(AssertionError):
        block.add_coord((3,3))

def test_block_add_non_neighboring_coord_diagonal():
    block = Block([(3,3)], 1)
    # all diagonal positions
    with pytest.raises(AssertionError):
        block.add_coord((4,4))
    with pytest.raises(AssertionError):
        block.add_coord((2,2))
    with pytest.raises(AssertionError):
        block.add_coord((2,4))
    with pytest.raises(AssertionError):
        block.add_coord((4,2))

def test_block_add_coords():
    block = Block([(0,0)], 1)
    block.add_coords([(0,1), (0,2)])
    assert block.coords == [(0,0), (0,1), (0,2)]

def test_block_add_duplicate_coords():
    block = Block([(0,0)], 1)
    # all duplicate coords
    with pytest.raises(AssertionError):
        block.add_coords([(0,0), (0,0)])
    # some duplicate coords (but not all)
    with pytest.raises(AssertionError):
        block.add_coords([(0,0), (0,0), (0,1)])

def test_block_add_non_neighboring_coords():
    block = Block([(0,0)], 1)
    # no neighboring coords
    with pytest.raises(AssertionError):
        block.add_coords([(0,3), (1,5), (4,2)])
    # some neighboring coords (but not all)
    with pytest.raises(AssertionError):
        block.add_coords([(0,1), (0,2), (4,2)])

def test_block_remove_coord():
    block = Block([(0,0)], 1)
    block.remove_coord((0,0))
    assert block.coords == []

def test_block_remove_coord_not_in_coords():
    block = Block([(0,0)], 1)
    block.remove_coord((0,1))
    assert block.coords == [(0,0)]

def test_block_remove_coords():
    block = Block([(0,0), (0,1)], 1)
    block.remove_coords([(0,0), (0,1)])
    assert block.coords == []

def test_block_remove_coords_some_in_coords():
    block = Block([(0,0), (0,1)], 1)
    block.remove_coords([(0,0), (0,2)])
    assert block.coords == [(0,1)]

def test_block_set_color():
    block = Block([(0,0)], 1)
    block.set_color(3)
    assert block.color == 3

def test_block_overlaps():
    # some overlap
    block1 = Block([(0,0), (0,1)])
    block2 = Block([(0,0), (1,0)])
    assert block1.overlaps(block2)
    # no overlap
    block3 = Block([(0,2), (0,3)])
    assert not block1.overlaps(block3)

def test_block_overlaps_itself():
    block = Block([(0,0), (0,1)])
    assert block.overlaps(block)

def test_block_not_overlaps_with_empty():
    block = Block([(0,0), (0,1)])
    assert not block.overlaps(Block())

def test_block_neighbors():
    # no overlap
    block1 = Block([(0,0), (0,1)])
    block2 = Block([(2,0), (1,0)])
    assert block1.neighbors(block2)
    # some overlap (not allowed)
    block3 = Block([(0,1), (0,2)])
    assert not block1.neighbors(block3)
    # some overlap (allowed)
    assert block1.neighbors(block3, overlap_allowed=True)

def test_block_not_neighbors_far_away():
    block1 = Block([(0,0), (0,1)])
    block2 = Block([(4,4), (4,5)])
    assert not block1.neighbors(block2)

def test_block_not_neighbors_itself():
    block = Block([(0,0), (0,1)])
    assert not block.neighbors(block)
    assert not block.neighbors(block, overlap_allowed=True)

def test_block_not_neighbors_with_empty():
    block = Block([(0,0), (0,1)])
    assert not block.neighbors(Block())

# Board tests

def test_board_empty_initialization():
    board = Board()
    assert ((board.height == 15) &
            (board.width == 7) &
            (board.blocks == []))