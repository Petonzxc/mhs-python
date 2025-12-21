#!/usr/bin/env python3

import numpy as np
from matrix import Matrix


def save_matrix_to_file(matrix: Matrix, filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(matrix))


def main() -> None:
    np.random.seed(0)

    A = Matrix(np.random.randint(0, 10, (10, 10)).tolist())
    B = Matrix(np.random.randint(0, 10, (10, 10)).tolist())

    save_matrix_to_file(A + B, "matrix+.txt")
    save_matrix_to_file(A * B, "matrix*.txt")
    save_matrix_to_file(A @ B, "matrix@.txt")


if __name__ == "__main__":
    main()
