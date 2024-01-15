import binguistics.card as card
import pytest

# graceful initializations & getters


def test_init_2():
    ll = range(16)
    s = 0b1110_0101_1100_0000
    c = card.Card(4, ll, s)
    assert c._size == 4
    assert c.size == 4
    assert set(c._square_table.items()) == set(zip(range(16), range(16)))
    assert c._state == s
    assert c.state == s
    assert c.blank == (0, 1, 2, 3, 4, 5, 9, 11, 12)
    assert c.filled == (6, 7, 8, 10, 13, 14, 15)
    assert c._free == ()
    assert c.free == ()


def test_init_3():
    ll = range(13)
    s = 0b1110_0101_1100_0000
    f = (5, 2, 4)
    s_f = 0b1110_0101_1111_0100
    c = card.Card(4, ll, s, f)
    assert set(c._square_table.items()) == {(0, 0), (1, 1), (3, 2)} | set(
        zip(range(6, 16), range(3, 13))
    )
    assert c._state == s_f
    assert c.state == s_f
    assert c.blank == (0, 1, 3, 9, 11, 12)
    assert c.filled == (6, 7, 8, 10, 13, 14, 15)
    assert c._free == (2, 4, 5)
    assert c.free == (2, 4, 5)


# evil initializations & getters


def test_init_101():
    ll = [None] * 14
    bad_f = (1, 1, 1, 2)
    s_f = 0b0000_0000_0000_0110
    c = card.Card(4, ll, free=bad_f)
    assert list(c._square_table.values()) == ll
    assert c._state == s_f
    assert c.state == s_f
    assert c.blank == (0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
    assert c.filled == ()
    assert c._free == (1, 2)
    assert c.free == (1, 2)


@pytest.mark.xfail(raises=ValueError)
def test_init_102():
    short_ll = (3, 1, 4, 1, 5)
    card.Card(4, short_ll)


@pytest.mark.xfail(raises=ValueError)
def test_init_103():
    long_ll = (3, 1, 4, 1, 5, 9, 2, 6, 5, 3)
    card.Card(3, long_ll)


@pytest.mark.xfail(raises=ValueError)
def test_init_104():
    short_ll = (3, 1)
    f = (5, 6)
    card.Card(4, short_ll, free=f)


@pytest.mark.xfail(raises=ValueError)
def test_init_105():
    long_ll = (3, 1, 4, 1, 5, 9, 2, 6, 5, 3)
    f = (5, 6)
    card.Card(3, long_ll, free=f)
