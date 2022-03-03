import re


# ############################################################## Analizator scris in python pentru identificarea elementelor din C

class LexicalAnalyzer:
    lin_num = 1

    def tokenize(self, code):
        rules = [
            ('MAIN', r'main'),          # main
            ('INT', r'int'),            # int
            ('VOID', r'void'),          # void
            ('FLOAT', r'float'),        # float
            ('FLOAT_CONST', r'\d(\d)*\.\d(\d)*'),  # FLOAT
            ('INTEGER_CONST', r'\d(\d)*'),  # INT
            ('IF', r'if'),              # if
            ('ELSE', r'else'),          # else
            ('WHILE', r'while'),        # while
            ('READ', r'read'),          # read
            ('PRINT', r'print'),        # print
            ('LBRACKET', r'\('),        # (
            ('RBRACKET', r'\)'),        # )
            ('COMMENT', r'[//].*[*/]\n'),
            ('INCREMENT',r'\+{2}'),
            ('DECREMENT', r'\-{2}'),
            ('LSBRACKET', r'\['),
            ('RSBRACKET', r'\]'),
            ('LCBRACKET', r'\{'),          # {
            ('RCBRACKET', r'\}'),          # }
            ('COMMA', r','),            # ,
            ('PCOMMA', r';'),           # ;
            ('EQ', r'=='),              # ==
            ('NE', r'!='),              # !=
            ('LE', r'<='),              # <=
            ('GE', r'>='),              # >=
            ('OR', r'\|\|'),            # ||
            ('AND', r'&&'),             # &&
            ('ATTR', r'\='),            # =
            ('LT', r'<'),               # <
            ('GT', r'>'),               # >
            ('PLUS', r'\+'),            # +
            ('MINUS', r'-'),            # -
            ('MULT', r'\*'),            # *
            ('DIV', r'\/'),             # /
            ('ID', r'[a-zA-Z]\w*'),     # IDENTIFIERS
            ('NEWLINE', r'\n'),         # NEW LINE
            ('SKIP', r'[ \t]+'),        # SPACE and TABS
            ('MISMATCH', r'.'),         # ANOTHER CHARACTER
        ]

        tokens_join = '|'.join('(?P<%s>%s)' % x for x in rules)#(?P<N>N)este syntaxa pentru a crea grupuri cu nume
        # print(tokens_join,'\n')
        lin_start = 0

        # Lists of output for the program
        token = []
        lengths = []
        row = []
        ids = []
        lexeme=[]
        # It analyzes the code to find the lexemes and their respective Tokens
        for m in re.finditer(tokens_join, code):
            # print(m)
            token_type = m.lastgroup
            token_lexeme = m.group(token_type)
            token_span=m.span(token_type)

            if token_type == 'NEWLINE':
                lin_start = m.end()
                self.lin_num += 1
            elif token_type == 'SKIP':
                continue
            elif token_type == 'MISMATCH':
                raise RuntimeError('%r unexpected on line %d' % (token_lexeme, self.lin_num))
            else:
                length = token_span[1] - token_span[0]
                id = m.start(token_type)  # id-ul de inceput al tokenului
                # col = m.start() - lin_start
                # column.append(col)
                token.append(token_type)
                lexeme.append(token_lexeme)
                row.append(self.lin_num)
                lengths.append(length)
                ids.append(id)
                # To print information about a Token
                # print('Token = {0}, Lexeme = \'{1}\', Row = {2}, Column = {3}'.format(token_type, token_lexeme, self.lin_num, col))
        return lexeme,token, lengths, row, ids #lexeme

class Buffer:
    def load_buffer(self):
        arq = open('program.c', 'r')
        text = arq.readline()

        buffer = []
        cont = 0

        # The buffer size can be changed by changing cont



        while text != "":
            buffer.append(text)
            text = arq.readline()
            cont += 1

            if cont == 20 or text == '':
                # Return a full buffer
                buf = ''.join(buffer)
                cont = 1
                yield buf

                # Reset the buffer
                buffer = []

        arq.close()

if __name__ == '__main__':
    Buffer = Buffer()
    Analyzer = LexicalAnalyzer()

    # Lists for every list returned list from the function tokenize
    token = []
    lexeme = []
    row = []
    column = []

    # Tokenize and reload of the buffer
    for i in Buffer.load_buffer():
        # print(i)
        lex,toke, lun, lin, id = Analyzer.tokenize(i)
        for j in range(len(toke)):
            print( 'Token = ',toke[j],' Lexeme= "',lex[j],'" Lungime = ',lun[j],' Linie = ',lin[j],' Id = ',id[j])
        token += toke
        # lexeme += lex
        row += lin
        # column += col