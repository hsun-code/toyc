#### Lexer

Since only a subset of C can be handled by `toyc`, a small number of tokens are defined as below:

```bash
# Keywords: int, if, while, for, break, return, continue, else
KW_INT: 'int'
KW_IF: 'if'
KW_ELSE: 'else'
KW_WHILE: 'while'
KW_FOR: 'for'
KW_BREAK: 'break'
KW_RETURN: 'return'
KW_CONTINUE: 'continue'

# Arithmetic operators
OP_ADD: '+'
OP_SUB: '-'
OP_MUL: '*'  # also used to indicate 'star' for pointers
OP_DIV: '/'

# Relation operators
OP_GT: '>'
OP_LT: '<'
OP_EQ: '=='
OP_NOT_EQ: '!='

# Address operator
OP_ADDR: '&'

# Specific signs
SIGN_SEMICOLON: ';'
SIGN_COMA: ','
SIGN_L_BRACE: '{'
SIGN_R_BRACE: '}'
SIGN_L_BRACKET: '['
SIGN_R_BRACKET: ']'
SIGN_L_PARENTHESIS: '('
SIGN_R_PARENTHESIS: ')'
SIGN_ASSIGN: '=' # assignment

# Constant value
CONST_VAL: [0-9]+ # only decimal integers are supported.

# Identifiers
VAR: [0-9, a-z, A-Z]+	# exclude Keywords and CONST_VAL
```

Take `test/fib.c` as an example. Lexer of `toyc` would tokenize it and generate the following tokens.

```bash
Get all the tokens
60 tokens:
0-th token: KW_INT, (1,1,1,3)
1-th token: VAR, a, (1,1,5,5)
2-th token: SIGN_ASSIGN, (1,1,7,7)
3-th token: CONST_VAL, 2, (1,1,9,9)
4-th token: SIGN_SEMICOLON, (1,1,10,10)
5-th token: KW_INT, (2,2,1,3)
6-th token: OP_MUL, (2,2,5,5)
7-th token: VAR, p, (2,2,6,6)
8-th token: SIGN_SEMICOLON, (2,2,7,7)
9-th token: KW_INT, (4,4,1,3)
10-th token: VAR, fib, (4,4,5,7)
11-th token: SIGN_L_PARENTHESIS, (4,4,8,8)
12-th token: KW_INT, (4,4,9,11)
13-th token: VAR, num, (4,4,13,15)
14-th token: SIGN_R_PARENTHESIS, (4,4,16,16)
15-th token: SIGN_L_BRACE, (5,5,1,1)
16-th token: KW_IF, (6,6,5,6)
17-th token: SIGN_L_PARENTHESIS, (6,6,8,8)
18-th token: VAR, num, (6,6,9,11)
19-th token: OP_EQ, (6,6,13,14)
20-th token: CONST_VAL, 1, (6,6,16,16)
21-th token: SIGN_R_PARENTHESIS, (6,6,17,17)
22-th token: SIGN_L_BRACE, (6,6,19,19)
23-th token: KW_RETURN, (7,7,9,14)
24-th token: CONST_VAL, 1, (7,7,16,16)
25-th token: SIGN_SEMICOLON, (7,7,17,17)
26-th token: SIGN_R_BRACE, (8,8,5,5)
27-th token: KW_ELSE, (8,8,7,10)
28-th token: SIGN_L_BRACE, (8,8,12,12)
29-th token: KW_IF, (9,9,9,10)
30-th token: SIGN_L_PARENTHESIS, (9,9,12,12)
31-th token: VAR, num, (9,9,13,15)
32-th token: OP_EQ, (9,9,17,18)
33-th token: CONST_VAL, 2, (9,9,20,20)
34-th token: SIGN_R_PARENTHESIS, (9,9,21,21)
35-th token: SIGN_L_BRACE, (9,9,23,23)
36-th token: KW_RETURN, (10,10,13,18)
37-th token: CONST_VAL, 1, (10,10,20,20)
38-th token: SIGN_SEMICOLON, (10,10,21,21)
39-th token: SIGN_R_BRACE, (11,11,9,9)
40-th token: KW_ELSE, (11,11,11,14)
41-th token: SIGN_L_BRACE, (11,11,16,16)
42-th token: KW_RETURN, (12,12,13,18)
43-th token: VAR, fib, (12,12,20,22)
44-th token: SIGN_L_PARENTHESIS, (12,12,23,23)
45-th token: VAR, num, (12,12,24,26)
46-th token: OP_SUB, (12,12,28,28)
47-th token: CONST_VAL, 1, (12,12,30,30)
48-th token: SIGN_R_PARENTHESIS, (12,12,31,31)
49-th token: OP_ADD, (12,12,33,33)
50-th token: VAR, fib, (12,12,35,37)
51-th token: SIGN_L_PARENTHESIS, (12,12,38,38)
52-th token: VAR, num, (12,12,39,41)
53-th token: OP_SUB, (12,12,43,43)
54-th token: CONST_VAL, 2, (12,12,45,45)
55-th token: SIGN_R_PARENTHESIS, (12,12,46,46)
56-th token: SIGN_SEMICOLON, (12,12,47,47)
57-th token: SIGN_R_BRACE, (13,13,9,9)
58-th token: SIGN_R_BRACE, (14,14,5,5)
59-th token: SIGN_R_BRACE, (15,15,1,1)
```

Please refer to `tok.py` and `lexer.py` for more details.

