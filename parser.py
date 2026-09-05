#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from symbolmeta import Symbol
from node import Node, Num, Plus, Minus, Mul, Div
from token import Token, iter_tokens

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
        Symbol("Mul"): Mul,
        Symbol("Div"): Div,
    }[sym]
    return cls(left, right)


class Parser:
    def __init__(self, sexpr: str):
        self.tokens = iter_tokens(sexpr)
        self._advance()

    def expr(self) -> Node:
        res = self.term()
        while (tok := self.tok) and tok.sym in (Symbol("Plus"), Symbol("Minus")):
            self._consume()
            res = make_binop(tok.sym, res, self.term())
        return res

    def term(self) -> Node:
        res = self.factor()
        while (tok := self.tok) and tok.sym in (Symbol("Mul"), Symbol("Div")):
            self._consume()
            res = make_binop(tok.sym, res, self.factor())
        return res

    def factor(self) -> Node:
        if Symbol("LPAREN") == self.tok:
            self._consume()
            res = self.expr()
            self._expect(Symbol("RPAREN"))
        else:
            res = Num(float(self.tok))
        self._consume()
        return res

    def parse(self) -> Node:
        return self.expr()

    def _advance(self) -> Token:
        try:
            self.tok = next(self.tokens)
        except StopIteration:
            self.tok = None
        return self.tok

    def _consume(self) -> None:
        self.tok = next(self.tokens)

    def _expect(self, expected_sym: Symbol) -> None:
        if expected_sym != self.tok:
            raise SyntaxError(f"{expected_sym!r} expected, got {self.tok!r}")
        self._consume()


if __name__ == "__main__":
    p = Parser()
    sexpr = "2 + (3 * 4) + 5"
    n: Node = p.parse(sexpr)
    print(n)
