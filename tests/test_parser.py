import unittest

from compilador.ast_nodes import Assign, Binary, Block, If, Print, Program, VarDecl, While
from compilador.parser import Parser, ParserError
from compilador.scanner import Scanner
from compilador.tokens import TokenType


class ParserTest(unittest.TestCase):
    def parse(self, source):
        tokens = Scanner(source).scan_tokens()
        return Parser(tokens).parse()

    def test_parses_variable_declaration_and_assignment(self):
        program = self.parse("""
        int x;
        x = 10;
        """)

        self.assertIsInstance(program, Program)
        self.assertEqual(len(program.statements), 2)
        self.assertIsInstance(program.statements[0], VarDecl)
        self.assertEqual(program.statements[0].type_name, "int")
        self.assertEqual(program.statements[0].name.lexeme, "x")
        self.assertIsInstance(program.statements[1], Assign)
        self.assertEqual(program.statements[1].name.lexeme, "x")

    def test_parses_expression_precedence(self):
        program = self.parse("""
        int x;
        x = 2 + 3 * 4;
        """)

        assignment = program.statements[1]

        self.assertIsInstance(assignment.expression, Binary)
        self.assertEqual(assignment.expression.operator.type, TokenType.PLUS)
        self.assertIsInstance(assignment.expression.right, Binary)
        self.assertEqual(assignment.expression.right.operator.type, TokenType.STAR)

    def test_parses_print_statement(self):
        program = self.parse("""
        int x;
        print(x);
        """)

        self.assertIsInstance(program.statements[1], Print)

    def test_parses_if_else_with_blocks(self):
        program = self.parse("""
        bool ok;
        if (ok) {
            print(true);
        } else {
            print(false);
        }
        """)

        if_statement = program.statements[1]

        self.assertIsInstance(if_statement, If)
        self.assertIsInstance(if_statement.then_branch, Block)
        self.assertIsInstance(if_statement.else_branch, Block)

    def test_parses_while_with_block(self):
        program = self.parse("""
        bool ok;
        while (ok) {
            print(ok);
        }
        """)

        while_statement = program.statements[1]

        self.assertIsInstance(while_statement, While)
        self.assertIsInstance(while_statement.body, Block)

    def test_reports_missing_semicolon(self):
        with self.assertRaises(ParserError):
            self.parse("""
            int x
            x = 10;
            """)


if __name__ == "__main__":
    unittest.main()
