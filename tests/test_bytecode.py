import unittest

from compilador.bytecode import BytecodeGenerator
from compilador.parser import Parser
from compilador.scanner import Scanner
from compilador.semantic import SemanticAnalyzer
from compilador.tac import TACGenerator


class BytecodeGeneratorTest(unittest.TestCase):
    def generate(self, source):
        tokens = Scanner(source).scan_tokens()
        ast = Parser(tokens).parse()
        SemanticAnalyzer().analyze(ast)
        tac = TACGenerator().generate(ast)
        return BytecodeGenerator().generate(tac)

    def test_generates_bytecode_for_arithmetic_and_print(self):
        bytecode = self.generate("""
        int x;
        x = 2 + 3;
        print(x);
        """)

        self.assertEqual(
            bytecode,
            [
                "PUSH 2",
                "PUSH 3",
                "ADD",
                "STORE t1",
                "LOAD t1",
                "STORE x",
                "LOAD x",
                "PRINT",
            ],
        )

    def test_generates_bytecode_for_conditionals(self):
        bytecode = self.generate("""
        bool ok;
        ok = true;
        if (ok) {
            print(1);
        } else {
            print(0);
        }
        """)

        self.assertIn("JMP_IF_FALSE L1", bytecode)
        self.assertIn("JMP L2", bytecode)
        self.assertIn("LABEL L1", bytecode)
        self.assertIn("LABEL L2", bytecode)


if __name__ == "__main__":
    unittest.main()
