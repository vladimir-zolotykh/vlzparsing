#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
# import pytest


class SymbolMeta(type):
    _symbols = {}

    def __call__(cls, name, pat=""):
        symbols = type(cls)._symbols
        if name not in symbols:
            symbols[name] = super().__call__(name, pat)
        return symbols[name]

    @classmethod
    def masterpat(cls):
        return "|".join(f"(?P<{name}>{sym.pat})" for name, sym in cls._symbols.items())


class Symbol(metaclass=SymbolMeta):
    def __init__(self, name, pat=""):
        # print(f"Initializing Symbol({name!r})")
        self.name = name
        self.pat = pat

    def __eq__(self, other) -> bool:
        if isinstance(other, type(self)):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        else:
            return NotImplemented

    def __repr__(self):
        return f"Symbol({self.name}, {self.pat})"


# @pytest.fixture
# def symbols():
#     SymbolMeta._symbols.clear()
#     name = Symbol("NAME", r"[A-Za-z_]\w*")
#     num = Symbol("NUM", r"\d+")
#     return name, num


# def test_symbol_eq(symbols):
#     name, num = symbols
#     assert name == "NAME"
#     assert name == Symbol("NAME")


# def test_masterpat(symbols):
#     assert SymbolMeta.masterpat() == "(?P<NAME>[A-Za-z_]\\w*)|(?P<NUM>\\d+)"


# def test_symbol(symbols):
#     name, num = symbols
#     assert str(name) == "Symbol(NAME, [A-Za-z_]\\w*)"
#     assert str(num) == "Symbol(NUM, \\d+)"
#     num2 = Symbol("NUM")
#     assert num is num2


# if __name__ == "__main__":
#     name = Symbol("NAME", r"[A-Za-z_]\w*")
#     num = Symbol("NUM", r"\d+")
#     print(num)
#     num2 = Symbol("NUM", r"\d+")
#     assert num is num2
