#### Unit Test Framework

The compilation/analysis result of each phase in `toyc` should be checked (yep, only correctness). Since the outputs for most phases are not a single number, here the checksum of the meaningful outputs produced by each phase is checked. For example, regarding tokenization phase, the meaningful output is a list of tokens, recording the token type, content and locations. A checksum is computed based on these tokens.

Note that the error message is used as the checksum if bad inputs are provided.

##### Usage

```shell
$ python3 test/test.py -h
usage: test.py [-h] [--src SRC_DIR]

Test framework for TOYC

optional arguments:
  -h, --help     show this help message and exit
  --src SRC_DIR  The location of TOYC source code. Default is $PWD
```

