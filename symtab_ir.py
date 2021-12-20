import sys

import tu
from tu import logger
from tu import SUBPHASE_TAG_STR
from tu import dump_checksum

# from astnode import ASTNode
# import lexer
chksum_file = '/tmp/toyc.symtab.ir'


################################
# DESC on tu.var_pool, tu.var_tab, tu.fun_pool, tu.fun_tab
#
# tu.var_pool: a list of variable info
#   Each element is one Var instance.
#
# tu.var_tab: a dict of mapping from string to one list.
#   string: the variable name
#   list: each element is the index of variable in var_pool.
#   Example: {tmp: [1], val: [2,3]}
#
# tu.fun_pool: a list of function info
#   Each element is one Fun instance.
#
# tu.fun_tab: a dict of mapping from string to an integer
#   string: the function name
#   integer: the index of this function in fun_pool
#   Example: {foo: 1, bar: 2}


################################
# global data

# current function under analysis
cur_fun_inx = -1
# current scope id (always increasing)
scope_id = -1
# current scope path
scope_path = list()

# IR
tmp_inx = -1


################################
# helpers to manage symtab

def FUNC_ENTER_SCOPE():
    global cur_fun_inx
    if cur_fun_inx != -1:
        # 5: scope size info
        tu.funpool[cur_fun_inx][5].append(0)


def FUNC_LEAVE_SCOPE():
    global cur_fun_inx
    if cur_fun_inx != -1:
        tu.funpool


def SYM_ENTER():
    global scope_id
    scope_id = scope_id + 1
    global scope_path
    scope_path.append(scope_id)
    FUNC_ENTER_SCOPE()


def SYM_LEAVE():
    global scope_path
    scope_path.pop()
    FUNC_LEAVE_SCOPE()


################################
# walk the ast

def walk_ast():
    print("test here")


################################
# main entry

def gen():
    # check whether parser succeeds
    if len(tu.ast) == 0:
        logger.error("No available ast.")
        sys.exit()

    logger.debug(SUBPHASE_TAG_STR)
    logger.debug('Start to generate symtab and ir')
    walk_ast()
    logger.debug('Generating succeeds')

    # dump the ast
    logger.debug(SUBPHASE_TAG_STR)
    logger.debug('Dump the symtab')
    # ast_str = dump_ast()

    # # generate the checksum of ast and dump it
    # if tu.CHECK_FLAG_SYMTAB_IR:
    #     import hashlib
    #     ast_checksum = hashlib.md5(ast_str.encode('utf-8')).hexdigest()
    #     logger.debug("ast checksum:%s" % ast_checksum)
    #     dump_checksum(chksum_file, ast_checksum)

    # finish
    logger.info("Done")
