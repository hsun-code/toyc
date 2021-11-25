`toyc` is a toy compiler for C subset, translating C-like source code into the x86_64 assembly (other architectures are not supported).



#### C Subset

Only a subset of C grammar is supported currently.

- only `int` type is supported
- only **1-D array** and **pointer** is supported
- only a number of arithmetic and relational operators are supported
- only decimal integers can be treated as constant values
- global variables and function calls are supported
- **DO NOT** support `do-while`, `switch`, `goto`, `header `, `macros`,  `typedefs`, `struct`,  `qualifiers`, `library functions`, `bitwise operators`, `strings`, etc.

Please refer to the [Lexer](./docs/lexer.md) and [Parser](./docs/parser.md) part for more details of our grammar.



#### Optimizations

After lexer and parser, we can obtain the AST. Then several passes would be conducted upon it.

- CFG and callgraph would be built, therefore unreachable code can be removed
- data flow analysis can be performed
- constant propagation
- common subexpression elimination
- peephole and register selection for backend



#### Usage

`toyc` is implemented in Python3. Given a source code `src.c`, simply run `python3 toyc.py -i src.c` and you would get:

- the corresponding assembly file `src.c.S` and
- the log file `src.c.LOG` where a lot of useful information along every phase (e.g., tokenization, AST generation, the symbol table/CFG/call graph, optimization passes, instruction selection) are recorded.

Note that option `--opt` should be add if you want to enable optimization passes.

Another **assembler** is needed if we want to run our compiled/generated assembly code (firstly turning the assembly into object file). Besides as built-in **library functions** are not supported in our grammar, we may want to use another **test driver** to print out the computation results of our generated code.

Take `test/fib.c` as an example. Function `fib()` computes the Fibonacci number and we need another file to call this function and dump the result.

```shell
python3 toyc.py -i fib.c
gcc -c fib.c.S -o fib.o
gcc -c drive.c -o drive.o
gcc fib.o drive.o -o a.out
./a.out
```



#### Docs

In the following, each phase is demonstrated in details.

[Lexer](./docs/lexer.md), [Parser](./docs/parser.md)

TBA



#### Test

A simple test framework is provided to check the correctness of every stage of `toyc`. See [Test](./docs/test.md)

```shell
python3 test/test.py --src $PATH_TO_TOYC
```

------

Please feel free to raise issues if you have any question. Thanks :)
