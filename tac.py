from dataclasses import dataclass
from typing import Any

from ast_nodes import Assign, Binary, Block, If, Literal, Print, Program, Read, Unary, VarDecl, Variable, While


@dataclass
class TACInstruction:
    op: str
    arg1: Any = None
    arg2: Any = None
    result: Any = None

    def __str__(self) -> str:
        if self.op == "assign":
            return f"{self.result} = {self.arg1}"
        if self.op == "binary":
            return f"{self.result} = {self.arg1} {self.arg2[0]} {self.arg2[1]}"
        if self.op == "unary":
            return f"{self.result} = {self.arg1}{self.arg2}"
        if self.op == "print":
            return f"print {self.arg1}"
        if self.op == "read":
            return f"{self.result} = read"
        if self.op == "label":
            return f"label {self.arg1}"
        if self.op == "goto":
            return f"goto {self.arg1}"
        if self.op == "if_false":
            return f"if_false {self.arg1} goto {self.arg2}"
        return f"{self.op} {self.arg1} {self.arg2} {self.result}"


class TACGenerator:
    def __init__(self):
        self.instructions: list[TACInstruction] = []
        self.temp_count = 0
        self.label_count = 0

    def generate(self, program: Program) -> list[TACInstruction]:
        self.instructions = []
        for statement in program.statements:
            self._emit_stmt(statement)
        return self.instructions

    def _new_temp(self) -> str:
        self.temp_count += 1
        return f"t{self.temp_count}"

    def _new_label(self) -> str:
        self.label_count += 1
        return f"L{self.label_count}"

    def _emit_stmt(self, statement) -> None:
        if isinstance(statement, VarDecl):
            return
        if isinstance(statement, Assign):
            value = self._emit_expr(statement.expression)
            self.instructions.append(TACInstruction("assign", value, result=statement.name.lexeme))
        elif isinstance(statement, Print):
            value = self._emit_expr(statement.expression)
            self.instructions.append(TACInstruction("print", value))
        elif isinstance(statement, Block):
            for child in statement.statements:
                self._emit_stmt(child)
        elif isinstance(statement, If):
            else_label = self._new_label()
            end_label = self._new_label()
            condition = self._emit_expr(statement.condition)
            self.instructions.append(TACInstruction("if_false", condition, else_label))
            self._emit_stmt(statement.then_branch)
            self.instructions.append(TACInstruction("goto", end_label))
            self.instructions.append(TACInstruction("label", else_label))
            if statement.else_branch is not None:
                self._emit_stmt(statement.else_branch)
            self.instructions.append(TACInstruction("label", end_label))
        elif isinstance(statement, While):
            start_label = self._new_label()
            end_label = self._new_label()
            self.instructions.append(TACInstruction("label", start_label))
            condition = self._emit_expr(statement.condition)
            self.instructions.append(TACInstruction("if_false", condition, end_label))
            self._emit_stmt(statement.body)
            self.instructions.append(TACInstruction("goto", start_label))
            self.instructions.append(TACInstruction("label", end_label))

    def _emit_expr(self, expression) -> str | int | bool:
        if isinstance(expression, Literal):
            return expression.value
        if isinstance(expression, Variable):
            return expression.name.lexeme
        if isinstance(expression, Read):
            temp = self._new_temp()
            self.instructions.append(TACInstruction("read", result=temp))
            return temp
        if isinstance(expression, Unary):
            right = self._emit_expr(expression.right)
            temp = self._new_temp()
            self.instructions.append(TACInstruction("unary", expression.operator.lexeme, right, temp))
            return temp
        if isinstance(expression, Binary):
            left = self._emit_expr(expression.left)
            right = self._emit_expr(expression.right)
            temp = self._new_temp()
            self.instructions.append(TACInstruction("binary", left, (expression.operator.lexeme, right), temp))
            return temp
        raise ValueError(f"Expressao sem geracao TAC: {expression!r}")
