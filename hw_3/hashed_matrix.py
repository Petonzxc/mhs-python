#!/usr/bin/env python3

from __future__ import annotations
from typing import List, Sequence, Dict, Tuple


class HashMixin:
    def __hash__(self) -> int:
        """
        hash(matrix) = сумма чисел в первой строке и первом столбце.
        """
        if self.rows == 0 or self.cols == 0:
            return 0

        first_row_sum = sum(self._data[0])
        first_col_sum = sum(row[0] for row in self._data)

        return int(first_row_sum + first_col_sum - self._data[0][0])


class HashedMatrix(HashMixin):
    _matmul_cache: Dict[Tuple[int, int], "HashedMatrix"] = {}


    def __init__(self, data: Sequence[Sequence[float]]):
        if not data:
            raise ValueError("Matrix cannot be empty")
        row_lengths = {len(row) for row in data}
        if len(row_lengths) != 1:
            raise ValueError("All rows in matrix must have the same length")

        self._data: List[List[float]] = [list(row) for row in data]
        self.rows = len(self._data)
        self.cols = len(self._data[0])

    def shape(self) -> tuple[int, int]:
        return self.rows, self.cols

    def __add__(self, other: HashedMatrix) -> HashedMatrix:
        if self.shape() != other.shape():
            raise ValueError(f"Cannot add matrices of shapes {self.shape()} and {other.shape()}")
        result = [
            [self._data[i][j] + other._data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return HashedMatrix(result)

    def __mul__(self, other: HashedMatrix) -> HashedMatrix:
        if self.shape() != other.shape():
            raise ValueError(f"Cannot multiply element-wise matrices of shapes {self.shape()} and {other.shape()}")
        result = [
            [self._data[i][j] * other._data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return HashedMatrix(result)

    def __matmul__(self, other: HashedMatrix) -> HashedMatrix:
        if self.cols != other.rows:
            raise ValueError(
                f"Cannot matrix-multiply shapes {self.shape()} and {other.shape()}: "
                f"{self.cols} != {other.rows}"
            )
        
        key = (hash(self), hash(other))
        if key in HashedMatrix._matmul_cache:
            return HashedMatrix._matmul_cache[key]

        result = [[0] * other.cols for _ in range(self.rows)]
        for i in range(self.rows):
            for k in range(self.cols):
                current = self._data[i][k]
                for j in range(other.cols):
                    result[i][j] += current * other._data[k][j]

        res_matrix = HashedMatrix(result)
        HashedMatrix._matmul_cache[key] = res_matrix
        return res_matrix

    def __str__(self) -> str:
        return "\n".join(" ".join(str(x) for x in row) for row in self._data)

