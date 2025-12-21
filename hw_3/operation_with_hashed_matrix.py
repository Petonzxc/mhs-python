#!/usr/bin/env python3

from matrix import Matrix
from hashed_matrix import HashedMatrix


def save_matrix(matrix, filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(matrix))


def main() -> None:
    A = HashedMatrix([[1, 2],
                [3, 4]])
    C = HashedMatrix([[2, 1],
                [3, 5]])

    B = HashedMatrix([[1, 0],
                [0, 1]])
    D = HashedMatrix([[1, 0],
                [0, 1]])

    assert hash(A) == hash(C)
    assert A._data != C._data
    assert B._data == D._data

    AB = A @ B
    CD_hashed = C @ D

    save_matrix(AB, "AB.txt")

    C = Matrix([[2, 1],
                [3, 5]])
    D = Matrix([[1, 0],
            [0, 1]])
    
    CD = C @ D
    save_matrix(CD, "CD.txt")

    assert AB._data != CD._data
    assert AB._data == CD_hashed._data

    with open("hash.txt", "w", encoding="utf-8") as f:
        f.write(f"hash(AB) = {hash(AB)}\n")
        f.write(f"hash(CD_hashed) = {hash(CD_hashed)}\n")


if __name__ == "__main__":
    main()
