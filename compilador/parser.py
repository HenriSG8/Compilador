from .ast_nodes import Assign, Binary, Block, If, Literal, Print, Program, Read, Unary, VarDecl, Variable, While
from .tokens import Token, TokenType


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, tokens: list[Token]):
        # O parser percorre a lista de tokens produzida pelo scanner.
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Program:
        # Um programa eh uma sequencia de declaracoes/comandos ate EOF.
        statements = []
        while not self._is_at_end():
            statements.append(self._declaration())
        return Program(statements)

    def _declaration(self):
        # Declaracoes de variavel comecam por tipo; o resto eh comando.
        if self._match(TokenType.INT, TokenType.BOOL):
            return self._var_declaration(self._previous())
        return self._statement()

    def _var_declaration(self, type_token: Token) -> VarDecl:
        name = self._consume(TokenType.IDENTIFIER, "Esperado nome da variavel.")
        self._consume(TokenType.SEMICOLON, "Esperado ';' apos declaracao de variavel.")
        return VarDecl(type_token.lexeme, name)

    def _statement(self):
        # Decide qual tipo de comando sera lido olhando o proximo token.
        if self._match(TokenType.PRINT):
            return self._print_statement()
        if self._match(TokenType.LEFT_BRACE):
            return Block(self._block())
        if self._match(TokenType.IF):
            return self._if_statement()
        if self._match(TokenType.WHILE):
            return self._while_statement()
        if self._check(TokenType.IDENTIFIER):
            return self._assignment()
        raise self._error(self._peek(), "Esperado comando.")

    def _assignment(self) -> Assign:
        name = self._consume(TokenType.IDENTIFIER, "Esperado nome da variavel.")
        self._consume(TokenType.ASSIGN, "Esperado '=' em atribuicao.")
        expression = self._expression()
        self._consume(TokenType.SEMICOLON, "Esperado ';' apos atribuicao.")
        return Assign(name, expression)

    def _print_statement(self) -> Print:
        self._consume(TokenType.LEFT_PAREN, "Esperado '(' apos print.")
        expression = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Esperado ')' apos valor do print.")
        self._consume(TokenType.SEMICOLON, "Esperado ';' apos print.")
        return Print(expression)

    def _if_statement(self) -> If:
        self._consume(TokenType.LEFT_PAREN, "Esperado '(' apos if.")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Esperado ')' apos condicao do if.")
        then_branch = self._statement()
        else_branch = self._statement() if self._match(TokenType.ELSE) else None
        return If(condition, then_branch, else_branch)

    def _while_statement(self) -> While:
        self._consume(TokenType.LEFT_PAREN, "Esperado '(' apos while.")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Esperado ')' apos condicao do while.")
        body = self._statement()
        return While(condition, body)

    def _block(self):
        statements = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            statements.append(self._declaration())

        self._consume(TokenType.RIGHT_BRACE, "Esperado '}' apos bloco.")
        return statements

    def _expression(self):
        # Entrada das expressoes. A ordem abaixo implementa precedencia.
        return self._equality()

    def _equality(self):
        expr = self._comparison()
        while self._match(TokenType.EQUAL, TokenType.BANG_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expr = Binary(expr, operator, right)
        return expr

    def _comparison(self):
        expr = self._term()
        while self._match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self._previous()
            right = self._term()
            expr = Binary(expr, operator, right)
        return expr

    def _term(self):
        expr = self._factor()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous()
            right = self._factor()
            expr = Binary(expr, operator, right)
        return expr

    def _factor(self):
        expr = self._unary()
        while self._match(TokenType.STAR, TokenType.SLASH):
            operator = self._previous()
            right = self._unary()
            expr = Binary(expr, operator, right)
        return expr

    def _unary(self):
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator = self._previous()
            right = self._unary()
            return Unary(operator, right)
        return self._primary()

    def _primary(self):
        if self._match(TokenType.FALSE):
            return Literal(False)
        if self._match(TokenType.TRUE):
            return Literal(True)
        if self._match(TokenType.NUMBER):
            return Literal(self._previous().literal)
        if self._match(TokenType.IDENTIFIER):
            return Variable(self._previous())
        if self._match(TokenType.READ):
            self._consume(TokenType.LEFT_PAREN, "Esperado '(' apos read.")
            self._consume(TokenType.RIGHT_PAREN, "Esperado ')' apos read.")
            return Read()
        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Esperado ')' apos expressao.")
            return expr
        raise self._error(self._peek(), "Esperada expressao.")

    def _match(self, *types: TokenType) -> bool:
        # Se o token atual bate com algum tipo esperado, consome ele.
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _consume(self, token_type: TokenType, message: str) -> Token:
        # Consome obrigatoriamente um token; se nao vier, gera erro sintatico.
        if self._check(token_type):
            return self._advance()
        raise self._error(self._peek(), message)

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == token_type

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]

    def _error(self, token: Token, message: str) -> ParserError:
        where = "fim do arquivo" if token.type == TokenType.EOF else f"{token.lexeme!r}"
        return ParserError(f"{message} Encontrado {where} na linha {token.line}, coluna {token.column}.")
