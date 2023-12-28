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
