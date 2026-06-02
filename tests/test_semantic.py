import unittest

from compilador.parser import Parser
from compilador.scanner import Scanner
from compilador.semantic import SemanticAnalyzer, SemanticError


class SemanticAnalyzerTest(unittest.TestCase):
    def analyze(self, source):
        tokens = Scanner(source).scan_tokens()
        ast = Parser(tokens).parse()
        SemanticAnalyzer().analyze(ast)

    def test_accepts_valid_program(self):
        self.analyze("""
        int x;
        bool ok;
        x = 10;
        ok = x > 5;

        if (ok) {
            print(x);
        }
        """)

    def test_rejects_undeclared_variable(self):
        with self.assertRaises(SemanticError):
            self.analyze("""
            x = 10;
            """)

    def test_rejects_duplicate_variable_in_same_scope(self):
        with self.assertRaises(SemanticError):
            self.analyze("""
            int x;
            bool x;
            """)

    def test_rejects_incompatible_assignment_type(self):
        with self.assertRaises(SemanticError):
            self.analyze("""
            int x;
            x = true;
            """)

    def test_rejects_non_boolean_if_condition(self):
        with self.assertRaises(SemanticError):
            self.analyze("""
            int x;
            x = 10;
            if (x) {
                print(x);
            }
            """)

    def test_allows_inner_scope_to_shadow_variable(self):
        self.analyze("""
        int x;
        {
            bool x;
            x = true;
            print(x);
        }
        x = 1;
        """)


if __name__ == "__main__":
    unittest.main()
