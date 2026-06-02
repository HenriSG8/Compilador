import unittest

from compilador.compiler import CompilationResult, compile_source


class CompilerPipelineTest(unittest.TestCase):
    def test_compiles_source_through_all_phases(self):
        result = compile_source("""
        int x;
        x = 2 + 3;
        print(x);
        """)

        self.assertIsInstance(result, CompilationResult)
        self.assertGreater(len(result.tokens), 0)
        self.assertEqual(len(result.ast.statements), 3)
        self.assertEqual([str(instruction) for instruction in result.tac], ["t1 = 2 + 3", "x = t1", "print x"])
        self.assertEqual(
            result.bytecode,
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


if __name__ == "__main__":
    unittest.main()
