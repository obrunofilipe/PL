import re
import ply.lex as lex


tokens = ["STRINGON", "STRINGOFF", "NUM", "DELIM", "STRING", "CAMPO", "NEWLINE", "LISTON", "LISTOFF"]
#"FUNC"

states = [
    ("string", "exclusive"),
    ("cabecalho", "exclusive"),
    ("list", "exclusive")
]



def t_list_DELIM(t):
    r','
    return t


def t_list_NUM(t):
    r'\d+'
    if t.lexer.boundaries == 0:
        t.lexer.list_min = t.value
    else:
        t.lexer.list_max = t.value
    t.lexer.boundaries += 1
    return t


def t_cabecalho_LISTON(t):
    r'{'
    lexer.push_state("list")
    lexer.if_list[-1] = 1
    return t


def t_list_LISTOFF(t):
    r'}'
    lexer.pop_state()
    if t.lexer.boundaries == 1:
        t.lexer.list_indexes.append(-1)
        t.lexer.list_indexes.append(t.lexer.list_min)
    else:
        t.lexer.list_indexes.append(t.lexer.list_min)
        t.lexer.list_indexes.append(t.lexer.list_max)
    t.lexer.boundaries = 0
    return t


def t_cabecalho_NEWLINE(t):
    r'\n'
    lexer.pop_state()
    t.lexer.line += 1
    return t


def t_cabecalho_DELIM(t):
    r','
    return t


def t_cabecalho_CAMPO(t):
    r'[^,\n{]+'
    t.lexer.if_list.append(0)
    t.lexer.cabecalho.append(t.value)
    return t


def t_NUM(t):
    r'\d+(\.\d+)?'
    print("NUM: ", t.lexer.index_col)
    t.lexer.dic[t.lexer.cabecalho[t.lexer.index_col]] = int(t.value)
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
    t.lexer.index_col = 0
    t.lexer.dics.append(t.lexer.dic)
    t.lexer.dic = {}
    return t



def t_string_STRING(t):
    r'[^"]+'
    t.lexer.dic[t.lexer.cabecalho[t.lexer.index_col]] = t.value
    return t


def t_CAMPO(t):
    r'[^,\n]'
    return t


def t_DELIM(t):
    r','
    t.lexer.index_col += 1
    return t
    
t_INITIAL_ignore = " \t"

def t_ANY_error(t):
    print("Illegal Character!")
    return t

#define lex
lexer = lex.lex()




#My state
lexer.dic = {}
lexer.dics = []
lexer.push_state("cabecalho") #começar a lista o cabeçalho
lexer.cabecalho = []
lexer.lista_min = 0
lexer.lista_max = 0
lexer.boundaries = 0
lexer.list_indexes = []
lexer.if_list = [] #0 -> não lista, 1 -> lista
lexer.line = 0
lexer.index_col = 0 #apontador da coluna atual
#[3,5,-1,8]

f = open("exemplo.csv", encoding="utf-8")

content = f.read()
lexer.input(content)

i = 0
for tok in lexer:
    pass

print(lexer.dics)
print(lexer.line)

final = open("alunos.json", "w", encoding="utf-8")
index = 0
field = 0



#for dict in dics:
#    if index == 0:
#        final.write("[\n")
#        index += 1
#    elif index != len(dics)-1:
#        final.write("\t{\n")
#        for fi in dict:
#            if field == len(lexer.cabecalho)-1: #ultimo elemento
#                final.write("\t\t")
#                final.write("\"" + fi + "\": \"" + str(dict[fi]) + "\"")
#                final.write("\n")
#                field += 1
#            else:
#                final.write("\t\t")
#                final.write("\"" + fi + "\": \"" + str(dict[fi]) + "\"")
#                final.write(",\n")
#                field += 1
#        final.write("\t},\n")
#        index += 1
#        field = 0
#    else:
#        final.write("\t{\n")
#        for fi in dict:
#            if field == len(lexer.cabecalho)-1: #ultimo elemento
#                print("Entrei aqui")
#                final.write("\t\t")
#                final.write("\"" + fi + "\": \"" + str(dict[fi]) + "\"")
#                final.write("\n")
#                field += 1
#            else:
#                final.write("\t\t")
#                final.write("\"" + fi + "\": \"" + str(dict[fi]) + "\"")
#                final.write(",\n")
#                field += 1
#        final.write("\t}")
#        index += 1
#        field = 0
#        final.write("\n]")
#
#

f.close()