import argparse
import os
import sys

import tu
from tu import logger
from tu import PHASE_TAG_STR
import lexer
import parser
import symtab_ir
import opt
import backend


def main():
    '''
    Command Option:
        python toyc.py [--opt] -i src.c [--chk PHASE]
        Input: src.c
        Output: assembly->src.c.S, logfile->src.c.LOG
    '''
    arg_parser = argparse.ArgumentParser(
        description="Toy Compiler for C Subset")
    arg_parser.add_argument('-i', required=True,
                            dest='src_file', help='Input source code')
    arg_parser.add_argument('--opt', default=False, action='store_true',
                            dest='opt_flag', help='Use optimization passes')
    arg_parser.add_argument('--chk', dest='check_flag', type=int, default=0,
                            choices=[1, 2, 3, 4, 5, 6, 7],
                            help="Unit test usage: generate the checksum of each phase's result. \
                                PHASE can be 1: token, 2: ast, 3: symtab_ir, 4: cfg, 5: call graph, \
                                6: passes, 7: codegen")

    # get options
    args = arg_parser.parse_args()

    # check whether source file is available
    try:
        src_file = open(args.src_file)
    except FileNotFoundError:
        print("ERROR: File %s is not found." % args.src_file)
        sys.exit()
    except PermissionError:
        print("ERROR: You don't have permission to access the file %s." %
              args.src_file)
        sys.exit()
    finally:
        src_file.close()

    # init tu
    tu.src_file_name = args.src_file
    opt_flag = args.opt_flag
    tu.as_file_name = tu.src_file_name + '.S'
    tu.log_file_name = tu.src_file_name + '.LOG'
    tu.init_logger()
    if args.check_flag != 0:
        tu.init_check_flag(args.check_flag)

    # dump the configuration details
    logger.info(PHASE_TAG_STR)
    logger.info("Configuration:")
    logger.info("\t Source code: %s" % tu.src_file_name)
    logger.info("\t Use optimization: %s" % opt_flag)
    logger.info("\t Generated assembly code: %s" % tu.as_file_name)
    logger.info("\t Log file: %s" % tu.log_file_name)
    logger.info("\t Check flag: %d"%args.check_flag)

    # lexer
    logger.info(PHASE_TAG_STR)
    logger.info("Lex phase")
    lexer.lex()

    # parser
    logger.info(PHASE_TAG_STR)
    logger.info("Parse phase")
    parser.parse()

    # symtab_ir
    logger.info(PHASE_TAG_STR)
    logger.info("symtab+ir phase")
    symtab_ir.gen()

    # optimization
    if(opt_flag):
        logger.info(PHASE_TAG_STR)
        logger.info("Optimization phase")
        opt.optimize()

    # code generation
    logger.info(PHASE_TAG_STR)
    logger.info("Codegen phase")
    backend.codegen()

    # finish
    logger.info(PHASE_TAG_STR)
    logger.info("Finish")


if __name__ == '__main__':
    main()
