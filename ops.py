#Métodos a aplicar depois da análise léxica e da conversão dos dados para uma lista de dicionários, um para cada linha do ficheiro.
#Métodos que poderão ser aplicados às listas

def mean(lista):
    i = 0
    total = 0
    print(lista)
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



import re

#operações sobre o dicionário. Aplicar às listas tudo o que for necessário aplicar. 

def apply_op(dics, cabecalho):
    for dict in dics:
        i = 0
        for key,value in dict.items():
            regex = r'[a-zA-Z0-9]+\-\>([a-zA-Z]+)'
            mo = re.search(regex, key)
            print(mo)
            print(value)
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
                    campo = a.split("->")[0]
                    op = a.split("->")[1]
                    print("Illegal function:", op)
                    cabecalho[i] = campo
            i += 1
