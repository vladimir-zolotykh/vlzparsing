#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import re
from symbolmeta import Symbol, SymbolMeta


class Token:
    def __init__(self, sym: Symbol, val: object):
        self.sym = sym
        self.val = val

    def __eq__(self, other) -> bool:
        if isinstance(other, type(self)):
            return self.sym == other.sym and self.val == other.val
        else:
            return NotImplemented

    def __repr__(self) -> str:
        return f"Token({self.sym}, {self.val})"


def iter_tokens(sexpr: str) -> Iterator[Token]:
    for match in re.finditer(SymbolMeta.masterpat(), sexpr):
        if Symbol("WS") != match:
            yield Token(Symbol(match.lastgroup), match.group(0))
