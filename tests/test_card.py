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


def test_label_1():
    ll = range(16)
    s = 0b1110_0101_1100_0000
    c = card.Card(4, ll, s)
    assert [c.label(i) for i in range(16)] == list(range(16))


def test_label_2():
    ll = range(13)
    s = 0b1110_0101_1100_0000
    f = (5, 2, 4)
    c = card.Card(4, ll, s, f)
    assert [c.label(i) for i in range(16)] == [0, 1, None, 2, None, None] + list(
        range(3, 13)
    )


def test_label_3():
    ll = [None] * 14
    bad_f = (1, 1, 1, 2)
    c = card.Card(4, ll, free=bad_f)
    assert [c.label(i) for i in range(16)] == [None] * 16


@pytest.mark.xfail(raises=ValueError)
def test_label_101():
    ll = range(16)
    s = 0b1110_0101_1100_0000
    c = card.Card(4, ll, s)
    c.label(-1)


@pytest.mark.xfail(raises=ValueError)
def test_label_102():
    ll = range(13)
    s = 0b1110_0101_1100_0000
    f = (5, 2, 4)
    c = card.Card(4, ll, s, f)
    c.label(16)


@pytest.mark.xfail(raises=ValueError)
def test_label_103():
    ll = [None] * 23
    bad_f = (1, 1, 1, 2)
    c = card.Card(5, ll, free=bad_f)
    c.label(29)


# graceful fillings


def test_fill_by_label_1():
    ll = (100, 200, 300, 400)
    c = card.Card(2, ll)
    c.fill_by_label(300)
    assert c.state == 0b01_00
    c.fill_by_label(200)
    assert c.state == 0b01_10
    c.fill_by_label(100)
    assert c.state == 0b01_11
    c.fill_by_label(400)
    assert c.state == 0b11_11


# evil fillings


def test_fill_by_label_2():
    ll = (100, 200, 300, 400)
    c = card.Card(2, ll)
    c.fill_by_label(-100)
    assert c.state == 0b00_00
    c.fill_by_label(-200)
    assert c.state == 0b00_00
    c.fill_by_label(100)
    assert c.state == 0b00_01
    c.fill_by_label(100)
    assert c.state == 0b00_01


def test_fill_by_label_3():
    ll = [range(33), [2], iter, [2]]
    c = card.Card(2, ll)
    c.fill_by_label(iter)
    assert c.state == 0b01_00
    c.fill_by_label((2,))
    assert c.state == 0b01_00
    c.fill_by_label([2])
    assert c.state == 0b11_10
    c.fill_by_label(range(33))
    assert c.state == 0b11_11


def test_fill_by_label_4():
    ll = (100, 200, 100, 100)
    c = card.Card(2, ll)
    c.fill_by_label(100)
    assert c.state == 0b11_01
    c.fill_by_label(100)
    assert c.state == 0b11_01
    c.fill_by_label(200)
    assert c.state == 0b11_11
