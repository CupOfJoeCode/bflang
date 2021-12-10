from re import L

VALID_BF = "+-<>,.[]"


class Token:
    def __init__(self, token_type, args, original=""):
        self.token_type = token_type
        self.args = args
        self.original = original
        self.original_filtered = original
        for c in VALID_BF:
            self.original_filtered = self.original_filtered.replace(c, '')

    def __str__(self):
        return 'Token(' + self.token_type + ', ' + str(self.args) + ')'


class Lexer:
    def __init__(self, inCode):
        self.code = inCode

    def generate(self):
        outTokens = []
        for l in self.code:
            if l[0] == ' ':
                line = l[1:]
            else:
                line = l
            lineType = line.split(' ')[0]
            lineRest = line.replace(lineType, '').replace(' ', '').split(',')
            if 'end' in lineRest:
                outTokens.append(Token('end', [lineType], line))
            else:
                outTokens.append(Token(lineType, lineRest, line))
        return outTokens
