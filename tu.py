import logging
from logging import handlers
from enum import Enum


# global metadata
src_file_name = ''
as_file_name = ''
log_file_name = ''
toks = list()
ast = list()
varpool = list()
vartab = dict()
funpool = list()
funtab = dict()
logger = logging.getLogger("toyc")

PHASE_TAG_STR = "====================================="
SUBPHASE_TAG_STR = "-------------------------------------"


# unit test flag
class FlagCheck(Enum):
    INVALID = 0
    LEX = 1
    AST = 2
    CFG = 3
    SYMTAB_IR = 4
    CALL_GRAPH = 5
    PASS = 6
    CODEGEN = 7


FLAG_CHECK = FlagCheck.INVALID


def init_logger():
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s |  %(levelname)s: %(message)s')
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logFilePath = log_file_name
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=logFilePath, when='midnight', backupCount=30)
    formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def init_check_flag(check_flag):
    global FLAG_CHECK
    FLAG_CHECK = FlagCheck(check_flag)


def dump_checksum(file, checksum_str):
    with open(file, 'w') as file:
        file.write(checksum_str)
        file.close()
