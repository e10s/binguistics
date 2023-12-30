# pylint: disable=redefined-outer-name, unused-argument

import pytest
import binguistics.card as card


def test_LineMask_1():
    mask3 = card.LineMask(3)
    assert len(mask3) == 8

    assert mask3.ROW_0 == 0b000_000_111
    assert mask3.ROW_1 == 0b000_111_000
    assert mask3.ROW_2 == 0b111_000_000

    assert mask3.COLUMN_0 == 0b001_001_001
    assert mask3.COLUMN_1 == 0b010_010_010
    assert mask3.COLUMN_2 == 0b100_100_100

    assert mask3.DIAGONAL_1 == 0b100_010_001
    assert mask3.DIAGONAL_2 == 0b001_010_100


# graceful initializations & getters


def test_init_1():
    c = card.CardBase(3)
    assert c._size == 3
    assert c.size == 3
    assert c._state == 0
    assert c.state == 0
    assert c.free == ()
    assert c.free == ()


def test_init_2():
    s = 0b1110_0101_1100_0000
    c = card.CardBase(4, s)
    assert c._size == 4
    assert c.size == 4
    assert c._state == s
    assert c.state == s
    assert c._free == ()
    assert c.free == ()


def test_init_3():
    s = 0b1110_0101_1100_0000
    f = (5, 2, 4)
    s_f = 0b1110_0101_1111_0100
    c = card.CardBase(4, s, f)
    assert c._state == s_f
    assert c.state == s_f
    assert c._free == (2, 4, 5)
    assert c.free == (2, 4, 5)


# evil initializations & getters


def test_init_101():
    bad_f = (1, 1, 1, 2)
    s_f = 0b0000_0000_0000_0110
    c = card.CardBase(4, free=bad_f)
    assert c._state == s_f
    assert c.state == s_f
    assert c._free == (1, 2)
    assert c.free == (1, 2)


def test_init_102():
    bad_f = (-1, 1, -111, 200, 200)
    s_f = 0b0000_0000_0000_0010
    c = card.CardBase(4, free=bad_f)
    assert c._state == s_f
    assert c.state == s_f
    assert c._free == (1,)
    assert c.free == (1,)


def test_init_103():
    bad_s = 0b11_000_010_000_010
    good_s = 0b010_000_010
    c = card.CardBase(3, bad_s)
    assert c._state == good_s
    assert c.state == good_s


def test_init_104():
    bad_f = (1, 0, 1, -1, -12, 999, 4)
    bad_s = 0b11_000_010_000_010
    good_s = 0b010_010_011
    c = card.CardBase(3, bad_s, bad_f)
    assert c._state == good_s
    assert c.state == good_s
    assert c._free == (0, 1, 4)
    assert c.free == (0, 1, 4)


# graceful fillings


def test_fill_1():
    c = card.CardBase(2)
    c.fill(2)
    assert c.state == 0b01_00
    c.fill(1)
    assert c.state == 0b01_10
    c.fill(0)
    assert c.state == 0b01_11
    c.fill(3)
    assert c.state == 0b11_11


# evil fillings


def test_fill_2():
    c = card.CardBase(2)
    c.fill(-2)
    assert c.state == 0b00_00
    c.fill(1)
    assert c.state == 0b00_10
    c.fill(1)
    assert c.state == 0b00_10
    c.fill(100)
    assert c.state == 0b00_10


def test_analyze_lines_1():
    s = 0b000_010_001
    c = card.CardBase(3, s)
    assert c.analyze_lines(3) == ()
    assert c.analyze_lines(2) == (card.LineMask(3).DIAGONAL_1,)
    assert c.analyze_lines(1) == (
        card.LineMask(3).ROW_0,
        card.LineMask(3).ROW_1,
        card.LineMask(3).COLUMN_0,
        card.LineMask(3).COLUMN_1,
        card.LineMask(3).DIAGONAL_2,
    )
    assert c.analyze_lines(0) == (
        card.LineMask(3).ROW_2,
        card.LineMask(3).COLUMN_2,
    )

    s = 0b001_000_001
    f = (1, 2, 5)
    c = card.CardBase(3, s, f)
    assert c.analyze_lines(3) == (card.LineMask(3).ROW_0,)
    assert c.analyze_lines(2) == (
        card.LineMask(3).COLUMN_0,
        card.LineMask(3).COLUMN_2,
        card.LineMask(3).DIAGONAL_2,
    )
    assert c.analyze_lines(1) == (
        card.LineMask(3).ROW_1,
        card.LineMask(3).ROW_2,
        card.LineMask(3).COLUMN_1,
        card.LineMask(3).DIAGONAL_1,
    )
    assert c.analyze_lines(0) == ()

    c = card.CardBase(3)
    assert c.analyze_lines(0) == tuple(card.LineMask(3))

    c = card.CardBase(3, free=range(3 * 3))
    assert c.analyze_lines(3) == tuple(card.LineMask(3))


def test_is_bingo_1():
    s = 0b0100_1010_0100_0001_1000
    c = card.CardBase(4, s)
    assert c.is_bingo(0)
    assert not c.is_bingo(1)
    assert not c.is_bingo(2)
    assert not c.is_bingo(3)

    s = 0b0100_1111_0100_0001_1000
    c = card.CardBase(4, s)
    assert c.is_bingo(0)
    assert c.is_bingo(1)
    assert not c.is_bingo(2)
    assert not c.is_bingo(3)


def test_is_bingo_2():
    s = 0b110_010_111
    c = card.CardBase(3, s)
    assert c.is_bingo(0)
    assert c.is_bingo(1)
    assert c.is_bingo(2)
    assert c.is_bingo(3)
    assert not c.is_bingo(4)
    assert not c.is_bingo(5)

    s = 0b111_010_111
    c = card.CardBase(3, s)
    assert c.is_bingo(0)
    assert c.is_bingo(1)
    assert c.is_bingo(2)
    assert c.is_bingo(3)
    assert c.is_bingo(4)
    assert c.is_bingo(5)
    assert not c.is_bingo(6)


def test_show_1(capsys):
    c = card.CardBase(3)
    c.show(blank="0", filled="1", free="F")
    out, _ = capsys.readouterr()
    assert out == "000\n000\n000\n"

    s = 0b000_010_011
    f = (2,)
    c = card.CardBase(3, s, f)
    c.show(blank="0", filled="1", free="F")
    out, _ = capsys.readouterr()
    assert out == "11F\n010\n000\n"
