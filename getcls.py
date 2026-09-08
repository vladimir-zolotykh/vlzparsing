from typing import Callable
from functools import singledispatch
import operator
import pytest
from node import BinOp, Plus, Minus, Mul, Div
from symbolmeta import Symbol

OpType = Callable[[float, float], float]


@singledispatch
def getop(arg: object) -> OpType:
    raise NotImplementedError(f"getop({arg!r}) not defined")


@getop.register
def _(cls: type(BinOp)) -> OpType:
    return {
        Plus: operator.add,
        Minus: operator.sub,
        Mul: operator.mul,
        Div: operator.truediv,
    }[cls]


@getop.register
def _(cls_name: str) -> OpType:
    # return getop(eval(cls_name, globals()))
    return getop(globals()[cls_name])


@singledispatch
def getcls(arg: object) -> type:
    raise NotImplementedError(f"getcls({arg!r}) not defined")


@getcls.register
def _(sym: Symbol) -> type[BinOp]:
    return {
        Symbol("PLUS"): Plus,
        Symbol("MINUS"): Minus,
        Symbol("MUL"): Mul,
        Symbol("DIV"): Div,
    }[sym]


@getcls.register
def _(sym_name: str) -> type[BinOp]:
    return getcls(Symbol(sym_name))


def test_getcls():
    assert getop(Minus) == operator.sub
    assert getop("Minus") == operator.sub
    assert getcls(Symbol("MUL")) == Mul
    assert getcls("MUL") == Mul


if __name__ == "__main__":
    import sys

    pytest.main(sys.argv)
