import re
import ply.lex as lex


tokens = ["STRINGON","STRINGOFF","NUM","DELIM","STRING","CAMPO", "NEWLINE"]
#"FUNC"

states = [
    ("string", "exclusive"),
    ("cabecalho", "exclusive")
]


def t_cabecalho_NEWLINE(t):
    r'\n'
    lexer.pop_state()
    t.lexer.line += 1
    return t


def t_cabecalho_DELIM(t):
    r','
    return t


def t_cabecalho_CAMPO(t):
    r'[^,\n]+'
    t.lexer.cabecalho.append(t.value)
    return t


def t_NUM(t):
    r'\d+(\.\d+)?'
    return t


def t_STRINGON(t):
    r'"'
    lexer.push_state("string")
    return t


def t_string_STRINGOFF(t):
    r'"'
    lexer.pop_state()
    return t


def t_NEWLINE(t):
    r'\n'
    t.lexer.line += 1
    return t


def t_string_STRING(t):
    r'[^"]+'
    return t


def t_CAMPO(t):
    r'[^,\n]'
    return t


def t_DELIM(t):
    r','
    return t
    
t_INITIAL_ignore = " \t"

def t_ANY_error(t):
    print("Illegal Character!")
    return t

#define lex
lexer = lex.lex()




#My state
lexer.dic = {}
lexer.push_state("cabecalho")
lexer.cabecalho = []
lexer.line = 0


f = open("alunos.csv", encoding="utf-8")

content = f.read()
lexer.input(content)

dics = []

i = 0

dic = {}
campo = ""
numero = 0

for tok in lexer:
    print(tok)
    if tok.type == "STRING":
        campo = tok.value
        numero = 0
    elif tok.type == "NUM":
        campo = tok.value
        numero = 1
    elif tok.type == "DELIM":
        if numero == 0:
            dic[lexer.cabecalho[i]] = campo
        else:
            dic[lexer.cabecalho[i]] = int(campo)
        i += 1
    elif tok.type == "NEWLINE":
        print("NEWLINE")
        if numero == 0:
            dic[lexer.cabecalho[i]] = campo
        else:
            dic[lexer.cabecalho[i]] = int(campo)
        i = 0
        print(dic)
        dics.append(dic)
        dic = {}
    else:
        pass

final = open("alunos.json", "w", encoding="utf-8")
index = 0
field = 0


for dict in dics:
    if index == 0:
        final.write("[\n")
        index += 1
    elif index != len(dics)-1:
        final.write("\t{\n")
        for fi in dict:
            if field == len(lexer.cabecalho)-1: #ultimo elemento
                final.write("\t\t")
                final.write("\"" + fi + "\": \"" + str(dict[fi]) + "\"")
                final.write("\n")
                field += 1
            else:
                final.write("\t\t")
                final.write("\"" + fi + "\": \"" + str(dict[fi]) + "\"")
                final.write(",\n")
                field += 1
        final.write("\t},\n")
        index += 1
        field = 0
    else:
        final.write("\t{\n")
        for fi in dict:
            if field == len(lexer.cabecalho)-1: #ultimo elemento
                print("Entrei aqui")
                final.write("\t\t")
                final.write("\"" + fi + "\": \"" + str(dict[fi]) + "\"")
                final.write("\n")
                field += 1
            else:
                final.write("\t\t")
                final.write("\"" + fi + "\": \"" + str(dict[fi]) + "\"")
                final.write(",\n")
                field += 1
        final.write("\t}")
        index += 1
        field = 0
        final.write("\n]")



f.close()