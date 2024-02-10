a [preprocessor](https://en.wikipedia.org/wiki/Preprocessor) or a precompiler is a program that processes its input data to produce output that is used as input in another program.
- output preprocessed form of the input data, used by compiler.
## Lexical preprocessors
are the lowest-level of preprocessors, they only require lexical analysis.
- operate on the source text, prior to any parsing, by performing simple substitution of tokenized character sequence for other tokenized character sequences, according to user-defined rules.
## Lexical toknization
is conversion of a text into (semantically or syntactically) meaningful lexical tokens belong to categories defined by a 'lexer' program.
- in case of programming language, the categories include identifiers, operators, grouping symbols and data types.
- a rule-based program, performing lexical tokenization, is called tokenizer, or scanner.
- scanner is also a term for the first stage of lexer.
- lexers and parsers used for compilers, but can be used for prettyprinters or linters.
Lexing can be divided in two stages:
1. scanning, segments input string into syntactic units called lexemes and categories into toke classes.
2. evaluating, which converts lexemes into processed values.