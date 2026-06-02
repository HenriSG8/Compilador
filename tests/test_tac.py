import unittest

from compilador.parser import Parser
from compilador.scanner import Scanner
from compilador.semantic import SemanticAnalyzer
from compilador.tac import TACGenerator


class TACGeneratorTest(unittest.TestCase):
    def generate(self, source):
        tokens = Scanner(source).scan_tokens()
        ast = Parser(tokens).parse()
        SemanticAnalyzer().analyze(ast)
        return [str(instruction) for instruction in TACGenerator().generate(ast)]

    def test_generates_tac_for_expression_and_assignment(self):
        tac = self.generate("""
        int x;
        x = 2 + 3 * 4;
        print(x);
        """)

        self.assertEqual(
            tac,
            [
                "t1 = 3 * 4",
                "t2 = 2 + t1",
                "x = t2",
                "print x",
            ],
        )

    def test_generates_tac_for_if_else(self):
        tac = self.generate("""
        bool ok;
        ok = true;
        if (ok) {
            print(1);
        } else {
            print(0);
        }
        """)

        self.assertIn("if_false ok goto L1", tac)
        self.assertIn("goto L2", tac)
        self.assertIn("label L1", tac)
        self.assertIn("label L2", tac)

    def test_generates_tac_for_while(self):
        tac = self.generate("""
        bool ok;
        ok = true;
        while (ok) {
            print(ok);
            ok = false;
        }
        """)

        self.assertEqual(tac[1], "label L1")
        self.assertIn("if_false ok goto L2", tac)
        self.assertIn("goto L1", tac)
        self.assertEqual(tac[-1], "label L2")


if __name__ == "__main__":
    unittest.main()
