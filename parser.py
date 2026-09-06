#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
from symbolmeta import Symbol
from node import Node, Num, Plus, Minus, Mul, Div

from itertokens import Token, iter_tokens

Symbol("NAME", r"[A-Za-z_]\w*")
Symbol("NUM", r"\d+")
Symbol("WS", r"\s+")
Symbol("LPAREN", r"\(")
Symbol("RPAREN", r"\)")
Symbol("PLUS", r"\+")
Symbol("MINUS", r"-")
Symbol("MUL", r"\*")
Symbol("DIV", r"/")


def make_binop(sym: Symbol, left: Node, right: Node) -> Node:
    cls = {
        Symbol("PLUS"): Plus,
        Symbol("MINUS"): Minus,
        Symbol("MUL"): Mul,
        Symbol("DIV"): Div,
    }[sym]
    return cls(left, right)


class Parser:
    def __init__(self):
        self.tokens: Iterator[Token] | None = None
        self.tok: Token | None = None

    def parse(self, sexpr: str) -> Node:
        self.tokens = iter_tokens(sexpr)
        self._advance()
        return self.expr()

    def expr(self) -> Node:
        res = self.term()
        while (tok := self.tok) and tok.sym in (Symbol("PLUS"), Symbol("MINUS")):
            self._consume()
            res = make_binop(tok.sym, res, self.term())
        return res

    def term(self) -> Node:
        res = self.factor()
        while (tok := self.tok) and tok.sym in (Symbol("MUL"), Symbol("DIV")):
            self._consume()
            res = make_binop(tok.sym, res, self.factor())
        return res

    def factor(self) -> Node:
        if Symbol("LPAREN") == self.tok.sym:
            self._consume()
            res = self.expr()
            self._expect(Symbol("RPAREN"))
        else:
            res = Num(float(self.tok.val))
            self._consume()
        return res

    def _advance(self) -> Token:
        try:
            self.tok = next(self.tokens)
        except StopIteration:
            self.tok = None
        return self.tok

    def _consume(self) -> None:
        self.tok = next(self.tokens, None)

    def _expect(self, expected_sym: Symbol) -> None:
        assert isinstance(expected_sym, Symbol)
        if expected_sym != self.tok.sym:
            raise SyntaxError(f"{expected_sym!r} expected, got {self.tok!r}")
        self._consume()


if __name__ == "__main__":
    sexpr = "2 + (3 * 4) + 5"
    n: Node = Parser().parse(sexpr)
    print(n)
