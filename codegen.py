from lexer import Token
# To Add:
#
#  arrayload, arraystore
#

MOD_PROG = '>++++++++++++><[->->+>>+<<<[>-]>[->>[-<<<+>>>]<]<<<]>[-]>>>[<<<<<+>>>>>-]<<<<<'
PRINTINT_PROG = '>>++++++++++<<[->+>-[>+>>]>[+[-<+>]>+>>]<<<<<<]>>[-]>>>++++++++++<[->-[>+>>]>[+[-<+>]>+>>]<<<<<]>[-]>>[>++++++[-<++++++++>]<.<<+>+>[-]]<[<[->-<]++++++[->++++++++<]>.[-]]<<++++++[-<++++++++>]<.[-]<<[-<+>]<[-]'
AND_PROG = '>>>[-]<<<>[>[>+<[-]]<[-]]>>[<<<+>>>-]<[-]<[-]<'
OR_PROG = '>[>>[-]+<<[-]]>[>[-]+<[-]]>[<<<+>>>[-]]<<<'


# I'll try my best to document this

class CodeGenerator:
    def __init__(self, inTokens, spacing=7, bits=8):
        self.bits = bits
        # This should combine all seperate 'malloc' statements into a single one
        self.tokens = self.combine_malloc(inTokens)

        self.memory_map = {}  # This dict stores the pointer location for each variable
        self.current_line = ''
        malloc = self.tokens[0]
        var_count = spacing

        # Assign each variable with a pointer location
        for var in malloc.args:
            self.memory_map[var] = var_count
            var_count += spacing

    def combine_malloc(self, tokens):
        outTokens = []
        outvars = []
        # Adds 2 extra variables to the end. 'ZEROPOINT' is unused, and is for when you need a zero value,
        # and 'ENDPOINT' is used for more complex instructions like 'printint'
        BUILT_IN_VARS = ['ZEROPOINT', 'ENDPOINT']
        for t in tokens:
            if t.token_type == 'malloc':
                for a in t.args:
                    if a not in outvars:
                        # Combine all variables into one 'malloc' statement
                        outvars.append(a)
        # Add one 'malloc' statement to the top
        outTokens.append(Token('malloc', outvars + BUILT_IN_VARS))
        for t in tokens:
            # Removes all previous 'malloc' statements
            if t.token_type != 'malloc':
                outTokens.append(t)
        return outTokens

    def run_at(self, var, code):
        # Returns brainfuck code which points to [var], runs [code], points back from [var]

        if var not in self.memory_map:  # If variable is not defined
            print("Error In:\n    " + self.current_line)
            print("Variable '" + var + "' is Not Declared\n")
            exit(1)
        return '>'*self.memory_map[var] + code + '<'*self.memory_map[var]

    def get_mod(self, arg0, arg1, arg2):
        # A seperate function to do a modulo operation, because it is used a few times

        # What modulo does is copy [arg0] and [arg1] to the cells after [arg2]
        # Creates a memory layout of [...,arg2, arg0, arg1, 0, 0, 0,... ]
        # Then it runs the special modulo code at [arg2]

        outBf = ''

        # Copy [arg0] and [arg1] to [arg2]
        outBf += self.run_at(arg2, '[-]>[-]>[-]<<')
        outBf += self.run_at(arg0, '[>+<')
        outBf += self.run_at(arg2, '>+<')
        outBf += self.run_at(arg0, '-]>[<+>-]<')

        outBf += self.run_at(arg1, '[>+<')
        outBf += self.run_at(arg2, '>>+<<')
        outBf += self.run_at(arg1, '-]>[<+>-]<')

        # Modulo
        outBf += self.run_at(arg2, MOD_PROG)
        return outBf

    def generate(self):
        outBf = ''
        for t in self.tokens:
            try:
                self.current_line = t.original  # Copies the original tokens for errors later on
                if t.token_type == 'copy':
                    # Is the first arg a valid number (including negative)
                    if t.args[0].isdigit() or t.args[0][1:].isdigit():
                        num = int(t.args[0])
                        if num < 0:
                            # Converts negative to positive number
                            numTimes = (1 << self.bits) + num
                        else:
                            numTimes = num

                        outBf += self.run_at(t.args[1],
                                             '[-]' + ('+'*numTimes))
                    else:
                        # Copy first variable to second variable
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
                    # This chain of 'ifs' just makes sure it doesnt parse an empty '}' when used for 'main {}'
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

                    # Equal is essentially !(a-b)
                    outBf += self.run_at(t.args[2], '[-]')
                    outBf += self.run_at(t.args[0], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[0], '>[<')
                    outBf += self.run_at(t.args[2], '+')
                    outBf += self.run_at(t.args[0], '>-]<')
                    outBf += self.run_at(t.args[1], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[1], '>[<')
                    outBf += self.run_at(t.args[2], '-')
                    outBf += self.run_at(t.args[1], '>-]<')

                    # Not operation
                    outBf += self.run_at(t.args[2], '>+<[>[-]<[-]]>[<+>-]<')
                elif t.token_type == 'nequal':

                    # Nequal is !!(a-b)
                    outBf += self.run_at(t.args[2], '[-]')
                    outBf += self.run_at(t.args[0], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[0], '>[<')
                    outBf += self.run_at(t.args[2], '+')
                    outBf += self.run_at(t.args[0], '>-]<')
                    outBf += self.run_at(t.args[1], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[1], '>[<')
                    outBf += self.run_at(t.args[2], '-')
                    outBf += self.run_at(t.args[1], '>-]<')

                    # Not but twice
                    outBf += self.run_at(t.args[2], '>+<[>[-]<[-]]>[<+>-]<'*2)
                elif t.token_type == 'printint':
                    # Copyies variable to ENDPOINT and runs PRINTINT_PROG at ENDPOINT
                    outBf += self.run_at('ENDPOINT', '[-]')
                    outBf += self.run_at(t.args[0], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[0], '>[<')
                    outBf += self.run_at('ENDPOINT', '+')
                    outBf += self.run_at(t.args[0], '>-]<')
                    outBf += self.run_at('ENDPOINT', PRINTINT_PROG)
                elif t.token_type == 'inc':
                    outBf += self.run_at(t.args[0], '+'*int(t.args[1]))
                elif t.token_type == 'dec':
                    outBf += self.run_at(t.args[0], '-'*int(t.args[1]))
                elif t.token_type == 'mul':
                    # Multiplication is just repeated addition
                    outBf += self.run_at(t.args[2], '[-]')
                    outBf += self.run_at(t.args[0], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[0], '>[<')
                    outBf += self.run_at(t.args[1], '[>+>+<<-]>>[<<+>>-]<<')
                    outBf += self.run_at(t.args[1], '>[<')
                    outBf += self.run_at(t.args[2], '+')
                    outBf += self.run_at(t.args[1], '>-]<')
                    outBf += self.run_at(t.args[0], '>-]<')
                elif t.token_type == 'mod':
                    # Modulo just uses get_mod
                    outBf += self.get_mod(t.args[0], t.args[1], t.args[2])
                elif t.token_type == 'div':
                    # Division is repeated subtraction but first, subtracts the remainder from the first value
                    # (a - (a % b)) / b
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
                    # Less can be thought of as
                    # If a < b, then a - (a % b) == 0
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
                    # Greater is actually >= instead of >
                    # If a >= b, then a - (a % b) != 0
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
                    # Logical AND
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
                    # Logical OR
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
                    # Undefined instruction/token
                    print("Error In:\n    " + t.original)
                    print("Undefined Token: '" + t.token_type + "'")
                    exit(1)
            except:
                # Other unknown error
                print("Error In:\n    " + t.original)
                print("Compiler Error")
                exit(1)
        return outBf
