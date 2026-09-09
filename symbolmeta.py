#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class SymbolMeta(type):
    _symbols = {}
    _frozen: bool = False

    def __call__(cls, name, pat="", nodecls=None):
        symbols = type(cls)._symbols
        if name not in symbols:
            if type(cls)._frozen:
                raise TypeError(f"{cls!r}: object does not support item assignment")
            symbols[name] = super().__call__(name, pat, nodecls)
        return symbols[name]

    @classmethod
    def masterpat(cls):
        cls._frozen = True
        return "|".join(f"(?P<{name}>{sym.pat})" for name, sym in cls._symbols.items())


class Symbol(metaclass=SymbolMeta):
    def __init__(self, name, pat="", nodecls=None):
        self.name = name
        self.pat = pat
        self.nodecls = nodecls

    def __eq__(self, other) -> bool:
        if isinstance(other, type(self)):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        else:
            return NotImplemented

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self):
        return f"{self.name}"
