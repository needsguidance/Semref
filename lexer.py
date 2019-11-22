from pygments.lexer import RegexLexer, words
from pygments.token import Name, Keyword


class SemrefLexer(RegexLexer):
    """Text Editor Syntax highlighter"""
    tokens = {
        'root': [
            (r'^[^:]+:\s*', Name.Variable),
            (words((
                'load', 'loadim', 'pop', 'store', 'push', 'loadrind', 'storerind',
                'add', 'sub', 'addim', 'subim', 'and', 'or', 'xor', 'not',
                'neg', 'shiftr', 'shiftl', 'rotar', 'rotal', 'jmprind', 'jmpaddr',
                'jcondrin', 'jcondaddr', 'loop', 'grt', 'grteq', 'eq', 'neq', 'nop',
                'call', 'return'), suffix=r'\b', prefix=r'\b'), Name.Class),
            (words(('r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7'),
                   suffix=r'\b', prefix=r'\b'), Name.Label),
            (words((
                'LOAD', 'LOADIM', 'POP', 'STORE', 'PUSH', 'LOADRIND', 'STORERIND',
                'ADD', 'SUB', 'ADDIM', 'SUBIM', 'AND', 'OR', 'XOR', 'NOT',
                'NEG', 'SHIFTR', 'SHIFTL', 'ROTAR', 'ROTAL', 'JMPRIND', 'JMPADDR',
                'JCONDRIN', 'JCONDADDR', 'LOOP', 'GRT', 'GRTEQ', 'EQ', 'NEQ',
                'NOP', 'CALL', 'RETURN'), suffix=r'\b', prefix=r'\b'), Name.Class),
            (words(('R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7'),
                   suffix=r'\b', prefix=r'\b'), Name.Constant),
            (words((
                'org', 'ORG', 'db', 'DB', 'CONST', 'const'), suffix=r'\b', prefix=r'\b'), Keyword),
            (words('#'), Keyword)

        ]
    }
