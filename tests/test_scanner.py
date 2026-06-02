import unittest

from compilador.scanner import Scanner, ScannerError
from compilador.tokens import TokenType


class ScannerTest(unittest.TestCase):
    def token_types(self, source):
        return [token.type for token in Scanner(source).scan_tokens()]

    def test_scans_variable_declaration_assignment_and_print(self):
        source = """
        int x;
        x = 10 + 20;
        print(x);
        """

        types = self.token_types(source)

        self.assertEqual(
            types,
            [
                TokenType.INT,
                TokenType.IDENTIFIER,
                TokenType.SEMICOLON,
                TokenType.IDENTIFIER,
                TokenType.ASSIGN,
                TokenType.NUMBER,
                TokenType.PLUS,
                TokenType.NUMBER,
                TokenType.SEMICOLON,
                TokenType.PRINT,
                TokenType.LEFT_PAREN,
                TokenType.IDENTIFIER,
                TokenType.RIGHT_PAREN,
                TokenType.SEMICOLON,
                TokenType.EOF,
            ],
        )

    def test_distinguishes_keywords_from_identifiers(self):
        tokens = Scanner("int idade; bool ativo; if else while true false").scan_tokens()

        self.assertEqual(tokens[0].type, TokenType.INT)
        self.assertEqual(tokens[1].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[3].type, TokenType.BOOL)
        self.assertEqual(tokens[4].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[6].type, TokenType.IF)
        self.assertEqual(tokens[7].type, TokenType.ELSE)
        self.assertEqual(tokens[8].type, TokenType.WHILE)
        self.assertEqual(tokens[9].type, TokenType.TRUE)
        self.assertEqual(tokens[9].literal, True)
        self.assertEqual(tokens[10].type, TokenType.FALSE)
        self.assertEqual(tokens[10].literal, False)

    def test_scans_one_and_two_character_operators(self):
        types = self.token_types("= == ! != < <= > >= + - * /")

        self.assertEqual(
            types,
            [
                TokenType.ASSIGN,
                TokenType.EQUAL,
                TokenType.BANG,
                TokenType.BANG_EQUAL,
                TokenType.LESS,
                TokenType.LESS_EQUAL,
                TokenType.GREATER,
                TokenType.GREATER_EQUAL,
                TokenType.PLUS,
                TokenType.MINUS,
                TokenType.STAR,
                TokenType.SLASH,
                TokenType.EOF,
            ],
        )

    def test_ignores_line_comments(self):
        types = self.token_types("int x; // comentario\nprint(x);")

        self.assertEqual(
            types,
            [
                TokenType.INT,
                TokenType.IDENTIFIER,
                TokenType.SEMICOLON,
                TokenType.PRINT,
                TokenType.LEFT_PAREN,
                TokenType.IDENTIFIER,
                TokenType.RIGHT_PAREN,
                TokenType.SEMICOLON,
                TokenType.EOF,
            ],
        )

    def test_reports_unexpected_character(self):
        with self.assertRaises(ScannerError):
            Scanner("int x @ 10;").scan_tokens()


if __name__ == "__main__":
    unittest.main()
