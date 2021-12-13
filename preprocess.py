import re


class PreProcessor:
    def __init__(self, inDir, macro_depth=16):
        self.folder = inDir
        self.mainfile = ''
        self.macro_depth = 16

    def remove_comments(self, inCode):
        scan = True
        outCode = ''
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
        code = re.sub(' +', ' ', code)  # Remove double spaces
        code = code.replace('while(', 'while ')
        outCode = ''
        scan = True
        outChar = ''
        for c in code:
            if c == "'":
                scan = not scan
                if scan == True:
                    outCode += str(ord(outChar[0]))
                    outChar = ''
            elif scan:
                outCode += c
            else:
                outChar += c
        return outCode

    # TODO: Add prints
    def expand_macros(self, inCode):
        macros = {

        }
        outCode = ''
        scan = True
        macro = ''
        for c in inCode:
            if c == '@':
                scan = False
            elif c == '\n':
                scan = True
                if len(macro.split(' ')) != 0:
                    macroArgs = macro.split(' ')
                    if macroArgs[0] == 'define':
                        macros[macroArgs[1]] = macroArgs[2]
                    elif macroArgs[0] == 'incmacro':
                        with open(self.folder + '/' + macroArgs[1] + '.bfmacro') as fp:
                            macros[macroArgs[1]] = fp.read()
                macro = ''
            elif scan:
                outCode += c
            else:
                macro += c
        for m in macros:
            outCode = outCode.replace(':' + m + ':', macros[m])
        return self.remove_comments(outCode)

    def process(self):
        with open(self.folder + '/main.bfl', 'r') as fp:
            self.mainfile = fp.read()
        self.mainfile = self.remove_comments(self.mainfile)
        for i in range(self.macro_depth):
            self.mainfile = self.expand_macros(self.mainfile)
        self.mainfile = self.simplify(self.mainfile)
        self.mainlines = self.mainfile.split(';')
        while '' in self.mainlines:
            self.mainlines.remove('')
        return self.mainlines
