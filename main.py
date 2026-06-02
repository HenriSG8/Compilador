import sys
from pathlib import Path

from compilador.compiler import compile_source


DEFAULT_SOURCE_PATH = Path("examples/demo.c")


def main() -> None:
    # Este arquivo demonstra o compilador passando por todas as fases.
    source_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SOURCE_PATH
    source = source_path.read_text(encoding="utf-8")

    print("=== CODIGO FONTE ===")
    print(f"Arquivo: {source_path}")
    print(source.strip())

    result = compile_source(source)

    print("\n=== FASE A: TOKENS ===")
    for token in result.tokens:
        print(token)

    print("\n=== FASE B: AST ===")
    print(result.ast)

    print("\n=== FASE C: SEMANTICA ===")
    print("Analise semantica concluida com sucesso!")

    print("\n=== FASE D: TAC ===")
    for instruction in result.tac:
        print(instruction)

    print("\n=== FASE E: BYTECODE ===")
    for instruction in result.bytecode:
        print(instruction)


if __name__ == "__main__":
    main()
