import sys
from preprocess import PreProcessor
from lexer import Lexer
from codegen import CodeGenerator

# --------------------------------------------
# Bflang is a custom programming language, which cross-compiles to brainfuck
# Bflang is sort of inspired by assembly, because of its simple instructions
#
# https://github.com/CupOfJoeCode/bflang
# --------------------------------------------

IN_FOLDER = sys.argv[1]


def main():
    pre = PreProcessor(IN_FOLDER)
    processed_code = pre.process()
    lex = Lexer(processed_code)
    tokens = lex.generate()
    cg = CodeGenerator(tokens)
    outText = ''
    for i in cg.tokens:
        outText += str(i) + '\n'
    with open(IN_FOLDER + '/out.bf', 'w') as fp:
        fp.write(cg.generate())


if __name__ == '__main__':
    main()
