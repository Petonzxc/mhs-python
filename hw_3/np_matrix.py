#!/usr/bin/env python3

from __future__ import annotations

from typing import Any
import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin


class DisplayMixin:
    def __str__(self) -> str:
        return np.array2string(self._data, separator=' ')


class FileMixin:
    def save_to_file(self, filename: str, fmt: str = "%g") -> None:
        np.savetxt(filename, self._data, fmt=fmt)


class PropertiesMixin:
    @property
    def data(self) -> np.ndarray:
        return self._data

    @data.setter
    def data(self, value: Any) -> None:
        self._data = np.array(value)

    @property
    def shape(self) -> tuple[int, int]:
        return self._data.shape


class MatrixNP(NDArrayOperatorsMixin, FileMixin, DisplayMixin, PropertiesMixin):
    __array_priority__ = 1000

    def __init__(self, data: Any):
        self._data = np.array(data)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        new_inputs = []
        for x in inputs:
            if isinstance(x, MatrixNP):
                new_inputs.append(x._data)
            else:
                new_inputs.append(x)

        result = getattr(ufunc, method)(*new_inputs, **kwargs)

        if isinstance(result, np.ndarray):
            return type(self)(result)

        return result
