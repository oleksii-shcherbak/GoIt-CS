class LexicalError(Exception):
    """Raised when an unknown character is encountered during lexical analysis."""
    pass


class ParsingError(Exception):
    """Raised when a syntax error occurs during parsing."""
    pass


class TokenType:
    INTEGER = "INTEGER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"
    DIV = "DIV"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    EOF = "EOF"


class Token:
    """Represents a token with type and value."""
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {repr(self.value)})"


class Lexer:
    """Responsible for converting input string into a stream of tokens."""
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        """Move to the next character."""
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        """Skip whitespace characters."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Read a multi-digit integer from the input."""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Lexical analyzer that breaks input into tokens."""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())

            if self.current_char == "+":
                self.advance()
                return Token(TokenType.PLUS, "+")

            if self.current_char == "-":
                self.advance()
                return Token(TokenType.MINUS, "-")

            if self.current_char == "*":
                self.advance()
                return Token(TokenType.MUL, "*")

            if self.current_char == "/":
                self.advance()
                return Token(TokenType.DIV, "/")

            if self.current_char == "(":
                self.advance()
                return Token(TokenType.LPAREN, "(")

            if self.current_char == ")":
                self.advance()
                return Token(TokenType.RPAREN, ")")

            raise LexicalError(f"Unknown character: {self.current_char}")

        return Token(TokenType.EOF, None)


class AST:
    """Base class for all AST nodes."""
    pass


class BinOp(AST):
    """Represents a binary operation node in the AST."""
    def __init__(self, left, op_token, right):
        self.left = left
        self.op = op_token
        self.right = right


class Num(AST):
    """Represents an integer number node in the AST."""
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser:
    """Parses a sequence of tokens into an abstract syntax tree."""
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise ParsingError("Parsing error")

    def eat(self, token_type):
        """Consume the current token if it matches the expected type."""
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """factor : INTEGER | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        else:
            self.error()

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
            node = BinOp(left=node, op_token=token, right=self.factor())
        return node

    def expr(self):
        """expr : term ((PLUS | MINUS) term)*"""
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            node = BinOp(left=node, op_token=token, right=self.term())
        return node


class Interpreter:
    """Interprets (evaluates) the abstract syntax tree."""
    def __init__(self, parser):
        self.parser = parser

    def visit(self, node):
        """Dispatch method to call the appropriate visit_ method."""
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def visit_BinOp(self, node):
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == TokenType.DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method")

    def interpret(self):
        """Parse and evaluate the input expression."""
        tree = self.parser.expr()
        return self.visit(tree)


def main():
    """Command-line interface loop for evaluating arithmetic expressions."""
    while True:
        try:
            text = input("Enter an expression (or 'exit' to quit): ")
            if text.lower() == "exit":
                print("Exiting.")
                break
            lexer = Lexer(text)
            parser = Parser(lexer)
            interpreter = Interpreter(parser)
            result = interpreter.interpret()
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
