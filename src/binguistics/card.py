import collections.abc
import enum


class _LineMaskFactory:
    # Each instance is a singleton.

    _instances: dict[int, enum.EnumMeta] = dict()

    @classmethod
    def create(cls, size: int) -> enum.EnumMeta:
        if size < 2:
            raise ValueError("size must be greater than or equal to 2")
        row_0 = 2**size - 1
        col_0 = sum(1 << i for i in range(0, size**2, size))

        LineMask_m = enum.IntEnum(  # type: ignore
            f"LineMask_{size}",
            dict(
                [(f"COLUMN_{i}", row_0 << (size * i)) for i in range(size)]
                + [
                    (
                        f"ROW_{i}",
                        col_0 << i,
                    )
                    for i in range(size)
                ]
                + [
                    (
                        "DIAGONAL_1",
                        sum(1 << i for i in range(0, size**2, size + 1)),
                    ),
                    (
                        "DIAGONAL_2",
                        sum(
                            1 << i
                            for i in range(
                                size - 1,
                                size**2 - size + 1,
                                size - 1,
                            )
                        ),
                    ),
                ]
            ),
        )

        return LineMask_m

    @classmethod
    def get(cls, size: int) -> enum.EnumMeta:
        if size not in cls._instances:
            cls._instances[size] = cls.create(size)
        return cls._instances[size]


def line_mask(size: int) -> enum.EnumMeta:
    """
    Return an `IntEnum` containing all rows, columns and diagonals in a card with
    `size`. Each member can be evaluated as an integer and its set bits correspond
    to the square IDs that make up a line.

    Parameters
    ----------
    size : int
        Card's size

    Returns
    -------
    enum.EnumMeta
        `LineMask_{size}`; `{size}` will be replaced by the actual value of `size`.

    See Also
    --------
    CardBase : Defining the relationship between square IDs and the layout of a card.
    """
    return _LineMaskFactory.get(size)


def _find_ones(nonneg_n: int) -> tuple[int, ...]:
    if nonneg_n < 0:
        raise ValueError("negative value")
    r = []
    kth = 0

    while nonneg_n > 0:
        if nonneg_n & 1:
            r.append(kth)
        kth += 1
        nonneg_n >>= 1
    return tuple(r)


class CardBase:
    """
    This is the base class that represents a bingo card.

    A card has four important attributes:
    * size
    * state
    * square IDs
    * free squares

    If a card has a size of `n`, that means the card has `n*n` squares.
    The state of a card shows which squares are filled and which are not.
    It is an `n*n`-bit integer and its set bits correspond to filled squares.
    The `k`-th bit of a state integer means the square with the ID of `k`.
    For example, on a bingo card of size 5, the IDs are arranged as follows.

        0 5 10 15 20
        1 6 11 16 21
        2 7 12 17 22
        3 8 13 18 23
        4 9 14 19 24
    """

    def __init__(
        self, size: int, state: int = 0, free: collections.abc.Iterable[int] = ()
    ):
        """
        Parameters
        ----------
        size : int
            Card's size
        state : int, optional
            Initial state, by default 0
        free : Iterable[int], optional
            IDs of free squares, by default ()
        """
        if size < 2:
            raise ValueError("size must be greater than or equal to 2")
        self._size = size

        if state < 0 or state.bit_length() > size**2:
            raise ValueError("state must be less than or equal to size**2 bits")
        self._state = state

        tmp_free = set()

        for i in free:
            if not (0 <= i < size**2):
                raise ValueError("out of range")
            tmp_free.add(i)
            self._state |= 1 << i
        self._free = tuple(sorted(tmp_free))

    @property
    def size(self) -> int:
        """
        The card size.

        Returns
        -------
        int
            The card size.
        """
        return self._size

    @property
    def state(self) -> int:
        """
        The internal card state.

        Returns
        -------
        int
            The card's current state, indicating which squares are filled
            and which are not.
        """
        return self._state

    @property
    def blank(self) -> tuple[int, ...]:
        """
        Blank squares in the card, neither filled nor free.

        Returns
        -------
        tuple[int]
            IDs of the blank squares in the card.
        """

        return _find_ones(~self.state & ((1 << self.size**2) - 1))

    @property
    def filled(self) -> tuple[int, ...]:
        """
        Filled squares in the card, not including free squares.

        Returns
        -------
        tuple[int]
            IDs of the filled squares in the card.
        """

        return tuple(i for i in _find_ones(self.state) if i not in self.free)

    @property
    def free(self) -> tuple[int, ...]:
        """
        Free squares in the card.

        Returns
        -------
        tuple[int]
            IDs of the free squares in the card.
        """

        return self._free

    def fill(self, square: int):
        """
        Fill a square whose ID is `square` if it exists in the card.

        Parameters
        ----------
        square : int
            The ID of the square.
        """
        if 0 <= square < self.size**2:
            self._state |= 1 << square

    def analyze_lines(self, k: int) -> tuple[enum.IntEnum, ...]:
        """
        Find out lines each of which is filled with `k` squares.

        Parameters
        ----------
        k : int
            Number of filled squares in a line.

        Returns
        -------
        tuple
            A tuple of `LineMask_{size}` members corresponding to the lines
            with `k` filled squares.
        """
        from collections.abc import Iterable
        from typing import cast

        return tuple(
            mask
            for mask in cast(Iterable[enum.IntEnum], line_mask(self.size))
            if (self.state & mask).bit_count() == k
        )

    def is_bingo(self, k: int = 1) -> bool:
        """
        Whether at least `k` lines are fully filled.

        Parameters
        ----------
        k : int, optional
            Number of fully filled lines, by default 1

        Returns
        -------
        bool
            Return `True` if and only if at least `k` lines are fully filled.
        """

        if k < 0:
            raise ValueError("negative value")
        return len(self.analyze_lines(self.size)) >= k

    def is_ready(self) -> bool:
        """
        Whether there is a square that will be a new completion of a line
        when it is filled.

        Returns
        -------
        bool
            Return `True` if and only if there is a square that will be a new completion
            of a line when it is filled.
        """

        return bool(self.analyze_lines(self.size - 1))

    def last_pieces_for_bingo(self) -> tuple[int, ...]:
        """
        Find which square needs to be filled to complete a line missing only one square.

        Returns
        -------
        tuple[int]
            A tuple of IDs of squares such that each of them will complete
            a line if it is filled.
        """

        from functools import reduce
        from operator import or_

        p = ((self.state & mask) ^ mask for mask in self.analyze_lines(self.size - 1))
        a = reduce(or_, p, 0)
        return _find_ones(a)

    def show(
        self, blank: str = "\u2B1A", filled: str = "\u25A9", free: str = "\U0001F193"
    ):
        """
        Pretty-print the card.

        Parameters
        ----------
        blank : str, optional
            String for blank squares, by default "\u2B1A" (Dotted Square)
        filled : str, optional
            String for filled squares, by default "\u25A9"
            (Square with Diagonal Crosshatch Fill)
        free : str, optional
            String for free squares, by default "\U0001F193" (Squared Free)
        """

        s = ""
        m = self.size
        for row in range(m):
            for col in range(m):
                square = col * m + row
                if square in self.free:
                    s += free
                    continue
                if self._state & (1 << square):
                    s += filled
                else:
                    s += blank
            s += "\n"
        print(s, end="")


class Card(CardBase):
    """
    This class represents a concrete bingo card.
    Each non-free square has its own label in addition to the four important attributes:
    * size
    * state
    * square IDs
    * free squares

    which are defined in `CardBase`. This new property allows you to
    fill any square with a particular label by specifying the label.

    For example, on a bingo card of size 5, the IDs are arranged as follows.

        0 5 10 15 20
        1 6 11 16 21
        2 7 12 17 22
        3 8 13 18 23
        4 9 14 19 24

    In this case, custom labels are arranged as follows.

        <label of ID 0> ... <label of ID 20>
        <label of ID 1> ... <label of ID 21>
        <label of ID 2> ... <label of ID 22>
        <label of ID 3> ... <label of ID 23>
        <label of ID 4> ... <label of ID 24>

    If the squares with ID 3 and 20 are free, they have no labels.

        <label of ID 0> ...      <FREE>
        <label of ID 1> ... <label of ID 21>
        <label of ID 2> ... <label of ID 22>
             <FREE>     ... <label of ID 23>
        <label of ID 4> ... <label of ID 24>
    """

    def __init__(
        self,
        size: int,
        labels: collections.abc.Iterable[object],
        state: int = 0,
        free: collections.abc.Iterable[int] = (),
    ):
        """
        Parameters
        ----------
        size : int
            Card's size
        labels : Iterable[object]
            Labels of non-free squares, in order of increasing ID.
        state : int, optional
            Initial state, by default 0
        free : Iterable[int], optional
            IDs of free squares, by default ()

        See Also
        --------
        CardBase :
            Defining the structure of a card and the meaning of
            the parameters, except `labels`, are the same.
        """

        super().__init__(size, state=state, free=free)

        sq_id_it = filter(lambda x: x not in free, range(size**2))
        self._square_table = dict(zip(sq_id_it, labels, strict=True))

    def label(self, square: int):
        """
        Return the label of a square whose ID is `square`.

        Parameters
        ----------
        square : int
            The ID of the square.

        Returns
        -------
        object
            The square's label.
        """

        if not (0 <= square < self.size**2):
            raise ValueError("out of range")

        return self._square_table.get(square)
