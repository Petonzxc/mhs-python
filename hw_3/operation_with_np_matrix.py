#!/usr/bin/env python3

import numpy as np
from np_matrix import MatrixNP


def main() -> None:
    np.random.seed(0)
    A = MatrixNP(np.random.randint(0, 10, (10, 10)))
    B = MatrixNP(np.random.randint(0, 10, (10, 10)))

    (A + B).save_to_file("np_matrix+.txt")
    (A * B).save_to_file("np_matrix*.txt")
    (A @ B).save_to_file("np_matrix@.txt")


if __name__ == "__main__":
    main()
