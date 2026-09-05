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

    def one_of(self, *expected_symbols: tuple[Symbol, ...]) -> Symbol | None:
        if not (tok := self.tok):
            return None
        if (sym := tok.sym) in expected_symbols:
            return sym
        else:
            return None

    def expr(self) -> Node:
        res = self.term()
        # while (tok := self.tok) and tok.sym in (Symbol("Plus"), Symbol("Minus")):
        while tok := self.one_of(Symbol("Plus"), Symbol("Minus")):
            self._consume()
            # res = make_binop(tok.sym, res, self.term())
            res = make_binop(tok.sym, res, self.term())
        return res

    def term(self) -> Node:
        res = self.factor()
        # while (tok := self.tok) and tok.sym in (Symbol("Mul"), Symbol("Div")):
        while tok := self.one_of(Symbol("Mul"), Symbol("Div")):
            self._consume()
            # res = make_binop(tok.sym, res, self.factor())
            res = make_binop(tok.sym, res, self.factor())
        return res

    def factor(self) -> Node:
        if Symbol("LPAREN") == self.tok:
            self._consume()
            res = self.expr()
            self._expect(Symbol("RPAREN"))
        else:
            res = Num(float(self.tok.val))
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
    sexpr = "2 + (3 * 4) + 5"
    p = Parser(sexpr)
    n: Node = p.parse()
    print(n)
