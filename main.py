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

# Regras definidas para o estado exclusivo cabecalho

def t_cabecalho_OP(t):
    r'::[a-zA-Z]+'
    campo = t.lexer.cabecalho[t.lexer.index_col]
    operacao = t.value[2:len(t.value):1]
    elem = campo + "_" + operacao
    t.lexer.cabecalho[t.lexer.index_col] = elem
    return t

def t_cabecalho_LISTON(t):
    r'{'
    lexer.push_state("list")
    #lexer.if_list[-1] = 1
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
        t.lexer.index_col += 1
    return t


def t_cabecalho_CAMPO(t):
    r'[^,;\t\|\n{]+'
    t.lexer.if_list.append((1,1))
    t.lexer.cabecalho.append(t.value)
    return t


# Regras definidas para o estado exclusivo list

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




# Regras definidas para o estado exlcusivo string

def t_string_STRINGOFF(t):
    r'"'
    lexer.pop_state()
    return t


def t_string_STRING(t):
    r'[^"]+'
    t.lexer.dic[t.lexer.cabecalho[t.lexer.index_col]] = t.value
    return t



# Estados definidos para os tokens no estado INITIAL

def t_NUM(t):
    r'\d+(\.\d+)?'
    if t.lexer.list_flag == -1:
        t.lexer.dic[t.lexer.cabecalho[t.lexer.index_col]] = int(t.value)
    else:
        t.lexer.dic[t.lexer.cabecalho[t.lexer.index_col]].append(int(t.value))

    return t

def t_STRINGON(t):
    r'"'
    lexer.push_state("string")
    return t

def t_NEWLINE(t):
    r'\n'
    t.lexer.line += 1
    t.lexer.index_col = 0
    t.lexer.dics.append(t.lexer.dic)
    t.lexer.list_flag = -1 
    t.lexer.dic = {}
    return t


def t_CAMPO(t):
    r'[^;,\t\|\n]+'
    if t.lexer.list_flag == -1:
        t.lexer.dic[t.lexer.cabecalho[t.lexer.index_col]] = t.value
    else:
        t.lexer.dic[t.lexer.cabecalho[t.lexer.index_col]].append(t.value)
    return t


def t_DELIM(t):
    r',|;|\||\t'
    if t.lexer.list_flag > 1:
        t.lexer.list_flag -= 1
    else:
        t.lexer.index_col += 1
        islist = t.lexer.if_list[t.lexer.index_col]
        if islist != (1,1):
            min,max = islist
            t.lexer.list_flag = max
            t.lexer.dic[t.lexer.cabecalho[t.lexer.index_col]] = []
        else:
            t.lexer.list_flag = -1
    return t

# Caracteres que serão ignorados no estado INITIAL

t_INITIAL_ignore = " \t"


# Definição da regra de erro para qualquer estado

def t_ANY_error(t):
    print("Illegal Character!")
    return t



#define lex
lexer = lex.lex()

#My state
lexer.dic = {}                # estrutura de dados onde vai ser guardado cada registo, um dicionário
lexer.dics = []               # estrutura de dados onde vão ser guardados todos os registos, uma lista de dicionários
lexer.push_state("cabecalho") # começar a lista o cabeçalho
lexer.cabecalho = []          # lista onde ficará armazenado o cabeçalho do ficheiro
lexer.lista_min = 0           # número que indica o número mínimo de elementos da lista
lexer.lista_max = 0           # número que indica o número máximo de elementos da lista
lexer.boundaries = 0          # flag que diz se a lista especificada no cabecalho tem 1 ou 2 fronteiras       
lexer.if_list = []            # (1,1) -> nao lista, else -> lista
lexer.line = 0                # variável que indica quantas linhas existem no ficheiro
lexer.index_col = 0           # apontador da coluna atual
lexer.list_flag = -1          # 


#Ficheiro de leitura
f = open("exemplo.csv", encoding="utf-8")
content = f.read()
lexer.input(content)

#Ciclo principal da análise léxica do ficheiro csv.

for tok in lexer:
    pass



#Métodos que poderão ser aplicados às listas

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



#operações sobre o dicionário. Aplicar às listas tudo o que for necessário aplicar. 

def apply_op(dics):
    for dict in dics:
        i = 0
        for key,value in dict.items():
            regex = r'[a-zA-Z0-9]+\_([a-zA-Z]+)'
            mo = re.search(regex, key)
            if mo:
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
                    a = mo.group(0)
                    campo = a.split("_")[0]
                    op = a.split("_")[1]
                    print("Illegal function:", op)
                    lexer.cabecalho[i] = campo
            i += 1


# função que, recebendo o elemento a escrever no ficheiro verifica se é uma string para o escrever com aspas ou um número, ou lista, para o escrever
# sem aspas 

def check_type(elem, final, cabecalho, field):
    if isinstance(elem, str):
        final.write("\"" + cabecalho[field] + "\": \"" + str(elem) + "\"")
    elif isinstance(elem, int):
        final.write("\"" + cabecalho[field] + "\": " + str(elem) + "")
    elif isinstance(elem,list):
        final.write("\"" + cabecalho[field] + "\": [")
        it = 0
        for i in elem:
            if it != len(elem)-1:
                if isinstance(i,str):
                    final.write("\"" + str(i) + "\", ")
                else:
                    final.write(str(i) + ", ")
            else:
                if isinstance(i,str):
                    final.write("\"" + str(i) + "\"")
                else:
                    final.write(str(i))
            it += 1
        final.write("]")
    else:
        final.write("\"" + cabecalho[field] + "\": " + str(elem) + "")


#funcao que itera os campos do dicionario e escreve os seus elementos no ficheiro .json, devidamente identados

def iterate_fields(dict, final, cabecalho):
    field = 0
    for fi in dict:
        if field == len(cabecalho)-1: #ultimo elemento
            final.write("\t\t")
            check_type(dict[fi], final, lexer.cabecalho, field)
            final.write("\n")
            field += 1
        else:
            final.write("\t\t")
            check_type(dict[fi], final, lexer.cabecalho, field)
            final.write(",\n")
            field += 1
    field += 1

#função que, com o auxílio das funções acima definidas, escreve a estrutura base do ficheiro .json

def dicToJson(dics, cabecalho):
    index = 0
    final = open("alunos.json", "w", encoding="utf-8")
    for dict in dics:
        if index == 0:
            final.write("[\n")
        
        final.write("\t{\n")
        iterate_fields(dict, final, cabecalho)
        if index != len(dics)-1:
            final.write("\t},\n")
        else:
            final.write("\t}")
            final.write("\n]")
        index += 1

#Métodos a aplicar depois da análise léxica e da conversão dos dados para uma lista de dicionários, um para cada linha do ficheiro.

print("Dicionario:", lexer.dics)

apply_op(lexer.dics)
dicToJson(lexer.dics, lexer.cabecalho)

f.close()