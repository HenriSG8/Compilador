from dataclasses import dataclass
from typing import Any

from tokens import Token


class Expr:
    pass


class Stmt:
    pass


@dataclass
class Program:
    statements: list[Stmt]


@dataclass
class VarDecl(Stmt):
    type_name: str
    name: Token


@dataclass
class Assign(Stmt):
    name: Token
    expression: Expr


@dataclass
class Print(Stmt):
    expression: Expr


@dataclass
class Block(Stmt):
    statements: list[Stmt]


@dataclass
class If(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Stmt | None


@dataclass
class While(Stmt):
    condition: Expr
    body: Stmt


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr


@dataclass
class Literal(Expr):
    value: Any


@dataclass
class Variable(Expr):
    name: Token


@dataclass
class Read(Expr):
    pass
