#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from operator import itemgetter
import pytest


class TupleMeta(type):
    def __init__(cls, clsname, bases, clsdict):
        super().__init__(clsname, bases, clsdict)
        fields = clsdict.get("_fields", [])
        for index, name in enumerate(fields):
            setattr(cls, name, property(itemgetter(index)))


class Tuple(tuple, metaclass=TupleMeta):
    def __new__(cls, *args):
        if (n := len(cls._fields)) != len(args):
            raise TypeError(f"{cls.__name__} gets exactly {n} arguments")
        return super().__new__(cls, args)


class Person(Tuple):
    _fields = ["name", "age", "salary"]


def test_person():
    bob = Person("Bob", 37, 12000)
    assert str(bob) == "('Bob', 37, 12000)"
    with pytest.raises(TypeError, match="gets exactly 3 arguments"):
        bob = Person("Bob", 37)
    with pytest.raises(TypeError, match="gets exactly 3 arguments"):
        bob = Person("Bob", 37, 12000, "Programmer")


if __name__ == "__main__":
    import sys

    pytest.main(sys.argv)
