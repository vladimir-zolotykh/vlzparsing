#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import operator


class Node:
    pass


class Num(Node):
    def __init__(self, val: float):
        assert isinstance(val, float)
        self.val = val

    def __eq__(self, other) -> bool:
        if isinstance(other, type(self)):
            return self.val == other.val
        else:
            return NotImplemented

    def __repr__(self) -> str:
        return f"Num({self.val})"

    def __float__(self) -> float:
        return self.val


class BinOp(Node):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right

    def __eq__(self, other) -> bool:
        if isinstance(other, type(self)):
            return self.left == other.left and self.right == other.right
        else:
            return NotImplemented

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.left}, {self.right})"

    def __float__(self) -> float:
        return self._op(float(self.left), float(self.right))


class Plus(BinOp):
    _op = operator.add


class Minus(BinOp):
    _op = operator.sub


class Mul(BinOp):
    _op = operator.mul


class Div(BinOp):
    _op = operator.truediv
