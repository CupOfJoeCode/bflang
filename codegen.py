from lexer import Token
# To Add:
#
#  and, or, mul, mod, div, greater, less
#


class CodeGenerator:
    def __init__(self, inTokens):
        self.tokens = self.combine_malloc(inTokens)
        self.memory_map = {}
        malloc = self.tokens[0]
        var_count = 4
        for var in malloc.args:
            self.memory_map[var] = var_count
            var_count += 4

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
        return '>'*self.memory_map[var] + code + '<'*self.memory_map[var]

    def generate(self):
        outBf = ''
        for t in self.tokens:
            # outBf += '\n' + t.token_type + '\n'
            if t.token_type == 'copy':
                if t.args[0].isdigit():
                    outBf += self.run_at(t.args[1],
                                         '[-]' + ('+'*int(t.args[0])))
                else:
                    outBf += self.run_at(t.args[1], '[-]')
                    outBf += self.run_at(t.args[0], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[0], '>[<')
                    outBf += self.run_at(t.args[1], '+')
                    outBf += self.run_at(t.args[0], '>-]<')
            if t.token_type == 'add':
                outBf += self.run_at(t.args[2], '[-]')
                outBf += self.run_at(t.args[0], '[>+>+<<-]>>[<<+>>-]<<')
                outBf += self.run_at(t.args[0], '>[<')
                outBf += self.run_at(t.args[2], '+')
                outBf += self.run_at(t.args[0], '>-]<')
                outBf += self.run_at(t.args[1], '[>+>+<<-]>>[<<+>>-]<<')
                outBf += self.run_at(t.args[1], '>[<')
                outBf += self.run_at(t.args[2], '+')
                outBf += self.run_at(t.args[1], '>-]<')
            if t.token_type == 'sub':
                outBf += self.run_at(t.args[2], '[-]')
                outBf += self.run_at(t.args[0], '[>+>+<<-]>>[<<+>>-]<<')
                outBf += self.run_at(t.args[0], '>[<')
                outBf += self.run_at(t.args[2], '+')
                outBf += self.run_at(t.args[0], '>-]<')
                outBf += self.run_at(t.args[1], '[>+>+<<-]>>[<<+>>-]<<')
                outBf += self.run_at(t.args[1], '>[<')
                outBf += self.run_at(t.args[2], '-')
                outBf += self.run_at(t.args[1], '>-]<')
            if t.token_type == 'putc':
                outBf += self.run_at(t.args[0], '.')
            if t.token_type == 'getc':
                outBf += self.run_at(t.args[0], ',')
            if t.token_type == 'while':
                outBf += self.run_at(t.args[0].replace('(',
                                     '').replace(')', ''), '[')
            if t.token_type == 'end':
                if len(t.args) != 0:
                    if t.args[0] != '':
                        if t.args[0] == '()':
                            outBf += self.run_at('ZEROPOINT'.replace('(',
                                                                     '').replace(')', ''), ']')
                        else:
                            outBf += self.run_at(t.args[0].replace('(',
                                                                   '').replace(')', ''), ']')
            if t.token_type == 'not':
                outBf += self.run_at(t.args[1], '[-]+')
                outBf += self.run_at(t.args[0], '[')
                outBf += self.run_at(t.args[1], '[-]')
                outBf += self.run_at('ZEROPOINT', ']')
            if t.token_type == 'equal':
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
            if t.token_type == 'nequal':
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

        return outBf
