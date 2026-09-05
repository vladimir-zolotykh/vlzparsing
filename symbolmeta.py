#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


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
        # return f"Symbol({self.name}, {self.pat})"
        return f"{self.name}"
