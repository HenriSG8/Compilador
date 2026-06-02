import sys
from pathlib import Path

from compilador.bytecode import BytecodeGenerator
from compilador.parser import Parser
from compilador.scanner import Scanner
from compilador.semantic import SemanticAnalyzer
from compilador.tac import TACGenerator


DEFAULT_SOURCE_PATH = Path("examples/demo.c")


def main() -> None:
    # Este arquivo demonstra o compilador passando por todas as fases.
    source_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SOURCE_PATH
    source = source_path.read_text(encoding="utf-8")

    print("=== CODIGO FONTE ===")
    print(f"Arquivo: {source_path}")
    print(source.strip())

    print("\n=== FASE A: TOKENS ===")
    tokens = Scanner(source).scan_tokens()
    for token in tokens:
        print(token)

    print("\n=== FASE B: AST ===")
    ast = Parser(tokens).parse()
    print(ast)

    print("\n=== FASE C: SEMANTICA ===")
    SemanticAnalyzer().analyze(ast)
    print("Analise semantica concluida com sucesso!")

    print("\n=== FASE D: TAC ===")
    tac = TACGenerator().generate(ast)
    for instruction in tac:
        print(instruction)

    print("\n=== FASE E: BYTECODE ===")
    bytecode = BytecodeGenerator().generate(tac)
    for instruction in bytecode:
        print(instruction)


if __name__ == "__main__":
    main()
