from compilador.bytecode import BytecodeGenerator
from compilador.parser import Parser
from compilador.scanner import Scanner
from compilador.semantic import SemanticAnalyzer
from compilador.tac import TACGenerator


SOURCE = """
int x;
bool ok;

x = 2 + 3 * 4;
ok = x > 10;

if (ok) {
    print(x);
} else {
    print(0);
}
"""


def main() -> None:
    print("=== CODIGO FONTE ===")
    print(SOURCE.strip())

    print("\n=== FASE A: TOKENS ===")
    tokens = Scanner(SOURCE).scan_tokens()
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
