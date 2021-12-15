from lexer import Token
# To Add:
#
#  arrayload, arraystore
#

MOD_PROG = '>>>[-]<[>+>>+<<<-]>>>[<<<+>>>-]<<<<<[-]>[<+>>>-[>+>+<<-]>>[<<+>>-]+<[>[-]<[-]]>[<+>-]<[<[-]<[>+>>+<<<-]>>>[<<<+>>>-]<<<<<[-]>>>>[-]]<<<-]>[-]>[-]>[-]>[-]<<<<<'
PRINTINT_PROG = '>>++++++++++<<[->+>-[>+>>]>[+[-<+>]>+>>]<<<<<<]>>[-]>>>++++++++++<[->-[>+>>]>[+[-<+>]>+>>]<<<<<]>[-]>>[>++++++[-<++++++++>]<.<<+>+>[-]]<[<[->-<]++++++[->++++++++<]>.[-]]<<++++++[-<++++++++>]<.[-]<<[-<+>]<[-]'
AND_PROG = '>>>[-]<<<>[>[>+<[-]]<[-]]>>[<<<+>>>-]<[-]<[-]<'
OR_PROG = '>[>>[-]+<<[-]]>[>[-]+<[-]]>[<<<+>>>[-]]<<<'


class CodeGenerator:
    def __init__(self, inTokens):
        self.tokens = self.combine_malloc(inTokens)
        self.memory_map = {}
        self.current_line = ''
        malloc = self.tokens[0]
        var_count = 6
        for var in malloc.args:
            self.memory_map[var] = var_count
            var_count += 6

    def combine_malloc(self, tokens):
        outTokens = []
        outvars = []
        BUILT_IN_VARS = ['ZEROPOINT', 'ENDPOINT']
        for t in tokens:
            if t.token_type == 'malloc':
                for a in t.args:
                    if a not in outvars:
                        outvars.append(a)

        outTokens.append(Token('malloc', outvars + BUILT_IN_VARS))
        for t in tokens:
            if t.token_type != 'malloc':
                outTokens.append(t)
        return outTokens

    def run_at(self, var, code):
        if var not in self.memory_map:
            print("Error In:\n    " + self.current_line)
            print("Variable '" + var + "' is Not Declared\n")
            exit(1)
        return '>'*self.memory_map[var] + code + '<'*self.memory_map[var]

    def get_mod(self, arg0, arg1, arg2):
        outBf = ''
        outBf += self.run_at(arg2, '[-]>[-]>[-]<<')
        outBf += self.run_at(arg0, '[>+<')
        outBf += self.run_at(arg2, '>+<')
        outBf += self.run_at(arg0, '-]>[<+>-]<')

        outBf += self.run_at(arg1, '[>+<')
        outBf += self.run_at(arg2, '>>+<<')
        outBf += self.run_at(arg1, '-]>[<+>-]<')

        outBf += self.run_at(arg2, MOD_PROG)
        return outBf

    def generate(self):
        outBf = ''
        for t in self.tokens:
            try:
                self.current_line = t.original
                if t.token_type == 'copy':
                    if t.args[0].isdigit() or t.args[0][1:].isdigit():
                        num = int(t.args[0])
                        if num < 0:
                            numTimes = 256 + num
                        else:
                            numTimes = num

                        outBf += self.run_at(t.args[1],
                                             '[-]' + ('+'*numTimes))
                    else:
                        outBf += self.run_at(t.args[1], '[-]')
                        outBf += self.run_at(t.args[0],
                                             '[>+>+<<-]>>[<<+>>-]<<')
                        outBf += self.run_at(t.args[0], '>[<')
                        outBf += self.run_at(t.args[1], '+')
                        outBf += self.run_at(t.args[0], '>-]<')
                elif t.token_type == 'add':
                    outBf += self.run_at(t.args[2], '[-]')
                    outBf += self.run_at(t.args[0], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[0], '>[<')
                    outBf += self.run_at(t.args[2], '+')
                    outBf += self.run_at(t.args[0], '>-]<')
                    outBf += self.run_at(t.args[1], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[1], '>[<')
                    outBf += self.run_at(t.args[2], '+')
                    outBf += self.run_at(t.args[1], '>-]<')
                elif t.token_type == 'sub':
                    outBf += self.run_at(t.args[2], '[-]')
                    outBf += self.run_at(t.args[0], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[0], '>[<')
                    outBf += self.run_at(t.args[2], '+')
                    outBf += self.run_at(t.args[0], '>-]<')
                    outBf += self.run_at(t.args[1], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[1], '>[<')
                    outBf += self.run_at(t.args[2], '-')
                    outBf += self.run_at(t.args[1], '>-]<')
                elif t.token_type == 'putc':
                    outBf += self.run_at(t.args[0], '.')
                elif t.token_type == 'getc':
                    outBf += self.run_at(t.args[0], ',')
                elif t.token_type == 'while':
                    outBf += self.run_at(t.args[0].replace('(',
                                                           '').replace(')', ''), '[')
                elif t.token_type == 'end':
                    if len(t.args) != 0:
                        if t.args[0] != '':
                            if t.args[0] == '()':
                                outBf += self.run_at('ZEROPOINT'.replace('(',
                                                                         '').replace(')', ''), ']')
                            else:
                                outBf += self.run_at(t.args[0].replace('(',
                                                                       '').replace(')', ''), ']')
                elif t.token_type == 'not':
                    outBf += self.run_at(t.args[1], '[-]+')
                    outBf += self.run_at(t.args[0], '[')
                    outBf += self.run_at(t.args[1], '[-]')
                    outBf += self.run_at(t.args[0], '[-]]')
                elif t.token_type == 'equal':
                    outBf += self.run_at(t.args[2], '[-]')
                    outBf += self.run_at(t.args[0], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[0], '>[<')
                    outBf += self.run_at(t.args[2], '+')
                    outBf += self.run_at(t.args[0], '>-]<')
                    outBf += self.run_at(t.args[1], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[1], '>[<')
                    outBf += self.run_at(t.args[2], '-')
                    outBf += self.run_at(t.args[1], '>-]<')
                    outBf += self.run_at(t.args[2], '>+<[>[-]<[-]]>[<+>-]<')
                elif t.token_type == 'nequal':
                    outBf += self.run_at(t.args[2], '[-]')
                    outBf += self.run_at(t.args[0], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[0], '>[<')
                    outBf += self.run_at(t.args[2], '+')
                    outBf += self.run_at(t.args[0], '>-]<')
                    outBf += self.run_at(t.args[1], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[1], '>[<')
                    outBf += self.run_at(t.args[2], '-')
                    outBf += self.run_at(t.args[1], '>-]<')
                    outBf += self.run_at(t.args[2], '>+<[>[-]<[-]]>[<+>-]<'*2)
                elif t.token_type == 'printint':
                    outBf += self.run_at('ENDPOINT', '[-]')
                    outBf += self.run_at(t.args[0], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[0], '>[<')
                    outBf += self.run_at('ENDPOINT', '+')
                    outBf += self.run_at(t.args[0], '>-]<')
                    outBf += self.run_at("ENDPOINT", PRINTINT_PROG)
                elif t.token_type == 'inc':
                    outBf += self.run_at(t.args[0], '+'*int(t.args[1]))
                elif t.token_type == 'dec':
                    outBf += self.run_at(t.args[0], '-'*int(t.args[1]))
                elif t.token_type == 'mul':
                    outBf += self.run_at(t.args[2], '[-]')
                    outBf += self.run_at(t.args[0], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[0], '>[<')
                    outBf += self.run_at(t.args[1], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[1], '>[<')
                    outBf += self.run_at(t.args[2], '+')
                    outBf += self.run_at(t.args[1], '>-]<')
                    outBf += self.run_at(t.args[0], '>-]<')
                elif t.token_type == 'mod':
                    outBf += self.get_mod(t.args[0], t.args[1], t.args[2])
                elif t.token_type == 'div':
                    outBf += self.get_mod(t.args[0], t.args[1], t.args[2])
                    outBf += self.run_at(t.args[0], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[2], '[')
                    outBf += self.run_at(t.args[0], '>-<')
                    outBf += self.run_at(t.args[2], '-]')
                    outBf += self.run_at(t.args[0], '>[<')
                    outBf += self.run_at(t.args[2], '+')
                    outBf += self.run_at(t.args[1], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[1], '>[<')
                    outBf += self.run_at(t.args[0], '>-<')
                    outBf += self.run_at(t.args[1], '>-]<')
                    outBf += self.run_at(t.args[0], '>]<')
                elif t.token_type == 'less':
                    outBf += self.get_mod(t.args[0], t.args[1], t.args[2])
                    outBf += self.run_at(t.args[0], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[2], '[')
                    outBf += self.run_at(t.args[0], '>-<')
                    outBf += self.run_at(t.args[2], '-]')
                    outBf += self.run_at(t.args[0], '>[<')
                    outBf += self.run_at(t.args[2], '+')
                    outBf += self.run_at(t.args[0], '>-]<')
                    outBf += self.run_at(t.args[2], '>+<[>[-]<[-]]>[<+>-]<')
                elif t.token_type == 'greater':
                    outBf += self.get_mod(t.args[0], t.args[1], t.args[2])
                    outBf += self.run_at(t.args[0], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[2], '[')
                    outBf += self.run_at(t.args[0], '>-<')
                    outBf += self.run_at(t.args[2], '-]')
                    outBf += self.run_at(t.args[0], '>[<')
                    outBf += self.run_at(t.args[2], '+')
                    outBf += self.run_at(t.args[0], '>-]<')
                    outBf += self.run_at(t.args[2], '>+<[>[-]<[-]]>[<+>-]<'*2)
                elif t.token_type == 'and':
                    outBf += self.run_at(t.args[2], '[-]>[-]>[-]<<')
                    outBf += self.run_at(t.args[0], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[1], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[0], '>[<')
                    outBf += self.run_at(t.args[2], '>+<')
                    outBf += self.run_at(t.args[0], '>-]<')
                    outBf += self.run_at(t.args[1], '>[<')
                    outBf += self.run_at(t.args[2], '>>+<<')
                    outBf += self.run_at(t.args[1], '>-]<')
                    outBf += self.run_at(t.args[2], AND_PROG)
                elif t.token_type == 'or':
                    outBf += self.run_at(t.args[2], '[-]>[-]>[-]<<')
                    outBf += self.run_at(t.args[0], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[1], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[0], '>[<')
                    outBf += self.run_at(t.args[2], '>+<')
                    outBf += self.run_at(t.args[0], '>-]<')
                    outBf += self.run_at(t.args[1], '>[<')
                    outBf += self.run_at(t.args[2], '>>+<<')
                    outBf += self.run_at(t.args[1], '>-]<')
                    outBf += self.run_at(t.args[2], OR_PROG)

                elif t.token_type not in ['malloc', 'main', '']:
                    print("Error In:\n    " + t.original)
                    print("Undefined Token: '" + t.token_type + "'")
                    exit(1)
            except:
                print("Error In:\n    " + t.original)
                print("Compiler Error")
                exit(1)
        return outBf
