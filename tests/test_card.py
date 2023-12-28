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
