# cdd.py
# Compiler Design Project: LL(1) Lexer and Parser for Custom Grammar
import re
from tabulate import tabulate

# ==========================================
# 1. LEXER (LEXICAL ANALYZER)
# ==========================================
TOKEN_SPEC = [
    ('KEYWORD',    r'\b(int|main|begin|for|to|do|if|endif|endfor|return|End)\b'),
    ('CONSTANT',   r'\b\d+\b'),
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('ASSIGN',     r'='),
    ('COMP',       r'>|<|==|!='),
    ('ARITH',      r'\+|-|\*|/'),
    ('DELIMITER',  r'\(|\)|\{|\}|\[|\]|;|,'),
    ('SKIP',       r'[ \t\n]+'),
    ('MISMATCH',   r'.'),
]

def lex(code):
    tokens = []
    regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)
    for mo in re.finditer(regex, code):
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise SyntaxError(f"Unexpected character: '{value}'")
        else:
            tokens.append((kind, value))
    return tokens

# ==========================================
# 2. GRAMMAR DEFINITION & LL(1) PARSING
# ==========================================
# Terminals map directly to Token Types or Specific Values for Keywords/Symbols
# To keep this clean and single-file, we simulate the LL(1) Parsing Table logic for the specified structure.

class LL1Parser:
    def __init__(self, tokens):
        self.tokens = tokens + [('EOF', '$')]
        self.index = 0
        self.current_token = self.tokens[self.index]
        
    def advance(self):
        if self.index < len(self.tokens) - 1:
            self.index += 1
            self.current_token = self.tokens[self.index]

    def match(self, expected_type, expected_val=None):
        kind, val = self.current_token
        if kind == expected_type and (expected_val is None or val == expected_val):
            print(f"Matched: {kind:12} | Value: {val}")
            self.advance()
            return True
        else:
            expected = expected_val if expected_val else expected_type
            raise SyntaxError(f"Syntax Error: Expected '{expected}', but got '{val}' (Type: {kind})")

    def parse(self):
        print("\n>>> [PARSING TRACE]: Starting LL(1) Parsing Process")
        print("-" * 50)
        self.Program()
        print("-" * 50)
        if self.current_token[0] == 'EOF':
            print("\n==================================================")
            print("SUCCESS: Input string is syntactically CORRECT!")
            print("The code conforms to the LL(1) Grammar rules.")
            print("==================================================")
        else:
            raise SyntaxError("Syntax Error: Redundant tokens at the end of file.")

    # --- Grammar Rules represented as Predictive Parsing Functions ---
    def Program(self):
        # Program -> int main() begin Statements return(maxval) End
        self.match('KEYWORD', 'int')
        self.match('IDENTIFIER', 'main')
        self.match('DELIMITER', '(')
        self.match('DELIMITER', ')')
        self.match('KEYWORD', 'begin')
        self.Statements()
        self.match('KEYWORD', 'return')
        self.match('DELIMITER', '(')
        self.match('IDENTIFIER', 'maxval')
        self.match('DELIMITER', ')')
        self.match('KEYWORD', 'End')

    def Statements(self):
        # Statements -> Statement Statements | epsilon
        # First(Statement) = {int, for, if, id}
        kind, val = self.current_token
        if (kind == 'KEYWORD' and val in ['int', 'for', 'if']) or kind == 'IDENTIFIER':
            self.Statement()
            self.Statements()
        # Follow(Statements) = {return} -> handles epsilon implicitly

    def Statement(self):
        kind, val = self.current_token
        if kind == 'KEYWORD' and val == 'int':
            self.DeclarationOrAssignment()
        elif kind == 'KEYWORD' and val == 'for':
            self.ForLoop()
        elif kind == 'KEYWORD' and val == 'if':
            self.IfStatement()
        elif kind == 'IDENTIFIER':
            self.Assignment()
        else:
            raise SyntaxError(f"Invalid Statement starting with '{val}'")

    def DeclarationOrAssignment(self):
        self.match('KEYWORD', 'int')
        self.match('IDENTIFIER')
        kind, val = self.current_token
        if kind == 'DELIMITER' and val == '[': # Array Decl: int L[10];
            self.match('DELIMITER', '[')
            self.match('CONSTANT')
            self.match('DELIMITER', ']')
            self.match('DELIMITER', ';')
        elif kind == 'ASSIGN': # Init Decl: int maxval=L[0];
            self.match('ASSIGN', '=')
            self.Expression()
            self.match('DELIMITER', ';')
        else:
            raise SyntaxError(f"Expected array declaration or initialization after 'int id'")

    def Assignment(self):
        # maxval=L[i];
        self.match('IDENTIFIER')
        self.match('ASSIGN', '=')
        self.Expression()
        self.match('DELIMITER', ';')

    def Expression(self):
        # Expression -> id | id[id] | id[constant] | constant
        if self.current_token[0] == 'IDENTIFIER':
            self.match('IDENTIFIER')
            if self.current_token[0] == 'DELIMITER' and self.current_token[1] == '[':
                self.match('DELIMITER', '[')
                if self.current_token[0] == 'IDENTIFIER':
                    self.match('IDENTIFIER')
                else:
                    self.match('CONSTANT')
                self.match('DELIMITER', ']')
        elif self.current_token[0] == 'CONSTANT':
            self.match('CONSTANT')
        else:
            raise SyntaxError(f"Invalid Expression at '{self.current_token[1]}'")

    def ForLoop(self):
        # for i=1 to n-1 do Statements endfor
        self.match('KEYWORD', 'for')
        self.match('IDENTIFIER')
        self.match('ASSIGN', '=')
        self.match('CONSTANT')
        self.match('KEYWORD', 'to')
        self.match('IDENTIFIER')
        if self.current_token[0] == 'ARITH':
            self.match('ARITH')
            self.match('CONSTANT')
        self.match('KEYWORD', 'do')
        self.Statements()
        self.match('KEYWORD', 'endfor')

    def IfStatement(self):
        # if L[i]>maxval Statements endif
        self.match('KEYWORD', 'if')
        self.Condition()
        self.Statements()
        self.match('KEYWORD', 'endif')

    def Condition(self):
        self.Expression()
        self.match('COMP')
        self.Expression()

# ==========================================
# 3. MAIN EXECUTION
# ==========================================
if __name__ == '__main__':
    # Input Grammar Code Snippet from Problem Statement
    input_code = """
    int main()
    begin
    int L[10];
    int maxval=L[0]; 
    for i=1 to n-1 do
    if L[i]>maxval
    maxval=L[i];
    endif
    endfor
    return(maxval)
    End
    """
    
    print("==================================================")
    print("      COMPILER DESIGN: LL(1) LEXER & PARSER       ")
    print("==================================================")
    print("\n>>> [INPUT CODE]:")
    print(input_code.strip())
    print("-" * 50)
    
    try:
        # Step 1: Run Lexer
        tokens = lex(input_code)
        
        print("\n>>> [LEXER OUTPUT]: Generated Tokens List")
        # Format for Tabulate
        table_data = [[i+1, t[0], t[1]] for i, t in enumerate(tokens)]
        print(tabulate(table_data, headers=["Sr No.", "Token Type", "Value"], tablefmt="grid"))
        
        # Step 2: Run Parser
        parser = LL1Parser(tokens)
        parser.parse()
        
    except SyntaxError as e:
        print("\n==================================================")
        print(f"FAILED: {e}")
        print("==================================================")
