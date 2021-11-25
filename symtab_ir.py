import os
import sys

import tu
from tu import logger
from tu import SUBPHASE_TAG_STR
from tu import dump_checksum
from tok import Token
# from astnode import ASTNode
# import lexer
chksum_file = '/tmp/toyc.symtab.ir'


################################
# global data

# tu.varpool: a list of variable info
#   0. string: name
#   1. vector: scope info
#   2. int: type info. 0 -> int (currently only INT type is supported.)
#   3. bool: is pointer? 0|1
#   4. bool: is array? 0|1
#   5. bool: is inited? 0|1
#   6. int: size
#   7. int: offset
#
# Example:
# [[...],
#  [tmp, [0,2,4], 0, 0, 1, 1, 4, 8], # inx = 1
#  [val, [0,2], 0, 0, 1, 1, 32, 16], # inx = 2
#  [val, [0,3], 0, 0, 1, 1, 8, 64]   # inx = 3
# ]
#
# tu.vartab: map one var name to one vector, which stores a list of var indexes.
# Example: {tmp:[1], val: [2,3]}
#
# tu.funpool: a list of function info
#   0. string: name
#   1. int: return type. 0 -> int
#   2. vector: parameter index list
#   3. int: max depth
#   4. int: current depth
#   5. vector: scope size info
#   6. vector: ir instructions
#
# Example:
# [[...],
#  [fun, 0, [1,3], 96, 3, [0,2,4],[xxx]] # inx = 1
# ]
#
# tu.funtab: map one func name to one func index.
# Example: {fun:1, fib:2}

# function index under analysis
cur_fun_inx = -1
# current scope id(always increasing)
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
