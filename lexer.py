import sys

import tu
from tu import logger
from tu import SUBPHASE_TAG_STR
from tu import dump_checksum

import tok
from tok import TokenType
from tok import Token

chksum_file = '/tmp/toyc.lex'


################################
# read each line and generate the tokens

def is_digit_or_letter(ch):
    if ch >= '0' and ch <= '9':
        return True
    if ch >= 'a' and ch <= 'z':
        return True
    if ch >= 'A' and ch <= 'Z':
        return True
    return False


def read_line(line, lineno):
    num = len(line)
    inx = 0
    col_b = 1
    while inx < num:
        cur_char = line[inx]
        if cur_char in tok.whitespace:
            logger.debug("\t%d-th char at col %d: WS" % (inx, col_b))
        else:
            logger.debug("\t%d-th char at col %d: %c" % (inx, col_b, cur_char))

        # single character token
        if cur_char in tok.single_char_tok_map.keys():
            logger.debug("\t\tis single character token.")
            token_type = tok.single_char_tok_map[cur_char]
            token = Token(token_type, None, lineno, lineno, col_b, col_b)
            tu.toks.append(token)
            inx = inx + 1
            col_b = col_b + 1
            continue

        # escape continuous whitespace
        if cur_char in tok.whitespace:
            while cur_char in tok.whitespace:
                logger.debug("\t\tis whitespace.")
                if cur_char == '\t':
                    col_b = col_b + tok.chars_per_tab
                else:
                    col_b = col_b + 1
                inx = inx + 1
                if inx == num:
                    break
                cur_char = line[inx]
            if inx == num:
                break
            continue

        # = and ==
        if cur_char == '=':
            if line[inx + 1] == '=':
                logger.debug("\t\tis ==")
                token = Token(TokenType.OP_EQ, None, lineno,
                              lineno, col_b, col_b + 1)
                tu.toks.append(token)
                inx = inx + 2
                col_b = col_b + 2
            else:
                logger.debug("\t\tis =")
                token = Token(TokenType.SIGN_ASSIGN, None,
                              lineno, lineno, col_b, col_b)
                tu.toks.append(token)
                inx = inx + 1
                col_b = col_b + 1
            continue

        # !=
        if cur_char == '!':
            if line[inx + 1] == '=':
                logger.debug("\t\tis !=")
                token = Token(TokenType.OP_NOT_EQ, None,
                              lineno, lineno, col_b, col_b + 1)
                tu.toks.append(token)
                inx = inx + 2
                col_b = col_b + 2
                continue
            else:
                err_str = "tokenization failed at line:%d, column:%d. '!=' is expected." % (
                    lineno, col_b + 1)
                if tu.FLAG_CHECK == tu.FlagCheck.LEX:
                    dump_checksum(chksum_file, err_str)
                logger.error(err_str)
                sys.exit()

        # keywrod/identifier/constant
        if is_digit_or_letter(cur_char):
            prev_inx = inx
            while is_digit_or_letter(cur_char):
                inx = inx + 1
                if inx == num:
                    break
                cur_char = line[inx]
            tok_str = line[prev_inx: inx]
            prev_col_b = col_b
            col_b = col_b + inx - prev_inx
            logger.debug("\t\tis string:%s" % tok_str)

            if tok_str in tok.keyword_tok_map.keys():
                token_type = tok.keyword_tok_map[tok_str]
                token = Token(token_type, None, lineno,
                              lineno, prev_col_b, col_b - 1)
            elif tok_str.isdigit():
                # TODO: lexer errors should be raised for '0123'
                token = Token(TokenType.CONST_VAL, int(tok_str), lineno,
                              lineno, prev_col_b, col_b - 1)
            else:
                token = Token(TokenType.VAR, tok_str, lineno,
                              lineno, prev_col_b, col_b - 1)
            tu.toks.append(token)
            continue

        # unrecoginized token
        err_str = "unrecognized token at line:%d, column:%d" % (lineno, col_b)
        if tu.FLAG_CHECK == tu.FlagCheck.LEX:
            dump_checksum(chksum_file, err_str)
        logger.error(err_str)
        sys.exit()


################################
# dump tokens

def dump_tokens():
    tokens_str = ""
    logger.debug("%d tokens:" % len(tu.toks))
    inx = 0
    for tok in tu.toks:
        assert isinstance(tok, Token), "tok must be Token!"
        inx_str = "%d-th token: " % (inx)
        tok_info = tok.info(True)

        logger.debug(inx_str + tok_info)
        tokens_str += inx_str + tok_info + '\t'
        inx = inx + 1
    return tokens_str


################################
# main entry

def lex():
    logger.debug(SUBPHASE_TAG_STR)
    logger.debug('Start to tokenize')
    with open(tu.src_file_name, 'r') as src_file:
        lines = src_file.readlines()
        lineno = 1
        for line in lines:
            logger.debug("analyzing line: %d" % lineno)
            read_line(line, lineno)
            lineno = lineno + 1
        src_file.close()

    # dump all the tokens
    logger.debug(SUBPHASE_TAG_STR)
    logger.debug('Get all the tokens')
    tokens_str = dump_tokens()

    # generate the checksum and dump it
    if tu.FLAG_CHECK == tu.FlagCheck.LEX:
        import hashlib
        tokens_checksum = hashlib.md5(tokens_str.encode('utf-8')).hexdigest()
        logger.debug("token checksum:%s" % tokens_checksum)
        dump_checksum(chksum_file, tokens_checksum)

    # finish
    logger.info('Done')
