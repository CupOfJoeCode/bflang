from re import L


class Token:
    def __init__(self, token_type, args):
        self.token_type = token_type
        self.args = args

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
                outTokens.append(Token('end', [lineType]))
            else:
                outTokens.append(Token(lineType, lineRest))
        return outTokens
