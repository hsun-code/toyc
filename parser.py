import sys

import tu
from tu import logger
from tu import SUBPHASE_TAG_STR
from tu import dump_checksum

from tok import TokenType
import astnode


chksum_file = '/tmp/toyc.ast'


################################
# global index

tok_inx = 0
astnode_inx = -1


################################
# helpers to access toks and astnodes

def CUR_TOK_TYPE():
    global tok_inx
    return tu.toks[tok_inx].type


def CUR_TOK_VAL():
    # Note: string for VAR and integer for CONST_VAL
    global tok_inx
    return tu.toks[tok_inx].value


def MOVE_NEXT():
    global tok_inx
    tok_inx = tok_inx + 1

# exit if mismatch


def MATCH_TOK(token_type):
    if CUR_TOK_TYPE() != token_type:
        global tok_inx
        err_str = "Mismatch token: %s" % (tu.toks[tok_inx].info(True))
        if tu.FLAG_CHECK == tu.FlagCheck.AST:
            dump_checksum(chksum_file, err_str)
        logger.error(err_str)
        sys.exit()

# append new astnode into tu.ast and return the index.


def NEW_NODE(node):
    global astnode_inx
    astnode_inx = astnode_inx + 1
    tu.ast.append(node)
    return astnode_inx


################################
# Algorithm: LL(1)

def parse_args(arg_list):
    if CUR_TOK_TYPE() == TokenType.SIGN_R_PARENTHESIS:
        MOVE_NEXT()
        return arg_list
    else:
        expr = parse_expr()
        arg_list.append(expr)
        if CUR_TOK_TYPE() == TokenType.SIGN_R_PARENTHESIS:
            MOVE_NEXT()
            return arg_list
        else:
            MATCH_TOK(TokenType.SIGN_COMA)
            MOVE_NEXT()
            return parse_args(arg_list)


def parse_val_expr():
    if CUR_TOK_TYPE() == TokenType.CONST_VAL:
        # constant value
        cst_val = CUR_TOK_VAL()
        MOVE_NEXT()
        return True, NEW_NODE(astnode.CstNode(cst_val))

    MATCH_TOK(TokenType.VAR)
    var_name = CUR_TOK_VAL()
    MOVE_NEXT()

    if CUR_TOK_TYPE() == TokenType.SIGN_L_BRACKET:
        # array indexing
        MOVE_NEXT()
        ary_inx = parse_expr()
        MATCH_TOK(TokenType.SIGN_R_BRACKET)
        MOVE_NEXT()
        return False, NEW_NODE(astnode.ArrayElmtNode(var_name, ary_inx))
    elif CUR_TOK_TYPE() == TokenType.SIGN_L_PARENTHESIS:
        # function call
        MOVE_NEXT()
        arg_list = list()
        arg_list = parse_args(arg_list)
        return False, NEW_NODE(astnode.FcallNode(var_name, len(arg_list), arg_list))
    else:
        # variable
        return False, NEW_NODE(astnode.VarNode(var_name))


def parse_factor():
    if CUR_TOK_TYPE() == TokenType.OP_MUL \
            or CUR_TOK_TYPE() == TokenType.OP_SUB \
            or CUR_TOK_TYPE() == TokenType.OP_ADDR:
        unary_op = CUR_TOK_TYPE()
        MOVE_NEXT()
        is_cst_val, val_expr = parse_val_expr()
        if is_cst_val:
            # No need to generate Unary Neg op for negative numbers.
            assert unary_op == TokenType.OP_SUB, "unaray_op must be OP_SUB!"
            assert isinstance(tu.ast[val_expr], astnode.CstNode), "val_expr node must be CstNode!"
            tu.ast[val_expr].neg()
            return val_expr
        else:
            return NEW_NODE(astnode.ExprUnaryNode(unary_op, val_expr))
    else:
        _, val_expr = parse_val_expr()
        return val_expr


def parse_multail(lval):
    if CUR_TOK_TYPE() == TokenType.OP_MUL \
            or CUR_TOK_TYPE() == TokenType.OP_DIV:
        mul_div_op = CUR_TOK_TYPE()
        MOVE_NEXT()
        fact = parse_factor()
        # Operator associativity: left to right
        mul_div = NEW_NODE(astnode.ExprBinaryNode(mul_div_op, lval, fact))
        return parse_multail(mul_div)
    else:
        return lval


def parse_mul_expr():
    fact = parse_factor()
    fact_or_mul = parse_multail(fact)
    return fact_or_mul


def parse_addtail(lval):
    if CUR_TOK_TYPE() == TokenType.OP_ADD \
            or CUR_TOK_TYPE() == TokenType.OP_SUB:
        add_sub_op = CUR_TOK_TYPE()
        MOVE_NEXT()
        mul_expr = parse_mul_expr()
        # Operator associativity: left to right
        add_sub = NEW_NODE(astnode.ExprBinaryNode(add_sub_op, lval, mul_expr))
        return parse_addtail(add_sub)
    else:
        return lval


def parse_add_expr():
    mul_expr = parse_mul_expr()
    mul_or_add = parse_addtail(mul_expr)
    return mul_or_add


def parse_cmptail(lval):
    if CUR_TOK_TYPE() == TokenType.OP_GT         \
            or CUR_TOK_TYPE() == TokenType.OP_LT \
            or CUR_TOK_TYPE() == TokenType.OP_EQ \
            or CUR_TOK_TYPE() == TokenType.OP_NOT_EQ:
        rel_op = CUR_TOK_TYPE()
        MOVE_NEXT()
        add_expr = parse_add_expr()
        # Operator associativity: left to right
        rel = NEW_NODE(astnode.ExprBinaryNode(rel_op, lval, add_expr))
        return parse_cmptail(rel)
    else:
        return lval


def parse_cmp_expr():
    add_expr = parse_add_expr()
    add_or_cmp = parse_cmptail(add_expr)
    return add_or_cmp


def parse_asstail(lval):
    if CUR_TOK_TYPE() == TokenType.SIGN_ASSIGN:
        MOVE_NEXT()
        cmp_expr = parse_cmp_expr()
        # Operator associativity: right to left
        cmp_or_ass = parse_asstail(cmp_expr)
        return NEW_NODE(astnode.ExprAssignNode(lval, cmp_or_ass))
    else:
        return lval


def parse_expr():
    cmp_expr = parse_cmp_expr()
    cmp_or_ass = parse_asstail(cmp_expr)
    return cmp_or_ass


def parse_para(para_list):
    MATCH_TOK(TokenType.KW_INT)
    MOVE_NEXT()

    is_ptr = 0
    if CUR_TOK_TYPE() == TokenType.OP_MUL:
        is_ptr = 1
        MOVE_NEXT()

    MATCH_TOK(TokenType.VAR)
    para_name = CUR_TOK_VAL()
    MOVE_NEXT()
    para = NEW_NODE(astnode.DefParaNode(TokenType.KW_INT, para_name, is_ptr))
    para_list.append(para)

    if CUR_TOK_TYPE() == TokenType.SIGN_COMA:
        MOVE_NEXT()
        return parse_para(para_list)
    else:
        return para_list


def parse_init_expr():
    is_inited = 0
    init_expr = -1

    if CUR_TOK_TYPE() == TokenType.SIGN_ASSIGN:
        is_inited = 1
        MOVE_NEXT()
        init_expr = parse_expr()

    return is_inited, init_expr


def parse_def(type, is_glb):
    if CUR_TOK_TYPE() == TokenType.OP_MUL:
        # pointer variable
        MOVE_NEXT()

        MATCH_TOK(TokenType.VAR)
        var_name = CUR_TOK_VAL()
        MOVE_NEXT()
        is_inited, init_expr = parse_init_expr()

        MATCH_TOK(TokenType.SIGN_SEMICOLON)
        MOVE_NEXT()

        return NEW_NODE(
            astnode.DefVarNode(type, var_name, 1, is_glb, 0, is_inited, init_expr, 0))
    elif CUR_TOK_TYPE() == TokenType.VAR:
        var_name = CUR_TOK_VAL()
        MOVE_NEXT()

        if CUR_TOK_TYPE() == TokenType.SIGN_L_BRACKET:
            # array. TODO: not support array initialization
            MOVE_NEXT()

            MATCH_TOK(TokenType.CONST_VAL)
            ary_size = CUR_TOK_VAL()
            MOVE_NEXT()

            MATCH_TOK(TokenType.SIGN_R_BRACKET)
            MOVE_NEXT()
            MATCH_TOK(TokenType.SIGN_SEMICOLON)
            MOVE_NEXT()

            return NEW_NODE(
                astnode.DefVarNode(type, var_name, 0, is_glb, 1, 0, -1, ary_size))
        elif is_glb == 1 and CUR_TOK_TYPE() == TokenType.SIGN_L_PARENTHESIS:
            # function: is_glb must be 1
            MOVE_NEXT()

            para_list = list()
            if CUR_TOK_TYPE() != TokenType.SIGN_R_PARENTHESIS:
                para_list = parse_para(para_list)

            MATCH_TOK(TokenType.SIGN_R_PARENTHESIS)
            MOVE_NEXT()
            func_body = parse_block()

            return NEW_NODE(
                astnode.DefFuncNode(type, var_name, len(para_list), para_list, func_body))
        else:
            # variable
            is_inited, init_expr = parse_init_expr()
            MATCH_TOK(TokenType.SIGN_SEMICOLON)
            MOVE_NEXT()

            return NEW_NODE(
                astnode.DefVarNode(type, var_name, 0, is_glb, 0, is_inited, init_expr, 0))
    else:
        global tok_inx
        err_str = "Mismatch token: %s" % (tu.toks[tok_inx].info(True))
        if tu.FLAG_CHECK == tu.FlagCheck.AST:
            dump_checksum(chksum_file, err_str)
        logger.error(err_str)
        sys.exit()


def parse_stmtlist(stmt_list):
    if CUR_TOK_TYPE() == TokenType.SIGN_R_BRACE:
        MOVE_NEXT()
        return stmt_list

    new_stmt = -1
    if CUR_TOK_TYPE() == TokenType.KW_INT:
        MOVE_NEXT()
        new_stmt = parse_def(TokenType.KW_INT, 0)  # is_glb: 0
    elif CUR_TOK_TYPE() == TokenType.KW_BREAK:
        MOVE_NEXT()
        MATCH_TOK(TokenType.SIGN_SEMICOLON)
        MOVE_NEXT()
        new_stmt = NEW_NODE(astnode.StmtBrkNode())
    elif CUR_TOK_TYPE() == TokenType.KW_CONTINUE:
        MOVE_NEXT()
        MATCH_TOK(TokenType.SIGN_SEMICOLON)
        MOVE_NEXT()
        new_stmt = NEW_NODE(astnode.StmtContNode())
    elif CUR_TOK_TYPE() == TokenType.KW_RETURN:
        MOVE_NEXT()
        ret_expr = parse_expr()
        MATCH_TOK(TokenType.SIGN_SEMICOLON)
        MOVE_NEXT()
        new_stmt = NEW_NODE(astnode.StmtRetNode(ret_expr))
    elif CUR_TOK_TYPE() == TokenType.KW_IF:
        MOVE_NEXT()
        MATCH_TOK(TokenType.SIGN_L_PARENTHESIS)
        MOVE_NEXT()
        cond_expr = parse_expr()
        MATCH_TOK(TokenType.SIGN_R_PARENTHESIS)
        MOVE_NEXT()
        then_body = parse_block()

        has_else = 0
        else_body = -1
        if CUR_TOK_TYPE() == TokenType.KW_ELSE:
            MOVE_NEXT()
            has_else = 1
            else_body = parse_block()

        new_stmt = NEW_NODE(
            astnode.StmtIfNode(cond_expr, then_body, has_else, else_body))
    elif CUR_TOK_TYPE() == TokenType.KW_FOR:
        MOVE_NEXT()
        MATCH_TOK(TokenType.SIGN_L_PARENTHESIS)
        MOVE_NEXT()
        init_expr = parse_expr()
        MATCH_TOK(TokenType.SIGN_SEMICOLON)
        MOVE_NEXT()
        bound_expr = parse_expr()
        MATCH_TOK(TokenType.SIGN_SEMICOLON)
        MOVE_NEXT()
        update_expr = parse_expr()
        MATCH_TOK(TokenType.SIGN_R_PARENTHESIS)
        MOVE_NEXT()
        for_body = parse_block()
        new_stmt = NEW_NODE(
            astnode.StmtForNode(init_expr, bound_expr, update_expr, for_body))
    elif CUR_TOK_TYPE() == TokenType.KW_WHILE:
        MOVE_NEXT()
        MATCH_TOK(TokenType.SIGN_L_PARENTHESIS)
        MOVE_NEXT()
        cond_expr = parse_expr()
        MATCH_TOK(TokenType.SIGN_R_PARENTHESIS)
        MOVE_NEXT()
        while_body = parse_block()
        new_stmt = NEW_NODE(astnode.StmtWhileNode(cond_expr, while_body))
    elif CUR_TOK_TYPE() == TokenType.SIGN_SEMICOLON:
        MOVE_NEXT()
        new_stmt = NEW_NODE(astnode.StmtEmptyNode())
    else:
        stmt_expr = parse_expr()
        MATCH_TOK(TokenType.SIGN_SEMICOLON)
        MOVE_NEXT()
        new_stmt = NEW_NODE(astnode.StmtExprNode(stmt_expr))

    stmt_list.append(new_stmt)
    return parse_stmtlist(stmt_list)


def parse_block():
    MATCH_TOK(TokenType.SIGN_L_BRACE)
    MOVE_NEXT()
    stmt_list = list()
    stmt_list = parse_stmtlist(stmt_list)
    return NEW_NODE(astnode.BlockNode(len(stmt_list), stmt_list))


# node: global variable | function
def parse_program(def_list):
    # check whether there is available token
    global tok_inx
    if tok_inx == len(tu.toks):
        return def_list

    MATCH_TOK(TokenType.KW_INT)
    MOVE_NEXT()
    node = parse_def(TokenType.KW_INT, 1)  # is_glb: 1
    def_list.append(node)
    return parse_program(def_list)


# tu.ast: [node, node, node, ..., PROG]
def do_parse():
    def_list = list()
    def_list = parse_program(def_list)
    # PROG is always the last node in tu.ast
    return NEW_NODE(astnode.ProgNode(len(def_list), def_list))


################################
# dump AST

def dump_ast():
    ast_str = ""
    logger.debug("%d astnode:" % len(tu.ast))
    inx = 0
    for node in tu.ast:
        inx_str = "%d-th node: " % (inx)
        node_info = node.info()

        logger.debug(inx_str + node_info)
        ast_str += inx_str + node_info + '\t'
        inx = inx + 1
    return ast_str


################################
# main entry

def parse():
    # check whether lexer succeeds
    if len(tu.toks) == 0:
        logger.error("No available tokens.")
        sys.exit()

    logger.debug(SUBPHASE_TAG_STR)
    logger.debug('Start to parse')
    do_parse()
    logger.debug('Parsing succeeds')

    # dump the ast
    logger.debug(SUBPHASE_TAG_STR)
    logger.debug('Dump the AST')
    ast_str = dump_ast()

    # generate the checksum of ast and dump it
    if tu.FLAG_CHECK == tu.FlagCheck.AST:
        import hashlib
        ast_checksum = hashlib.md5(ast_str.encode('utf-8')).hexdigest()
        logger.debug("ast checksum:%s" % ast_checksum)
        dump_checksum(chksum_file, ast_checksum)

    # finish
    logger.info("Done")
