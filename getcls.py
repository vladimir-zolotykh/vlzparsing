from typing import Callable, TYPE_CHECKING
from functools import singledispatch
import operator
import pytest
from node import BinOp, Plus, Minus, Mul, Div
from symbolmeta import Symbol

OpType = Callable[[float, float], float]
if TYPE_CHECKING:
    BinOpType = type[BinOp]
else:
    BinOpType = type(BinOp)


@singledispatch
def getop(arg: object) -> OpType:
    raise NotImplementedError(f"getop({arg!r}) not defined")


@getop.register
def _(cls: BinOpType) -> OpType:
    return cls._op


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
def _(sym_name: str) -> BinOpType:
    return getcls(Symbol(sym_name))


def test_getcls():
    assert getop(Minus) == operator.sub
    assert getop("Minus") == operator.sub
    assert getcls(Symbol("MUL")) == Mul
    assert getcls("MUL") == Mul


if __name__ == "__main__":
    import sys

    pytest.main(sys.argv)
