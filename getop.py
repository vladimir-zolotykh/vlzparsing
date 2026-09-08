#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from functools import singledispatch


@singledispatch
def getop(arg):
    print(f"getop({arg!r}) not implemented")


@getop.register
def _(arg: int) -> int:
    print(f"{arg = }")
    return arg


@getop.register
def _(arg: float) -> float:
    print(f"{arg = }")
    return arg


if __name__ == "__main__":
    getop(10)
    getop(12.5)
    getop("asdf")
