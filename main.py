from collections import Counter
import math

# Creamos un objeto "Info" que nos devolverá la función "codificar()". Este contendrá toda
# la info de la codificación: el árbol de huffman, el código y una tabla. La tabla contiene para 
# cada letra, su codificación y su frecuencia: "tabla[letra] = [frecuencia, codificacion]"
class Info:
    def __init__(self):
        self.tabla = dict()
        self.arbol = None
        self.codigo = None
        self.texto = None

# crear arbol de huffman
def crear_arbol(texto, info):
    # contar las veces que aparece cada letra: lista de tuplas '(letra, número de veces que aparece)'
    c = Counter(texto)
    N = len(texto)
    for k,v in c.items():
        info.tabla[k] = [v/N, ""]
    # ordenarlas de mayor a menor (número de apariciones)
    tuplas = sorted(c.items(), key=lambda x : x[1])
    tuplas.reverse()
    # crear arbol de forma recursiva
    N = len(tuplas)
    for k in range(N-1):
        # coger los dos arboles de menos peso: a1 y a2
        a1, p1 = tuplas[-1]
        a2, p2 = tuplas[-2]
        del tuplas[-1]
        del tuplas[-1]
        # unir a1 y a2 
        a = (a1, a2)
        peso = p1 + p2
        union = [a,peso]
        # guardar la unión
        if k == N-2:
            tuplas.append(union)
        else:
            length = len(tuplas)
            for i in range(length):
                if tuplas[i][1] <= peso:
                    tuplas.insert(i, union)
                    break
                elif i == length-1:
                    tuplas.append(union)
    # en 'tuplas' nos queda finalmente un único árbol, el que buscamos
    info.arbol = tuplas[0][0]

# crear un diccionario con los códigos (0 / 1) de cada letra
def crear_tabla_codigos(arbol, prefijo, info):
    # comprobar si es una hoja
    if type(arbol) == str:
        info.tabla[arbol][1] = prefijo
    # añadir "0" y "1" al prefijo según vayamos a la izquierda o derecha del árbol
    else:
        crear_tabla_codigos(arbol[0], prefijo + "0", info)
        crear_tabla_codigos(arbol[1], prefijo + "1", info)

# codificar el texto con una cierta tabla de codigos, es ir letra por letra sustituyendola por su código
def codificar_con_tabla(texto, tabla):
    codigo = ""
    for c in texto:
        codigo += tabla[c][1]
    return codigo

# codificar mensaje desde 0
def codificar(texto):
    info = Info()
    info.texto = texto
    crear_arbol(texto, info)
    crear_tabla_codigos(info.arbol, "", info)
    info.codigo = codificar_con_tabla(texto, info.tabla)
    return info
    
# descodificar mensaje
def descodificar(codigo, arbol):
    texto = ""
    actual = arbol
    for c in codigo:
        if c == "0":
            actual = actual[0]
        else:
            actual = actual[1]
        if type(actual) == str:
            texto += actual
            actual = arbol
    return texto


# -------------------------------------------------------------------------
#                           PARTE DE EJERCICIOS
# -------------------------------------------------------------------------

with open('ingles.txt', 'r',encoding="utf8") as file:
    en = file.read()
     
with open('español.txt', 'r',encoding="utf8") as file:
    es = file.read()

# Codificamos y guardarmos la información en tuplas (español , inglés)
info   = (codificar(es), codificar(en))
nombre = ("Español", "Ingles")
texto  = (es, en)

# Entropía
H = lambda tabla : -sum([v[0]*math.log2(v[0]) for k,v in tabla.items()])
# Longitud media
L = lambda tabla : sum([tabla[letra][0] * len(tabla[letra][1]) for letra in tabla.keys()])
# Error
E = lambda info : math.sqrt( (1.0/len(info.texto))**2 * sum([ (math.log2(v[0]) + 1.0/math.log(2))**2  for v in info.tabla.values()]) )


def pregunta1():
    for i in range(2):
        print("\n1) Idioma:", nombre[i])
        longitud = L(info[i].tabla)
        print("2) Longitud media: {:.4f}".format(longitud))
        print("3.0) Error:")
        print(" E(C) =", E(info[i])) # => redondeamos a 2 decimales
        print("3) Comprobación del primer teorema de Shannon:")
        print(" H(C) = {:.2f}".format(H(info[i].tabla)), ", L(C) = {:.2f}".format(longitud), " => H(C) <= L(C) < H(C) + 1")
        print("4) Codigos del alfabeto:")
        for letra in info[i].tabla.keys():
            l = letra if letra != "\n" else "\\n"
            print(f"\t[{l}] ->", info[i].tabla[letra][1])

def pregunta2():
    X = "dimension"
    for i in range(2):
        cod = codificar_con_tabla(X, info[i].tabla)
        print(f"\n[{nombre[i]}] \nCodificacion de 'dimension':", cod)
        n = len(cod)
        N = 8 # log_2(256) = 8 -> siendo 256, el nº de carcateres que se usan en el código ascii
        print("Longitud:", n, f"\t(Longitud ascii: {N*len(X)})")

def pregunta3():
    print(f"\n[{nombre[1]}]")
    palabra = "isomorphism"
    cod = codificar_con_tabla(palabra, info[1].tabla)
    decod = descodificar(cod, info[1].arbol)
    print(f"Decodificacion de '{cod}':", decod)

def main():
    print("\nPREGUNTA 1:")
    pregunta1()
    print("\nPREGUNTA 2:")
    pregunta2()
    print("\nPREGUNTA 3:")
    pregunta3()
    print()


if __name__ == "__main__":
    main()