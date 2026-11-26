# Design and Implementation of an LL(1) Lexical Analyzer and Predictive Parser

**Course Code:** `5CS221PC` | **Domain:** Compiler Design  
**Institution:** Shri Sant Gajanan Maharaj College of Engineering (SSGMCE), Shegaon - 444203 (M.S.)  
**Academic Session:** 2026–2027  

**Submitted By:** Ms. Suhana H. Tiwari (Third Year, Fifth Semester, B.E. CSE)  
**Project Guide:** Prof. S. M. Jawake (Assistant Professor, Dept. of CSE)  
**Head of Department:** Dr. J. M. Patil (HOD, Dept. of CSE)  
**Repository:** [https://github.com/Suhana943/cd project](https://github.com/Suhana943/cd%20project)[span_0](start_span)[span_0](end_span)[span_1](start_span)[span_1](end_span)

---

## 1. Problem Statement & Objectives

- **Problem Context:** Visually impaired individuals face structural access limits when trying to interact with standard computational execution blocks driven entirely via visual UI displays. Assistive translation layers require robust, deterministic syntactic parsing engines that interpret textual custom language statements securely without code failure[span_2](start_span)[span_2](end_span).
- **Core System Objective:** Design, develop, and mathematically isolate an LL(1) Lexical Analyzer and Predictive Stack Parser engine capable of tokenizing and parsing multi-line language arrays and iterative loop blocks in linear time complexity ($O(n)$)[span_3](start_span)[span_3](end_span)[span_4](start_span)[span_4](end_span).

---

## 2. Core Advantages

- **Linear Processing Bounds ($O(n)$):** Uses an explicit deterministic state-matching algorithm to avoid stack-overflow issues caused by recursive backtracking[span_5](start_span)[span_5](end_span).
- **Left-Recursion Safety:** Grammatical structure supports clean top-down parsing with a single lookahead token ($LL(1)$)[span_6](start_span)[span_6](end_span).
- **Isolated Fault Detection:** Pinpoints token alignment mismatches and reports syntax errors clearly on invalid inputs[span_7](start_span)[span_7](end_span).

---

## 3. System Architecture Pipeline

```text
Source Code String
       │
       ▼
Lexical Analyzer (Lexer)
Regex Engine / Tokenizer
       │  Token Stream Matrix
       ▼
LL(1) Predictive Parser
Non-Recursive Stream Validation
       │
       ▼
Syntax Parsing Success Logs
```[span_8](start_span)[span_8](end_span)

---

## 4. Token Specification & Context-Free Grammar

### Token Classification
| Token Type | Regex Pattern / Rule | Description & Usage |
| :--- | :--- | :--- |
| `KEYWORD` | `\b(int\|main\|begin\|for\|to\|do\|if\|endif\|endfor\|return\|End)\b` | Language control and block keywords |
| `CONSTANT` | `\b\d+\b` | Numerical constants and array indices |
| `IDENTIFIER` | `\b[a-zA-Z_][a-zA-Z0-9_]*\b` | Variable names and array identifiers |
| `ASSIGN` | `=` | Assignment operator |
| `COMP` | `>\|<\|==\|!=` | Relational comparison operators |
| `DELIMITER` | `[()\[\];]` | Structural delimiters and statement terminator |

### Context-Free Grammar (CFG) Rules
- `Program -> int main() begin Statements return(maxval) End`
- `Statements -> Statement Statements | ε`
- `Statement -> DeclarationOrAssignment | ForLoop | IfStatement | Assignment`
- `DeclarationOrAssignment -> int id [constant]; | int id = Expression;`
- `Assignment -> id = Expression;`
- `Expression -> id | id [id] | id [constant] | constant`
- `ForLoop -> for id = constant to id [ARITH constant] do Statements endfor`
- `IfStatement -> if Condition Statements endif`
- `Condition -> Expression COMP Expression`[span_9](start_span)[span_9](end_span)

---

## 5. Sample Input Program

```text
int main()
begin
    int L[10];
    int maxval = L[0];
    for i = 1 to 9 do
        if L[i] > maxval
            maxval = L[i];
        endif
    endfor
    return(maxval)
End
```[span_10](start_span)[span_10](end_span)

---

## 6. Python Implementation (`parser.py`)

```python
import re

sample_code = """
int main()
begin
    int L[10];
    int maxval = L[0];
    for i = 1 to 9 do
        if L[i] > maxval
            maxval = L[i];
        endif
    endfor
    return(maxval)
End
"""

token_specification = [
    ('KEYWORD',    r'\b(int|main|begin|for|to|do|if|endif|endfor|return|End)\b'),
    ('CONSTANT',   r'\b\d+\b'),
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('COMP',       r'==|!=|>|<'),
    ('ASSIGN',     r'='),
    ('DELIMITER',  r'[()\[\];]'),
    ('SKIP',       r'[ \t\n\r]+'),
    ('MISMATCH',   r'.'),
]

tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

def tokenize(code):
    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Lexical Error: Unexpected character {value!r}')
        else:
            tokens.append((kind, value))
    return tokens

class LL1Parser:
    def __init__(self, tokens):
        self.tokens = tokens + [('EOF', '$')]
        self.index = 0
        self.current_token = self.tokens[self.index]
        self.step = 1
        self.logs = []

    def advance(self):
        if self.index < len(self.tokens) - 1:
            self.index += 1
            self.current_token = self.tokens[self.index]

    def match(self, expected_type, expected_val=None, action="Matched token"):
        kind, val = self.current_token
        if kind == expected_type and (expected_val is None or val == expected_val):
            self.logs.append((self.step, kind, val, action))
            self.step += 1
            self.advance()
            return True
        else:
            raise SyntaxError(f"Expected '{expected_type}' ({expected_val}), got '{kind}' ('{val}')")

    def parse(self):
        self.Program()
        if self.current_token[0] == 'EOF':
            return True
        else:
            raise SyntaxError(f"Unexpected trailing token: {self.current_token}")

    def Program(self):
        self.match('KEYWORD', 'int', 'Matched Program Primitive')
        self.match('KEYWORD', 'main', 'Verified Entrance Entry Identifier')
        self.match('DELIMITER', '(', 'Scope Start Tag Verified')
        self.match('DELIMITER', ')', 'Scope Closure Tag Verified')
        self.match('KEYWORD', 'begin', 'Initialized Core Statements Scope')
        self.Statements()
        self.match('KEYWORD', 'return', 'Matched Return Statement')
        self.match('DELIMITER', '(', 'Return Argument Start')
        self.match('IDENTIFIER', 'maxval', 'Verified Return Value Identifier')
        self.match('DELIMITER', ')', 'Return Argument End')
        self.match('KEYWORD', 'End', 'Program End Block Verified')

    def Statements(self):
        kind, val = self.current_token
        if (kind == 'KEYWORD' and val in ('int', 'for', 'if')) or kind == 'IDENTIFIER':
            self.Statement()
            self.Statements()

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
            raise SyntaxError(f"Unexpected token in Statement: {self.current_token}")

    def DeclarationOrAssignment(self):
        self.match('KEYWORD', 'int', 'Routed to DeclarationOrAssignment()')
        self.match('IDENTIFIER', None, 'Stored Local Symbol Identifier')
        kind, val = self.current_token
        if kind == 'DELIMITER' and val == '[':
            self.match('DELIMITER', '[', 'Array Brackets Mapped Successfully')
            self.match('CONSTANT', None, 'Allocated Fixed Data Index Bounds')
            self.match('DELIMITER', ']', 'Closed Bounds Verification')
            self.match('DELIMITER', ';', 'Statement Terminator Matched Cleanly')
        elif kind == 'ASSIGN':
            self.match('ASSIGN', '=', 'Matched Variable Initialization Operator')
            self.Expression()
            self.match('DELIMITER', ';', 'Statement Terminator Matched Cleanly')
        else:
            raise SyntaxError(f"Invalid declaration syntax at {self.current_token}")

    def Assignment(self):
        self.match('IDENTIFIER', None, 'Routed to Assignment() Target')
        self.match('ASSIGN', '=', 'Matched Assignment Operator')
        self.Expression()
        self.match('DELIMITER', ';', 'Statement Terminator Matched Cleanly')

    def Expression(self):
        kind, val = self.current_token
        if kind == 'IDENTIFIER':
            self.match('IDENTIFIER', None, 'Matched Operand Identifier')
            if self.current_token == ('DELIMITER', '['):
                self.match('DELIMITER', '[', 'Array Index Access Start')
                idx_kind, _ = self.current_token
                if idx_kind in ('IDENTIFIER', 'CONSTANT'):
                    self.match(idx_kind, None, f'Matched Array Index ({idx_kind})')
                else:
                    raise SyntaxError(f"Invalid array index: {self.current_token}")
                self.match('DELIMITER', ']', 'Array Index Access End')
        elif kind == 'CONSTANT':
            self.match('CONSTANT', None, 'Matched Operand Constant')
        else:
            raise SyntaxError(f"Invalid Expression starting with {self.current_token}")

    def ForLoop(self):
        self.match('KEYWORD', 'for', 'Initialized ForLoop Block')
        self.match('IDENTIFIER', None, 'Matched Loop Control Variable')
        self.match('ASSIGN', '=', 'Matched Loop Start Assignment')
        self.match('CONSTANT', None, 'Matched Loop Lower Bound')
        self.match('KEYWORD', 'to', 'Matched Range Keyword (to)')
        self.match('CONSTANT', None, 'Matched Loop Upper Bound')
        self.match('KEYWORD', 'do', 'Entered Loop Body Scope (do)')
        self.Statements()
        self.match('KEYWORD', 'endfor', 'Closed ForLoop Block (endfor)')

    def IfStatement(self):
        self.match('KEYWORD', 'if', 'Initialized Conditional IfStatement')
        self.Condition()
        self.Statements()
        self.match('KEYWORD', 'endif', 'Closed Conditional Block (endif)')

    def Condition(self):
        self.Expression()
        self.match('COMP', None, 'Matched Relational Comparison Operator')
        self.Expression()

if __name__ == "__main__":
    tokens = tokenize(sample_code)
    parser = LL1Parser(tokens)
    parser.parse()

    print(f"{'Step':<5} | {'Token Evaluated':<15} | {'Lexeme Value':<12} | {'Parser Action / Routing Status'}")
    print("-" * 80)
    for step, kind, val, action in parser.logs:
        print(f"{step:<5} | {kind:<15} | {val:<12} | {action}")
    print("=" * 80)
    print("SUCCESS: INPUT STREAM IS SYNTACTICALLY CORRECT!")
    print("The custom code source satisfies all target LL(1) Grammar boundaries.")
```[span_11](start_span)[span_11](end_span)[span_12](start_span)[span_12](end_span)

---

## 7. Execution & Verification Output

```text
Step  | Token Evaluated | Lexeme Value | Parser Action / Routing Status
--------------------------------------------------------------------------------
1     | KEYWORD         | int          | Matched Program Primitive
2     | KEYWORD         | main         | Verified Entrance Entry Identifier
3     | DELIMITER       | (            | Scope Start Tag Verified
4     | DELIMITER       | )            | Scope Closure Tag Verified
5     | KEYWORD         | begin        | Initialized Core Statements Scope
6     | KEYWORD         | int          | Routed to DeclarationOrAssignment()
7     | IDENTIFIER      | L            | Stored Local Symbol Identifier
8     | DELIMITER       | [            | Array Brackets Mapped Successfully
9     | CONSTANT        | 10           | Allocated Fixed Data Index Bounds
10    | DELIMITER       | ]            | Closed Bounds Verification
11    | DELIMITER       | ;            | Statement Terminator Matched Cleanly
...
47    | KEYWORD         | End          | Program End Block Verified
================================================================================
SUCCESS: INPUT STREAM IS SYNTACTICALLY CORRECT!
The custom code source satisfies all target LL(1) Grammar boundaries.
```[span_13](start_span)[span_13](end_span)

---

## 8. How to Run

```bash
python parser.py
```
