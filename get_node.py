from typing import Callable
from functools import singledispatch
import operator
import pytest
from node import Node, Plus, Minus, Mul, Div
from symbolmeta import Symbol

OpType = Callable[[float, float], float]


@singledispatch
def get_op(arg) -> OpType:
    raise NotImplementedError(f"get_op({type(arg)}) not defined")


@get_op.register
def _(cls: Node) -> OpType:
    return {
        Plus: operator.add,
        Minus: operator.sub,
        Mul: operator.mul,
        Div: operator.truediv,
    }[cls]


@get_op.register
def _(cls_name: str) -> OpType:
    # return get_op(eval(cls_name, globals()))
    return get_op(globals()[cls_name])


@singledispatch
def get_node(arg) -> Node:
    raise NotImplementedError(f"get_node({type(arg)}) not defined")


@get_node.register
def _(sym: Symbol) -> Node:
    return {
        Symbol("PLUS"): Plus,
        Symbol("MINUS"): Minus,
        Symbol("MUL"): Mul,
        Symbol("DIV"): Div,
    }[sym]


@get_node.register
def _(sym_name: str) -> Node:
    return get_node(Symbol(sym_name))


def test_get_node():
    assert get_op(Minus) == operator.sub
    assert get_op("Minus") == operator.sub
    assert get_node(Symbol("MUL")) == Mul
    assert get_node("MUL") == Mul


if __name__ == "__main__":
    import sys

    pytest.main(sys.argv)
