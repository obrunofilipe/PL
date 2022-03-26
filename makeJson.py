# função que, recebendo o elemento a escrever no ficheiro verifica se é uma string para o escrever com aspas ou um número, ou lista, para o escrever
# sem aspas 

def check_type(elem, final, cabecalho, field):
    if isinstance(elem, str):
        final.write("\"" + cabecalho[field] + "\": \"" + str(elem) + "\"")
    elif isinstance(elem, float):
        final.write("\"" + cabecalho[field] + "\": " + str(elem) + "")
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
            check_type(dict[fi], final, cabecalho, field)
            final.write("\n")
            field += 1
        else:
            final.write("\t\t")
            check_type(dict[fi], final, cabecalho, field)
            final.write(",\n")
            field += 1
    field += 1

#função que, com o auxílio das funções acima definidas, escreve a estrutura base do ficheiro .json

def dicToJson(dics, cabecalho):
    index = 0
    final = open("exemplo.json", "w", encoding="utf-8")
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

