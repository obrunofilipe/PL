import re
import ply.lex as lex


tokens = ["STRINGON", "STRINGOFF", "NUM", "DELIM", "STRING", "CAMPO", "NEWLINE", "LISTON", "LISTOFF", "OP"]
#"FUNC"

states = [
    ("string", "exclusive"),
    ("cabecalho", "exclusive"),
    ("list", "exclusive")
]

def t_eof(t):
    t.lexer.line += 1
    t.lexer.index_col = 0
    t.lexer.dics.append(t.lexer.dic)
    t.lexer.dic = {}


def t_cabecalho_OP(t):
    r'::[a-zA-Z]+'
    campo = t.lexer.cabecalho[t.lexer.index_col]
    operacao = t.value[2:len(t.value):1]
    elem = campo + "_" + operacao
    t.lexer.cabecalho[t.lexer.index_col] = elem
    return t


def t_list_DELIM(t):
    r','
    return t


def t_list_NUM(t):
    r'\d+'
    if t.lexer.boundaries == 0:
        t.lexer.lista_min = int(t.value)
    else:
        t.lexer.lista_max = int(t.value)
    t.lexer.boundaries += 1
    return t


def t_cabecalho_LISTON(t):
    r'{'
    lexer.push_state("list")
    #lexer.if_list[-1] = 1
    return t


def t_list_LISTOFF(t):
    r'}'
    lexer.pop_state()
    if t.lexer.boundaries == 1:
        t.lexer.if_list[-1] = ((0,t.lexer.lista_min))
        t.lexer.list_flag = t.lexer.lista_min
    else:
        t.lexer.if_list[-1] = ((t.lexer.lista_min,t.lexer.lista_max))
        t.lexer.list_flag = t.lexer.lista_max
    t.lexer.boundaries = 0
    return t


def t_cabecalho_NEWLINE(t):
    r'\n'
    lexer.pop_state()
    t.lexer.line += 1
    t.lexer.index_col = 0
    t.lexer.list_flag = -1 
    return t


def t_cabecalho_DELIM(t):
    r',|;|\||\t'
    if t.lexer.list_flag > 1:
        t.lexer.list_flag -= 1

    else:
        print(t.lexer.list_flag)
        print(t.lexer.index_col)
        t.lexer.index_col += 1
    
    return t


def t_cabecalho_CAMPO(t):
    r'[^,;\t\|\n{]+'
    print(t.lexer.index_col)
    t.lexer.if_list.append((1,1))
    t.lexer.cabecalho.append(t.value)
    print(t.lexer.cabecalho[t.lexer.index_col])
    return t


def t_NUM(t):
    r'\d+(\.\d+)?'
    if t.lexer.list_flag == -1:
        t.lexer.dic[t.lexer.cabecalho[t.lexer.index_col]] = int(t.value)
    else:
        print(t.lexer.cabecalho)
        print(t.lexer.dic)
        print(t.lexer.index_col)
        t.lexer.dic[t.lexer.cabecalho[t.lexer.index_col]].append(int(t.value))

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
    t.lexer.list_flag = -1 
    t.lexer.dic = {}
    return t



def t_string_STRING(t):
    r'[^"]+'
    t.lexer.dic[t.lexer.cabecalho[t.lexer.index_col]] = t.value
    return t


def t_CAMPO(t):
    r'[^;,\t\|\n]+'
    t.lexer.dic[t.lexer.cabecalho[t.lexer.index_col]] = t.value
    return t


def t_DELIM(t):
    r',|;|\||\t'
    print("Flag: ", t.lexer.list_flag)
    if t.lexer.list_flag > 1:
        t.lexer.list_flag -= 1
    else:
        t.lexer.index_col += 1
        islist = t.lexer.if_list[t.lexer.index_col]
        if islist != (1,1):
            min,max = islist
            t.lexer.list_flag = max
            t.lexer.dic[t.lexer.cabecalho[t.lexer.index_col]] = []
            print("HELLO")
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
lexer.if_list = [] # (1,1) -> nao lista, else -> lista
lexer.line = 0
lexer.index_col = 0 #apontador da coluna atual
lexer.list_flag = -1
lexer.list = []
#[3,5,-1,8]

f = open("exemplo.csv", encoding="utf-8")

content = f.read()
lexer.input(content)

i = 0
for tok in lexer:
    print(tok)
    #pass


print(lexer.dics)


final = open("alunos.json", "w", encoding="utf-8")
index = 0
field = 0


def mean(lista):
    i = 0
    total = 0
    for elem in lista:
        total += elem
        i+=1
    result = total/i
    return result


def mult(lista):
    total = 1
    for elem in lista:
        total = total * elem
    return total

def count(lista):
    return len(lista)



possible_ops = ["sum", "mean", "mult", "max", "min", "sort"]

op = 0

def pick_op(mo):
    if mo.group(1) == "sum":
        dict[key] = sum(value)
    elif mo.group(1) == "mean":
        dict[key] = mean(value)
    elif mo.group(1) == "mult":
        dict[key] = mult(value)
    elif mo.group(1) == "min":
        dict[key] = min(value)
    elif mo.group(1) == "max":
        dict[key] = max(value)
    elif mo.group(1) == "sort":
        value.sort()
        dict[key] = value
    else:
        pass

for dict in lexer.dics:
    for key,value in dict.items():
        regex = r'[a-zA-Z0-9]+\_([a-zA-Z]+)'
        mo = re.search(regex, key)
        if mo:
            pick_op(mo)



for dict in lexer.dics:
    if index == 0:
        final.write("[\n")
        final.write("\t{\n")
        for fi in dict:
            if field == len(lexer.cabecalho)-1: #ultimo elemento
                final.write("\t\t")
                if isinstance(dict[fi], str):
                    final.write("\"" + fi + "\": \"" + str(dict[fi]) + "\"")
                elif isinstance(dict[fi], int):
                    final.write("\"" + fi + "\": " + str(dict[fi]) + "")
                else:
                    final.write("\"" + fi + "\": " + str(dict[fi]) + "")
                final.write("\n")
                field += 1
            else:
                final.write("\t\t")
                if isinstance(dict[fi], str):
                    final.write("\"" + fi + "\": \"" + str(dict[fi]) + "\"")
                elif isinstance(dict[fi], int):
                    final.write("\"" + fi + "\": " + str(dict[fi]) + "")
                else:
                    final.write("\"" + fi + "\": " + str(dict[fi]) + "")
                final.write(",\n")
                field += 1
        final.write("\t},\n")
        index += 1
        field = 0
    elif index != len(lexer.dics)-1:
        final.write("\t{\n")
        for fi in dict:
            if field == len(lexer.cabecalho)-1: #ultimo elemento
                final.write("\t\t")
                if isinstance(dict[fi], str):
                    final.write("\"" + fi + "\": \"" + str(dict[fi]) + "\"")
                elif isinstance(dict[fi], int):
                    final.write("\"" + fi + "\": " + str(dict[fi]) + "")
                else:
                    final.write("\"" + fi + "\": " + str(dict[fi]) + "")
                final.write("\n")
                field += 1
            else:
                final.write("\t\t")
                if isinstance(dict[fi], str):
                    final.write("\"" + fi + "\": \"" + str(dict[fi]) + "\"")
                elif isinstance(dict[fi], int):
                    final.write("\"" + fi + "\": " + str(dict[fi]) + "")
                else:
                    final.write("\"" + fi + "\": " + str(dict[fi]) + "")
                final.write(",\n")
                field += 1
        final.write("\t},\n")
        index += 1
        field = 0
    else:
        final.write("\t{\n")
        for fi in dict:
            if field == len(lexer.cabecalho)-1: #ultimo elemento
                final.write("\t\t")
                if isinstance(dict[fi], str):
                    final.write("\"" + fi + "\": \"" + str(dict[fi]) + "\"")
                elif isinstance(dict[fi], int):
                    final.write("\"" + fi + "\": " + str(dict[fi]) + "")
                else:
                    final.write("\"" + fi + "\": " + str(dict[fi]) + "")
                final.write("\n")
                field += 1
            else:
                final.write("\t\t")
                if isinstance(dict[fi], str):
                    final.write("\"" + fi + "\": \"" + str(dict[fi]) + "\"")
                elif isinstance(dict[fi], int):
                    final.write("\"" + fi + "\": " + str(dict[fi]) + "")
                else:
                    final.write("\"" + fi + "\": " + str(dict[fi]) + "")
                final.write(",\n")
                field += 1
        final.write("\t}")
        index += 1
        field = 0
        final.write("\n]")



f.close()