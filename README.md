# Lexical Analyzer for Compiler Design

**Course Code:** `5CS221PC` | **Domain:** Compiler Design  
**Institution:** Shri Sant Gajanan Maharaj College of Engineering (SSGMCE), Shegaon - 444203 (M.S.)  
**Academic Session:** 2026–2027  

**Submitted By:** Ms. Suhana H. Tiwari (Third Year, Fifth Semester, B.E. CSE)  
**Project Guide:** Prof. S. M. Jawake (Assistant Professor, Dept. of CSE)  
**Head of Department:** Dr. J. M. Patil (HOD, Dept. of CSE)  
**Repository:** [https://github.com/Suhana943/cd project](https://github.com/Suhana943/cd%20project)

---

## 1. Overview

This project implements a **Lexical Analyzer (Lexer / Tokenizer)** in Python using regular expressions to scan source code character-by-character / pattern-by-pattern and convert it into a structured stream of tokens (`KEYWORD`, `IDENTIFIER`, `CONSTANT`, `ASSIGN`, `COMP`, and `DELIMITER`) while ignoring whitespace and flagging invalid characters.

---

## 2. Token Classification Table

| Token Type | Regex Pattern | Description |
| :--- | :--- | :--- |
| `KEYWORD` | `\b(int\|main\|begin\|for\|to\|do\|if\|endif\|endfor\|return\|End)\b` | Reserved keywords and block markers |
| `CONSTANT` | `\b\d+\b` | Numeric integer literals |
| `IDENTIFIER` | `\b[a-zA-Z_][a-zA-Z0-9_]*\b` | Variable and array names |
| `ASSIGN` | `=` | Assignment operator |
| `COMP` | `==\|!=\|>\|<` | Relational comparison operators |
| `DELIMITER` | `[()\[\];]` | Parentheses, brackets, and semicolon |

---

## 3. Sample Input Source Code

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
```

---

## 4. Python Lexical Analyzer Code (`lexer.py`)

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
    ('SKIP',       r'[ \t\r]+'),
    ('NEWLINE',    r'\n'),
    ('MISMATCH',   r'.'),
]

tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

def tokenize(code):
    tokens = []
    line_num = 1
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NEWLINE':
            line_num += 1
        elif kind == 'SKIP':
            continue
        elif
