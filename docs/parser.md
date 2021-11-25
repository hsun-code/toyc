#### Parser

Syntax. C subset

```bash
# Symbols: global variable and function
program     : KW_INT def program | nil
def         : VAR idtail | * VAR init ;
idtail      : [ CONST_VAL ] ; | ( para ) block | init ;
init        : = expr | nil

# Paramenters
para        : KW_INT paradata paralist | nil
paradata    : VAR | * VAR
paralist    : , KW_INT paradata paralist | nil

# Statments
block       : { subprogram }
subprogram  : localdef subprogram | stmt subprogram | nil

localdef    : KW_INT defdata ;
defdata     : VAR varrdef | * VAR init
varrdef     : [ CONST_VAL ] | init

stmt        : altexpr ; | KW_BREAK ; | KW_CONTINUE ; | KW_RETURN expr ;
              | ifstmt | forstmt | whilestmt

ifstmt      : KW_IF ( expr ) block elsestmt
elsestmt    : KW_ELSE block | nil
forstmt     : KW_FOR ( expr ; expr ; expr )  block
whilestmt   : KW_WHILE ( expr ) block

# Expressions
# Note: priority should be considered
#  1: a[i], foo()
#  2: *ptr, -123, &var
#  3: mul, div
#  4: add, sub
#  5: relation
#  6: assignment
altexpr     : expr | nil         # Can be empty
expr        : cmp_expr asstail
asstail     : = cmp_expr asstail | nil

cmp_expr    : add_expr cmptail
cmptail     : cmp_ops add_expr cmptail | nil
cmp_ops     : > | < | == | !=

add_expr    : mul_expr addtail
addtail     : add_ops mul_expr addtail | nil
add_ops     : + | -

mul_expr    : factor multail
multail     : mul_ops factor multail | nil
mul_ops     : * | /

factor      : unary_op val | val
unary_op    : * | - | &

val         : VAR valtail | CONST_VAL
valtail     : [ expr ] | ( args ) | nil

# Arguments
args       : expr arglist | nil
arglist    : , expr arglist | nil
```

Take `test/fib.c` as an example. Parser of `toyc` would generate the following AST.

```bash
Dump the AST
33 astnode:
0-th node: CST, cst_val: 2
1-th node: DEF_VAR, data_type: KW_INT, var_name: a, is_ptr: 0, is_glb: 1, is_ary: 0,is_inited: 1, init_expr(inx): 0, ary_size: 0
2-th node: DEF_VAR, data_type: KW_INT, var_name: p, is_ptr: 1, is_glb: 1, is_ary: 0,is_inited: 0, init_expr(inx): -1, ary_size: 0
3-th node: DEF_PARA, data_type: KW_INT, para_name: num, is_ptr: 0
4-th node: VAR, var_name: num
5-th node: CST, cst_val: 1
6-th node: EXPR_BINARY, opcode: OP_EQ, op1_expr(inx): 4, op2_expr(inx): 5
7-th node: CST, cst_val: 1
8-th node: STMT_RET, ret_expr(inx): 7
9-th node: BLOCK, stmt_num: 1, stmtlist(inx): [8]
10-th node: VAR, var_name: num
11-th node: CST, cst_val: 2
12-th node: EXPR_BINARY, opcode: OP_EQ, op1_expr(inx): 10, op2_expr(inx): 11
13-th node: CST, cst_val: 1
14-th node: STMT_RET, ret_expr(inx): 13
15-th node: BLOCK, stmt_num: 1, stmtlist(inx): [14]
16-th node: VAR, var_name: num
17-th node: CST, cst_val: 1
18-th node: EXPR_BINARY, opcode: OP_SUB, op1_expr(inx): 16, op2_expr(inx): 17
19-th node: FCALL, func_name: fib, arg_num: 1, arglist: [18]
20-th node: VAR, var_name: num
21-th node: CST, cst_val: 2
22-th node: EXPR_BINARY, opcode: OP_SUB, op1_expr(inx): 20, op2_expr(inx): 21
23-th node: FCALL, func_name: fib, arg_num: 1, arglist: [22]
24-th node: EXPR_BINARY, opcode: OP_ADD, op1_expr(inx): 19, op2_expr(inx): 23
25-th node: STMT_RET, ret_expr(inx): 24
26-th node: BLOCK, stmt_num: 1, stmtlist(inx): [25]
27-th node: STMT_IF, cond_expr(inx): 12, then_body(inx): 15,has_else: 1, else_body(inx): 26
28-th node: BLOCK, stmt_num: 1, stmtlist(inx): [27]
29-th node: STMT_IF, cond_expr(inx): 6, then_body(inx): 9,has_else: 1, else_body(inx): 28
30-th node: BLOCK, stmt_num: 1, stmtlist(inx): [29]
31-th node: DEF_FUN, ret_type: KW_INT, func_name: fib, para_num: 1, paralist(inx): [3],func_body(inx): 30
32-th node: PROG, def_num: 3, deflist: [1, 2, 31]
Done
```

Please refer to `astnode.py` and `parser.py` for more details.

