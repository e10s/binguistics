class LineMask:
    # Each instance is a singleton.

    _instances = dict()

    def __new__(cls, m):
        if m not in cls._instances:
            row_0 = 2**m - 1
            col_0 = sum(1 << i for i in range(0, m**2, m))

            import enum

            cls._instances[m] = enum.IntEnum(
                f"LineMask_{m}",
                dict(
                    [(f"ROW_{i}", row_0 << (m * i)) for i in range(m)]
                    + [
                        (
                            f"COLUMN_{i}",
                            col_0 << i,
                        )
                        for i in range(m)
                    ]
                    + [
                        (
                            "DIAGONAL_1",
                            sum(1 << i for i in range(0, m**2, m + 1)),
                        ),
                        (
                            "DIAGONAL_2",
                            sum(
                                1 << i
                                for i in range(
                                    m - 1,
                                    m**2 - m + 1,
                                    m - 1,
                                )
                            ),
                        ),
                    ]
                ),
            )

        return cls._instances[m]


class CardBase:
    """
    This is the base class that represents a bingo card.

    A card has four important attributes: size, state, square ID, and free squares.
    If a card has a size of `n`, that means the card has `n*n` squares.
    The state of a card shows which squares are filled and which are not.
    It is an `n*n`-bit integer and its set bits correspond to filled squares.
    The `k`-th bit of a state integer means the square with the ID of `k`.
    For example, on a bingo card of size 5, the IDs are arranged as follows.

         0  1  2  3  4
         5  6  7  8  9
        10 11 12 13 14
        15 16 17 18 19
        20 21 22 23 24
    """

    from collections.abc import Iterable

    def __init__(self, size: int, state: int = 0, free: Iterable[int] = ()):
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

        self._size = size
        coverall_mask = (1 << size**2) - 1
        self._state = state & coverall_mask
        self._free = tuple(sorted(set(i for i in free if 0 <= i < size**2)))
        for i in self._free:
            self._state |= 1 << i

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
            The card's current state, indicating which squares are filled and which are not.
        """
        return self._state

    @property
    def free(self) -> tuple[int]:
        """
        Free squares in the card.

        Returns
        -------
        tuple[int]
            IDs of the free squares in the card.
        """

        return self._free
