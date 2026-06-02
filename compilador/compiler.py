from dataclasses import dataclass

from .ast_nodes import Program
from .bytecode import BytecodeGenerator
from .parser import Parser
from .scanner import Scanner
from .semantic import SemanticAnalyzer
from .tac import TACGenerator, TACInstruction
from .tokens import Token


@dataclass
class CompilationResult:
    # Guarda o resultado de cada fase para facilitar testes e impressao.
    tokens: list[Token]
    ast: Program
    tac: list[TACInstruction]
    bytecode: list[str]


def compile_source(source: str) -> CompilationResult:
    # Pipeline principal: cada fase recebe o resultado da fase anterior.
    tokens = Scanner(source).scan_tokens()
    ast = Parser(tokens).parse()
    SemanticAnalyzer().analyze(ast)
    tac = TACGenerator().generate(ast)
    bytecode = BytecodeGenerator().generate(tac)

    return CompilationResult(tokens, ast, tac, bytecode)
