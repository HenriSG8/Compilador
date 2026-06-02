from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class TokenType(Enum):
    # Simbolos simples da linguagem, como parenteses, chaves e operadores.
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    SEMICOLON = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    ASSIGN = auto()
    EQUAL = auto()
    BANG = auto()
    BANG_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    INT = auto()
    BOOL = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    PRINT = auto()
    READ = auto()
    TRUE = auto()
    FALSE = auto()
    EOF = auto()


KEYWORDS = {
    # Palavras reservadas: quando o scanner encontra esses textos,
    # eles nao viram identificadores comuns.
    "int": TokenType.INT,
    "bool": TokenType.BOOL,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "print": TokenType.PRINT,
    "read": TokenType.READ,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
}


@dataclass(frozen=True)
class Token:
    # Um token guarda o tipo reconhecido, o texto original e a posicao no codigo.
    type: TokenType
    lexeme: str
    literal: Any
    line: int
    column: int

    def __repr__(self) -> str:
        return (
            f"Token({self.type.name}, lexeme={self.lexeme!r}, "
            f"literal={self.literal!r}, line={self.line}, column={self.column})"
        )
