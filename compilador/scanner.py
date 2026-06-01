from .tokens import KEYWORDS, Token, TokenType


class ScannerError(Exception):
    pass


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.start_column = 1

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            self.start = self.current
            self.start_column = self.column
            self._scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line, self.column))
        return self.tokens

    def _scan_token(self) -> None:
        char = self._advance()

        single_char_tokens = {
            "(": TokenType.LEFT_PAREN,
            ")": TokenType.RIGHT_PAREN,
            "{": TokenType.LEFT_BRACE,
            "}": TokenType.RIGHT_BRACE,
            ";": TokenType.SEMICOLON,
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.STAR,
        }

        if char in single_char_tokens:
            self._add_token(single_char_tokens[char])
        elif char == "/":
            if self._match("/"):
                while self._peek() != "\n" and not self._is_at_end():
                    self._advance()
            else:
                self._add_token(TokenType.SLASH)
        elif char == "=":
            self._add_token(TokenType.EQUAL if self._match("=") else TokenType.ASSIGN)
        elif char == "!":
            self._add_token(TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG)
        elif char == "<":
            self._add_token(TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS)
        elif char == ">":
            self._add_token(TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER)
        elif char in (" ", "\r", "\t"):
            return
        elif char == "\n":
            self.line += 1
            self.column = 1
        elif char.isdigit():
            self._number()
        elif char.isalpha() or char == "_":
            self._identifier()
        else:
            raise ScannerError(
                f"Caractere inesperado {char!r} na linha {self.line}, coluna {self.start_column}."
            )

    def _identifier(self) -> None:
        while self._peek().isalnum() or self._peek() == "_":
            self._advance()

        text = self.source[self.start:self.current]
        token_type = KEYWORDS.get(text, TokenType.IDENTIFIER)

        if token_type == TokenType.TRUE:
            self._add_token(token_type, True)
        elif token_type == TokenType.FALSE:
            self._add_token(token_type, False)
        else:
            self._add_token(token_type)

    def _number(self) -> None:
        while self._peek().isdigit():
            self._advance()

        text = self.source[self.start:self.current]
        self._add_token(TokenType.NUMBER, int(text))

    def _match(self, expected: str) -> bool:
        if self._is_at_end() or self.source[self.current] != expected:
            return False

        self.current += 1
        self.column += 1
        return True

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        self.column += 1
        return char

    def _add_token(self, token_type: TokenType, literal=None) -> None:
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line, self.start_column))

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)
