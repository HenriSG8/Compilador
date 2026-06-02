from .tac import TACInstruction


class BytecodeGenerator:
    # Mapeia operadores do TAC para instrucoes do bytecode de pilha.
    OPERATORS = {
        "+": "ADD",
        "-": "SUB",
        "*": "MUL",
        "/": "DIV",
        ">": "GT",
        ">=": "GTE",
        "<": "LT",
        "<=": "LTE",
        "==": "EQ",
        "!=": "NEQ",
    }

    def generate(self, tac: list[TACInstruction]) -> list[str]:
        # Traduz cada instrucao TAC para instrucoes simples de pilha.
        bytecode: list[str] = []

        for instruction in tac:
            if instruction.op == "assign":
                self._emit_load_value(bytecode, instruction.arg1)
                bytecode.append(f"STORE {instruction.result}")
            elif instruction.op == "binary":
                operator, right = instruction.arg2
                self._emit_load_value(bytecode, instruction.arg1)
                self._emit_load_value(bytecode, right)
                bytecode.append(self.OPERATORS[operator])
                bytecode.append(f"STORE {instruction.result}")
            elif instruction.op == "unary":
                self._emit_load_value(bytecode, instruction.arg2)
                bytecode.append("NEG" if instruction.arg1 == "-" else "NOT")
                bytecode.append(f"STORE {instruction.result}")
            elif instruction.op == "print":
                self._emit_load_value(bytecode, instruction.arg1)
                bytecode.append("PRINT")
            elif instruction.op == "read":
                bytecode.append("READ")
                bytecode.append(f"STORE {instruction.result}")
            elif instruction.op == "label":
                bytecode.append(f"LABEL {instruction.arg1}")
            elif instruction.op == "goto":
                bytecode.append(f"JMP {instruction.arg1}")
            elif instruction.op == "if_false":
                self._emit_load_value(bytecode, instruction.arg1)
                bytecode.append(f"JMP_IF_FALSE {instruction.arg2}")

        return bytecode

    def _emit_load_value(self, bytecode: list[str], value) -> None:
        # Constantes usam PUSH; variaveis e temporarios usam LOAD.
        if isinstance(value, bool):
            bytecode.append(f"PUSH {str(value).lower()}")
        elif isinstance(value, int):
            bytecode.append(f"PUSH {value}")
        else:
            bytecode.append(f"LOAD {value}")
