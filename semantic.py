from ast_nodes import Assign, Binary, Block, If, Literal, Print, Program, Read, Unary, VarDecl, Variable, While
from tokens import TokenType


class SemanticError(Exception):
    pass


class SymbolTable:
    def __init__(self):
        self.scopes: list[dict[str, str]] = [{}]

    def begin_scope(self) -> None:
        self.scopes.append({})

    def end_scope(self) -> None:
        self.scopes.pop()

    def declare(self, name: str, type_name: str) -> None:
        current_scope = self.scopes[-1]
        if name in current_scope:
            raise SemanticError(f"Variavel '{name}' ja declarada neste escopo.")
        current_scope[name] = type_name

    def get(self, name: str) -> str:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise SemanticError(f"Variavel '{name}' nao declarada.")


class SemanticAnalyzer:
    def __init__(self):
        self.symbols = SymbolTable()

    def analyze(self, program: Program) -> None:
        for statement in program.statements:
            self._analyze_stmt(statement)

    def _analyze_stmt(self, statement) -> None:
        if isinstance(statement, VarDecl):
            self.symbols.declare(statement.name.lexeme, statement.type_name)
        elif isinstance(statement, Assign):
            expected_type = self.symbols.get(statement.name.lexeme)
            actual_type = self._type_of(statement.expression)
            if expected_type != actual_type:
                raise SemanticError(
                    f"Tipo invalido em '{statement.name.lexeme}': esperado {expected_type}, recebido {actual_type}."
                )
        elif isinstance(statement, Print):
            self._type_of(statement.expression)
        elif isinstance(statement, Block):
            self.symbols.begin_scope()
            for child in statement.statements:
                self._analyze_stmt(child)
            self.symbols.end_scope()
        elif isinstance(statement, If):
            self._require_bool(statement.condition, "if")
            self._analyze_stmt(statement.then_branch)
            if statement.else_branch is not None:
                self._analyze_stmt(statement.else_branch)
        elif isinstance(statement, While):
            self._require_bool(statement.condition, "while")
            self._analyze_stmt(statement.body)
        else:
            raise SemanticError(f"Comando sem regra semantica: {statement!r}")

    def _require_bool(self, expression, command_name: str) -> None:
        actual_type = self._type_of(expression)
        if actual_type != "bool":
            raise SemanticError(f"A condicao do {command_name} deve ser bool, recebeu {actual_type}.")

    def _type_of(self, expression) -> str:
        if isinstance(expression, Literal):
            return "bool" if isinstance(expression.value, bool) else "int"
        if isinstance(expression, Variable):
            return self.symbols.get(expression.name.lexeme)
        if isinstance(expression, Read):
            return "int"
        if isinstance(expression, Unary):
            right_type = self._type_of(expression.right)
            if expression.operator.type == TokenType.MINUS:
                if right_type != "int":
                    raise SemanticError("Operador '-' unario exige int.")
                return "int"
            if expression.operator.type == TokenType.BANG:
                if right_type != "bool":
                    raise SemanticError("Operador '!' exige bool.")
                return "bool"
        if isinstance(expression, Binary):
            left_type = self._type_of(expression.left)
            right_type = self._type_of(expression.right)
            operator = expression.operator.type

            if operator in (TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH):
                if left_type != "int" or right_type != "int":
                    raise SemanticError(f"Operador '{expression.operator.lexeme}' exige operandos int.")
                return "int"

            if operator in (TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
                if left_type != "int" or right_type != "int":
                    raise SemanticError(f"Operador '{expression.operator.lexeme}' exige operandos int.")
                return "bool"

            if operator in (TokenType.EQUAL, TokenType.BANG_EQUAL):
                if left_type != right_type:
                    raise SemanticError("Comparacao exige operandos do mesmo tipo.")
                return "bool"

        raise SemanticError(f"Expressao sem tipo conhecido: {expression!r}")
