import pytest
from symbolmeta import Symbol, SymbolMeta


@pytest.fixture
def symbols():
    SymbolMeta._symbols.clear()
    name = Symbol("NAME", r"[A-Za-z_]\w*")
    num = Symbol("NUM", r"\d+")
    return name, num


def test_symbol_eq(symbols):
    name, num = symbols
    assert name == "NAME"
    assert name == Symbol("NAME")


def test_masterpat(symbols):
    assert SymbolMeta.masterpat() == "(?P<NAME>[A-Za-z_]\\w*)|(?P<NUM>\\d+)"


def test_symbol(symbols):
    name, num = symbols
    assert str(name) == "Symbol(NAME, [A-Za-z_]\\w*)"
    assert str(num) == "Symbol(NUM, \\d+)"
    num2 = Symbol("NUM")
    assert num is num2
