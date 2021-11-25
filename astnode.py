from enum import Enum
from tok import TokenType


class NodeType(Enum):
    PROG = 1           # the whole program
    DEF_VAR = 2        # variable definition
    DEF_FUN = 3        # function definition
    DEF_PARA = 4       # parameter definition
    BLOCK = 5          # a block of statements
    STMT_BRK = 6       # break stmt
    STMT_CONT = 7      # continue stmt
    STMT_EMPTY = 8     # empty stmt, i.e. ";"
    STMT_RET = 9       # return stmt
    STMT_IF = 10       # if stmt
    STMT_FOR = 11      # for stmt
    STMT_WHILE = 12    # while stmt
    STMT_EXPR = 13     # single expr as one stmt
    EXPR_ASSIGN = 14   # assignment
    EXPR_BINARY = 15   # binary operation
    EXPR_UNARY = 16    # unary operation
    VAR = 17           # variable
    CST = 18           # constant value
    ARRAY_ELMT = 19    # array indexing
    FCALL = 20         # function call


class ProgNode(object):
    def __init__(self, def_num, def_list):
        assert isinstance(def_list, list), "def_list must be list!"
        self.type = NodeType.PROG
        self.def_num = def_num
        # a list of node index. Each node can be global variable or function.
        self.def_list = def_list

    def info(self):
        node_info = "%s, def_num: %d, deflist: %s" % (
            self.type.name, self.def_num, self.def_list)
        return node_info


class DefVarNode(object):
    def __init__(self, data_type, var_name, is_ptr, is_glb, is_ary, is_inited,
                 init_expr, ary_size):
        assert not (
            is_ary and is_inited), "initialization with array is not supported currently!"
        assert isinstance(data_type, TokenType), "data_type must be TokenType!"
        self.type = NodeType.DEF_VAR
        # TODO: associate astnode with token location info for debugging.
        self.data_type = data_type  # TokenType. only INT supported
        self.var_name = var_name    # string. variable name
        self.is_ptr = is_ptr        # 1 for pointer type
        self.is_glb = is_glb        # 1 for global variable
        self.is_ary = is_ary        # 1 for array variable
        self.is_inited = is_inited  # 1 if initialized
        self.init_expr = init_expr  # node index. initialization expression
        self.ary_size = ary_size    # integer. array size

    def info(self):
        node_info = "%s, data_type: %s, var_name: %s, is_ptr: %d, is_glb: %d, is_ary: %d, "\
                    "is_inited: %d, init_expr(inx): %d, ary_size: %d" % (
                        self.type.name, self.data_type.name, self.var_name,
                        self.is_ptr, self.is_glb, self.is_ary, self.is_inited,
                        self.init_expr, self.ary_size)
        return node_info


class DefFuncNode(object):
    def __init__(self, ret_type, func_name, para_num, para_list, func_body):
        assert isinstance(ret_type, TokenType), "ret_type must be TokenType!"
        self.type = NodeType.DEF_FUN
        self.ret_type = ret_type    # TokenType. only INT supported
        self.func_name = func_name  # string. function name
        self.para_num = para_num    # integer. number of parameters
        self.para_list = para_list  # a list of node index. parameter defintion list
        self.func_body = func_body  # node index. function main body

    def info(self):
        node_info = "%s, ret_type: %s, func_name: %s, para_num: %d, paralist(inx): %s, "\
                    "func_body(inx): %d" % (
                        self.type.name, self.ret_type.name, self.func_name,
                        self.para_num, self.para_list, self.func_body)
        return node_info


class DefParaNode(object):
    def __init__(self, data_type, para_name, is_ptr):
        assert isinstance(data_type, TokenType), "data_type must be TokenType!"
        self.type = NodeType.DEF_PARA
        self.data_type = data_type  # TokenType. only INT supported
        self.para_name = para_name  # string. parameter name
        self.is_ptr = is_ptr        # 1 for pointer type

    def info(self):
        node_info = "%s, data_type: %s, para_name: %s, is_ptr: %d" % (
            self.type.name, self.data_type.name, self.para_name, self.is_ptr)
        return node_info


class BlockNode(object):
    def __init__(self, stmt_num, stmt_list):
        self.type = NodeType.BLOCK
        self.stmt_num = stmt_num    # int. number of statements in this block
        self.stmt_list = stmt_list  # a list of node index. each index is one statement

    def info(self):
        node_info = "%s, stmt_num: %d, stmtlist(inx): %s" % (
            self.type.name, self.stmt_num, self.stmt_list)
        return node_info


# TODO: define one base class, where the only member is type and the only method is info.
# in this way Brk/Cont/Empty can inherit this base class.


class StmtBrkNode(object):
    def __init__(self):
        self.type = NodeType.STMT_BRK

    def info(self):
        node_info = "%s" % (self.type.name)
        return node_info


class StmtContNode(object):
    def __init__(self):
        self.type = NodeType.STMT_CONT

    def info(self):
        node_info = "%s" % (self.type.name)
        return node_info


class StmtEmptyNode(object):
    def __init__(self):
        self.type = NodeType.STMT_EMPTY

    def info(self):
        node_info = "%s" % (self.type.name)
        return node_info


class StmtRetNode(object):
    def __init__(self, ret_expr):
        self.type = NodeType.STMT_RET
        self.ret_expr = ret_expr    # node index. return value expression

    def info(self):
        node_info = "%s, ret_expr(inx): %d" % (self.type.name, self.ret_expr)
        return node_info


class StmtIfNode(object):
    def __init__(self, cond_expr, then_body, has_else, else_body):
        self.type = NodeType.STMT_IF
        self.cond_expr = cond_expr  # node index. the condition expression
        self.then_body = then_body  # node index. then body
        self.has_else = has_else    # 1 if there is else block
        self.else_body = else_body  # node index. else body

    def info(self):
        node_info = "%s, cond_expr(inx): %d, then_body(inx): %d, "\
                    "has_else: %d, else_body(inx): %d" % (
                        self.type.name, self.cond_expr, self.then_body,
                        self.has_else, self.else_body)
        return node_info


class StmtForNode(object):
    def __init__(self, init_expr, bound_expr, update_expr, for_body):
        self.type = NodeType.STMT_FOR
        self.init_expr = init_expr      # node index. init expression
        self.bound_expr = bound_expr    # node index. bound expression
        self.update_expr = update_expr  # node index. update expression
        self.for_body = for_body        # node index. for body

    def info(self):
        node_info = "%s, init_expr(inx): %d, bound_expr(inx): %d, "\
                    "update_expr(inx): %d, for_body(inx): %d" % (
                        self.type.name, self.init_expr, self.bound_expr,
                        self.update_expr, self.for_body)
        return node_info


class StmtWhileNode(object):
    def __init__(self, cond_expr, while_body):
        self.type = NodeType.STMT_WHILE
        self.cond_expr = cond_expr    # node index. the condition expression
        self.while_body = while_body  # node index. while body

    def info(self):
        node_info = "%s, cond_expr(inx): %d, while_body(inx): %d" % (
            self.type.name, self.cond_expr, self.while_body)
        return node_info


class StmtExprNode(object):
    def __init__(self, stmt_expr):
        self.type = NodeType.STMT_EXPR
        self.stmt_expr = stmt_expr  # node index. single expr as the stmt

    def info(self):
        node_info = "%s, stmt_expr(inx): %d" % (self.type.name, self.stmt_expr)
        return node_info


class ExprAssignNode(object):
    def __init__(self, lval_expr, rval_expr):
        self.type = NodeType.EXPR_ASSIGN
        self.lval_expr = lval_expr  # node index. lval: var, *ptr, array indexing
        self.rval_expr = rval_expr  # node index. rval

    def info(self):
        node_info = "%s, lval_expr(inx): %d, rval_expr(inx): %d" % (
            self.type.name, self.lval_expr, self.rval_expr)
        return node_info


class ExprBinaryNode(object):
    def __init__(self, opcode, op1_expr, op2_expr):
        assert isinstance(opcode, TokenType), "opcode must be TokenType!"
        self.type = NodeType.EXPR_BINARY
        self.opcode = opcode        # TokenType. Can be ADD|SUB|MUL|DIV|GT|LT|EQ|NOT_EQ
        self.op1_expr = op1_expr    # node index. op1 expression
        self.op2_expr = op2_expr    # node index. op2 expression

    def info(self):
        node_info = "%s, opcode: %s, op1_expr(inx): %d, op2_expr(inx): %d" % (
            self.type.name, self.opcode.name, self.op1_expr, self.op2_expr)
        return node_info


class ExprUnaryNode(object):
    def __init__(self, opcode, op_expr):
        assert isinstance(opcode, TokenType), "opcode must be TokenType!"
        self.type = NodeType.EXPR_UNARY
        self.opcode = opcode        # TokenType. Can be SUB|MUL|ADDR
        self.op_expr = op_expr      # node index. operand expression

    def info(self):
        node_info = "%s, opcode: %s, op_expr(inx): %d" % (
            self.type.name, self.opcode.name, self.op_expr)
        return node_info


class VarNode(object):
    def __init__(self, var_name):
        self.type = NodeType.VAR
        self.var_name = var_name    # string. variable name

    def info(self):
        node_info = "%s, var_name: %s" % (self.type.name, self.var_name)
        return node_info


class CstNode(object):
    def __init__(self, cst_val):
        self.type = NodeType.CST
        self.cst_val = cst_val      # integer. constant value

    def neg(self):                  # negation
        self.cst_val = 0 - self.cst_val

    def info(self):
        node_info = "%s, cst_val: %d" % (self.type.name, self.cst_val)
        return node_info


class ArrayElmtNode(object):
    def __init__(self, ary_name, ary_inx):
        self.type = NodeType.ARRAY_ELMT
        self.ary_name = ary_name    # string. array name
        self.ary_inx = ary_inx      # node index. array indexing expression

    def info(self):
        node_info = "%s, ary_name: %s, ary_inx(inx) %d" % (
            self.type.name, self.ary_name, self.ary_inx)
        return node_info


class FcallNode(object):
    def __init__(self, func_name, arg_num, arg_list):
        self.type = NodeType.FCALL
        self.func_name = func_name  # string. function name
        self.arg_num = arg_num      # int. number of arguments
        self.arg_list = arg_list    # a list of node index. argument list

    def info(self):
        node_info = "%s, func_name: %s, arg_num: %d, arglist: %s" % (
            self.type.name, self.func_name, self.arg_num, self.arg_list)
        return node_info
