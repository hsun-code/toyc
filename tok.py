from enum import Enum


class TokenType(Enum):
    VAR = 1                         # identifier -> variables, parameters, functions
    KW_INT = 2                      # int type
    KW_IF = 3
    KW_ELSE = 4
    KW_WHILE = 5
    KW_FOR = 6
    KW_BREAK = 7
    KW_RETURN = 8
    KW_CONTINUE = 9
    OP_ADD = 10                     # arith operator: +, -, *, /
    OP_SUB = 11
    OP_MUL = 12                     # also used to indicate pointers
    OP_DIV = 13
    OP_GT = 14                      # relation operator: >, <, ==, !=
    OP_LT = 15
    OP_EQ = 16
    OP_NOT_EQ = 17
    OP_ADDR = 18                    # &
    CONST_VAL = 19                  # constant integers
    SIGN_SEMICOLON = 20             # ; and ,
    SIGN_COMA = 21
    SIGN_L_BRACE = 22               # { and }
    SIGN_R_BRACE = 23
    SIGN_L_BRACKET = 24             # [ and ]
    SIGN_R_BRACKET = 25
    SIGN_L_PARENTHESIS = 26         # ( and )
    SIGN_R_PARENTHESIS = 27
    SIGN_ASSIGN = 28                # assignment


class Token(object):
    def __init__(self, type, value, row_b, row_e, col_b, col_e):
        assert isinstance(type, TokenType), "type must be TokenType!"
        self.type = type            # class TokenType
        self.value = value          # string for VAR and integer for CONST_VAL
        self.row_b = row_b          # location info
        self.row_e = row_e
        self.col_b = col_b
        self.col_e = col_e

    def info(self, is_raw=False):
        tok_info = ''
        if is_raw:
            if self.type == TokenType.VAR:
                tok_info = "%s, %s, (%d,%d,%d,%d)" % (
                    self.type.name, self.value, self.row_b, self.row_e, self.col_b, self.col_e)
            elif self.type == TokenType.CONST_VAL:
                tok_info = "%s, %d, (%d,%d,%d,%d)" % (
                    self.type.name, self.value, self.row_b, self.row_e, self.col_b, self.col_e)
            else:
                tok_info = "%s, (%d,%d,%d,%d)" % (
                    self.type.name, self.row_b, self.row_e, self.col_b, self.col_e)
        else:
            if self.type == TokenType.VAR:
                tok_info = "%s, %s" % (self.type.name, self.value)
            elif self.type == TokenType.CONST_VAL:
                tok_info = "%s, %d" % (self.type.name, self.value)
            else:
                tok_info = "%s" % (self.type.name)

        return tok_info


single_char_tok_map = {
    '{': TokenType.SIGN_L_BRACE,
    '}': TokenType.SIGN_R_BRACE,
    '(': TokenType.SIGN_L_PARENTHESIS,
    ')': TokenType.SIGN_R_PARENTHESIS,
    '[': TokenType.SIGN_L_BRACKET,
    ']': TokenType.SIGN_R_BRACKET,
    ';': TokenType.SIGN_SEMICOLON,
    ',': TokenType.SIGN_COMA,
    '>': TokenType.OP_GT,
    '<': TokenType.OP_LT,
    '+': TokenType.OP_ADD,
    '-': TokenType.OP_SUB,
    '*': TokenType.OP_MUL,
    '/': TokenType.OP_DIV,
    '&': TokenType.OP_ADDR
}

keyword_tok_map = {
    'if': TokenType.KW_IF,
    'else': TokenType.KW_ELSE,
    'for': TokenType.KW_FOR,
    'while': TokenType.KW_WHILE,
    'return': TokenType.KW_RETURN,
    'int': TokenType.KW_INT,
    'continue': TokenType.KW_CONTINUE,
    'break': TokenType.KW_BREAK
}

whitespace = [' ', '\t', '\b', '\n']
chars_per_tab = 4
