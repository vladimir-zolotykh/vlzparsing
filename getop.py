#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from functools import singledispatch
from node import Plus


@singledispatch
def getop(arg):
    print(f"getop({arg!r}) not implemented")


@getop.register
def _(arg: type) -> int:
    print(f"{arg = }")
    return arg


@getop.register
def _(arg: str) -> float:
    print(f"{arg = }")
    return arg


if __name__ == "__main__":
    getop(Plus)
    getop("Plus")
