import re

# This is the preprocessor.
# What this does is removes comments, converts char constants to integers,
# expands macros, removes \n characters, and converts all if statements to while statements


class PreProcessor:
    def __init__(self, inDir, macro_depth=16):
        self.folder = inDir
        self.mainfile = ''
        self.macro_depth = 16  # How many times it expands macros that include other macros

    def remove_comments(self, inCode):
        scan = True
        outCode = ''

        # Removes all characters between '\' characters
        for c in inCode:
            if c == '\\':
                scan = not scan
            elif scan:
                outCode += c
        return outCode

    def simplify(self, inCode):
        code = inCode.replace(
            '\t', ' ')  # Replace tabs with 1 space and remove new line
        code = code.replace('\n', '').replace('if', 'while').replace(
            '->', ',')  # if to while and -> to ,
        code = code.replace('{', ';').replace(
            '}', 'end;')  # { to ; and } to end;
        # Remove double spaces with regular expression
        code = re.sub(' +', ' ', code)
        code = code.replace('while(', 'while ')
        outCode = ''
        scan = True
        outChar = ''
        for c in code:
            if c == "'":
                scan = not scan
                if scan == True:
                    # Converts char constants to integers ('A' -> 65, '0' -> 48, etc.)
                    outCode += str(ord(outChar[0]))
                    outChar = ''
            elif scan:
                outCode += c
            else:
                outChar += c
        return outCode

    def expand_macros(self, inCode):
        macros = {

        }
        outCode = ''
        scan = True
        macro = ''
        for c in inCode:

            # All directives start with '@' and end with '\n'
            # because of this, even directives at the bottom of a file must have another line under them
            if c == '@':
                scan = False
            elif c == '\n':
                scan = True
                if len(macro.split(' ')) != 0:
                    macroArgs = macro.split(' ')
                    if macroArgs[0] == 'define':
                        # @define MACRO value
                        macros[macroArgs[1]] = macroArgs[2]
                    elif macroArgs[0] == 'incmacro':
                        # @incmacro file (without .bfmacro, it automacically uses .bfmacro)
                        with open(self.folder + '/' + macroArgs[1] + '.bfmacro') as fp:
                            macros[macroArgs[1]] = fp.read()
                    elif macroArgs[0] == 'prints':
                        # @prints var Some more text
                        # Creates a long chain of:
                        # copy 'H' -> var; putc var; inc var, ...; putc var; ...
                        useVar = macroArgs[1]
                        inString = ' '.join(macroArgs[2:])
                        outMacro = 'copy ' + \
                            str(ord(inString[0])) + ' -> ' + useVar + \
                            ';\nputc ' + useVar + ';\n'
                        prevChar = ord(inString[0])
                        for i in range(1, len(inString)):
                            c = ord(inString[i])
                            if c == prevChar:
                                outMacro += 'putc ' + useVar + ';\n'
                            elif c > prevChar:
                                outMacro += 'inc ' + useVar + \
                                    ', ' + str(c - prevChar) + \
                                    ';\nputc ' + useVar + ';\n'
                            else:
                                outMacro += 'dec ' + useVar + \
                                    ', ' + str(prevChar - c) + \
                                    ';\nputc ' + useVar + ';\n'
                            prevChar = c
                        outCode += outMacro
                macro = ''
            elif scan:
                outCode += c
            else:
                macro += c
        for m in macros:
            # This is what expands macros
            # Anything between two ':' chars is seen as a macro

            # @define THING 10
            # copy THING -> a;
            # -- Turns into --
            # copy 10 -> a;
            outCode = outCode.replace(':' + m + ':', macros[m])
        # Also removes comments from expanded macros
        return self.remove_comments(outCode)

    def process(self):
        # Opens main file in folder
        with open(self.folder + '/main.bfl', 'r') as fp:
            self.mainfile = fp.read()

        self.mainfile = self.remove_comments(self.mainfile)  # Remove comments

        for i in range(self.macro_depth):
            self.mainfile = self.expand_macros(self.mainfile)  # Expands macros

        self.mainfile = self.simplify(self.mainfile)  # Simplify code
        # Seperate code into list of instruction strings seperated by ';'
        self.mainlines = self.mainfile.split(';')
        while '' in self.mainlines:
            self.mainlines.remove('')  # Remove all blank instructions
        return self.mainlines
