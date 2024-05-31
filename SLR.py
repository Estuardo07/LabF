# Algoritmo para crear un AFD a partir de una gramatica utilizando SLR
import graphviz
import copy
import pandas as pd

class Estado:
    def __init__(self, id, gramatica):
        self.id = id
        self.gramatica = gramatica
        self.transiciones = {}
    
    # Se agrega una transicion al estado
    def agregar_transicion(self, simbolo, estado):
        # Si el simbolo ya existe en las transiciones se agrega el estado al que se va a transicionar
        if simbolo in self.transiciones:
            self.transiciones[simbolo].append(estado)
        # Si el simbolo no existe en las transiciones se crea una nueva transicion
        else:
            self.transiciones[simbolo] = [estado]
    
    # Se obtienen las transiciones de un estado
    def get_transiciones(self, simbolo):
        if simbolo in self.transiciones:
            return self.transiciones[simbolo]
        else:
            return []
    
    # Se borra una transicion de un estado
    def borra_transicion(self, simbolo):
        if simbolo in self.transiciones:
            del self.transiciones[simbolo]

# clase que guarda los estados y trancisiones del SLR y dibuja el AFD
class SLR:
    def __init__(self):
        self.estados = set()
        self.estado_inicial = set()
        self.tabla = {}
        self.gramatica_inicial = []
        self.terminals = []
        self.no_terminals = []

    def get_estados(self):
        return self.estados

    def get_estados_finales(self):
        return self.estados_finales

    def draw_afd(self):
        dot = graphviz.Digraph(comment='SLR')
        for estado in self.estados:
            pr = ""
            for produccion in estado.gramatica:
                pr += str(produccion) + "\n"
            dot.node(str(estado.id), str(pr), shape='square')
        for estado in self.estados:
            for simbolo in estado.transiciones:
                for estado_siguiente in estado.get_transiciones(simbolo):
                    dot.edge(str(estado.id), str(
                        estado_siguiente.id), label=simbolo.nombre)
        dot.format = 'png'
        dot.attr(rankdir='LR')
        dot.render('SLR', view=True)

    def get_estado(self, id):
        for estado in self.estados:
            if estado.id == id:
                return estado

    def get_estado_inicial(self):
        for estado in self.estados:
            if estado.id == 0:
                return estado


# clase para identificar simbolos terminales
class Terminal:

    def __init__(self, nombre):
        self.nombre = nombre

    def __str__(self):
        return self.nombre

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Terminal) and self.nombre == __value.nombre

    def __hash__(self) -> int:
        return hash(self.nombre)

# clase para identificar simbolos no terminales
class NoTerminal:

    def __init__(self, nombre):
        self.nombre = nombre

    def __str__(self):
        return self.nombre

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, NoTerminal) and self.nombre == __value.nombre

    def __hash__(self) -> int:
        return hash(self.nombre)

# clase para identificar facilmente el simbolo Punto
class Punto:
    def __init__(self):
        self.nombre = "."

    def __str__(self):
        return self.nombre

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Punto) and self.nombre == __value.nombre

# clase para guardar las producciones de la gramatica
class Produccion:
    def __init__(self, head, produccion: list):
        self.head = head
        self.produccion = produccion

    def __str__(self):
        return self.head.nombre + " -> " + " ".join(str(x) for x in self.produccion)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Produccion) and self.head == __value.head and self.produccion == __value.produccion

    def __hash__(self) -> int:
        return hash(self.head) + hash(self.produccion)

    def get_head(self):
        return self.head

    def get_produccion(self):
        return self.produccion

# cerradura de un estado
def cerradura_inicial(gramatica_evaluar, gramatica_inicial):
    gramatica_in = gramatica_inicial.copy()
    gramatica = []
    # agregar punto al inicio de la produccion si no tiene. Solo se ejecuta la primera vez que se pasa e'
    for produccion in gramatica_evaluar:
        if Punto() not in produccion.produccion:
            print("no tiene punto")
            print(str(produccion))
            produccion.produccion.insert(0, Punto())
            gramatica.append(produccion)
        else:
            # mover el punto a la siguiente posicion en la lista de la produccion
            index = produccion.produccion.index(Punto())
            if index + 1 < len(produccion.produccion):
                produccion.produccion[index], produccion.produccion[index +
                                                                    1] = produccion.produccion[index + 1], produccion.produccion[index]
                gramatica.append(produccion)
    
    # aplicar cerradura recursivamente hasta que no se pueda agregar mas producciones
    def cerradura(gramatica, gramatica_in):
        for produccion in gramatica:
            if produccion.produccion[-1] != Punto():
                index = produccion.produccion.index(Punto())
                simbol = produccion.produccion[index + 1]
                for produccion_gramatica in gramatica_in:
                    if simbol == produccion_gramatica.head:
                        if produccion_gramatica not in gramatica:
                            gramatica.append(produccion_gramatica)
                            produccion_gramatica.produccion.insert(0, Punto())
                            cerradura(gramatica, gramatica_in)
    cerradura(gramatica, gramatica_in)
    return gramatica

def ir_a(gramatica, simbolo):
    res = []
    # se busca el punto en la produccion y se busca si existe algun movimiento posible con el simbolo que se esta evaluando
    for produccion in gramatica:
        index = produccion.produccion.index(Punto())
        if index + 1 < len(produccion.produccion):
            if produccion.produccion[index + 1] == simbolo:
                res.append(produccion)
    return res

# funcion para agregar el simbolo de inicio a la gramatica. Por ejemplo e' -> e
def extender_gramatica(gramatica):
    element = list(gramatica.keys())[0]
    gramatica_extendida = {element + "'": [element]}
    gramatica_extendida.update(gramatica)
    print(gramatica_extendida)
    return gramatica_extendida

# convertir la lista de terminales en objetos de la clase Terminal
def terminales_to_obj(terminales):
    terminales_obj = []
    for terminal in terminales:
        terminales_obj.append(Terminal(terminal))
    return terminales_obj

# convertir la lista de no terminales en objetos de la clase NoTerminal
def no_terminales_to_obj(no_terminales):
    no_terminales_obj = []
    for no_terminal in no_terminales:
        no_terminales_obj.append(NoTerminal(no_terminal))
    return no_terminales_obj

# convertir la gramatica extendida a objetos de la clase Produccion
def gramatica_to_obj(gramatica_extendida, terminales, no_terminales):
    gramatica_inicial = []
    for no_terminal in gramatica_extendida:
        for produccion in gramatica_extendida[no_terminal]:
            s = produccion.split()
            prod = []
            for word in s:
                if word in terminales:
                    prod.append(Terminal(word))
                elif word in no_terminales:
                    prod.append(NoTerminal(word))
            new_prod = Produccion(NoTerminal(no_terminal), prod)
            gramatica_inicial.append(new_prod)
    return gramatica_inicial


def first(simbolo, gramatica_inicial):
    firstSet = set()
    epsilon = "epsilon"

    if isinstance(simbolo, Terminal):
        firstSet.add(simbolo)

    for produccion in gramatica_inicial:
        if produccion.head == simbolo:
            if produccion.produccion[0] == epsilon:
                firstSet.add(epsilon)
            elif isinstance(produccion.produccion[0], Terminal):
                firstSet.add(produccion.produccion[0])
            elif isinstance(produccion.produccion[0], NoTerminal):
                next_symbol = produccion.produccion[0]
                if next_symbol != simbolo:
                    firstSet.update(first(next_symbol, gramatica_inicial))

    return firstSet


def siguientes(gramatica_inicial):
    followSet = {}
    epsilon = "epsilon"

    for produccion in gramatica_inicial:
        followSet[produccion.head] = set()

    followSet[gramatica_inicial[0].head].add(Terminal("$"))

    for _ in range(len(gramatica_inicial)):
        for produccion in gramatica_inicial:
            for i in range(len(produccion.produccion)):
                if isinstance(produccion.produccion[i], NoTerminal):
                    if i + 1 < len(produccion.produccion):
                        next_symbol = produccion.produccion[i + 1]
                        if isinstance(next_symbol, Terminal):
                            followSet[produccion.produccion[i]].add(
                                next_symbol)
                        elif isinstance(next_symbol, NoTerminal):
                            followSet[produccion.produccion[i]].update(
                                first(next_symbol, gramatica_inicial)
                            )
                            if epsilon in first(next_symbol, gramatica_inicial):
                                followSet[produccion.produccion[i]].update(
                                    followSet[produccion.head]
                                )
                    else:
                        followSet[produccion.produccion[i]].update(
                            followSet[produccion.head]
                        )

    return followSet


# funcion principal para crear el SLR
def slr_construction(gramatica, terminales, no_terminales):
    gramatica_extendida = extender_gramatica(gramatica)
    gramatica_inicial = gramatica_to_obj(
        gramatica_extendida, terminales, no_terminales)
    simbolos = []
    # a lo largo del algoritmo se utiliza copy.deepcopy para evitar que se modifiquen las listas originales
    alt = copy.deepcopy(no_terminales)
    simbolos.extend(no_terminales_to_obj(alt))
    simbolos.extend(terminales_to_obj(copy.deepcopy(terminales)))
    l = []
    l.append(copy.deepcopy(gramatica_inicial[0]))
    # se aplica cerradura inicial
    res = cerradura_inicial(l, copy.deepcopy(gramatica_inicial))
    estados_por_evaluar = []
    # se crea el estado inicial y se inicia el SLR
    id = 0
    newEstado = Estado(id, res)
    id += 1
    estados_por_evaluar.append(newEstado)
    slr = SLR()
    slr.estados.add(newEstado)
    slr.estado_inicial.add(newEstado)
    # se aplican las reglas del SLR para crear los estados. Mientras haya estados por visitar, se repite el ciclo.
    while len(estados_por_evaluar) > 0:
        estado = estados_por_evaluar.pop(0)
        for simbolo in simbolos:
            gr = ir_a(copy.deepcopy(estado.gramatica), copy.deepcopy(simbolo))
            gr = cerradura_inicial(gr, copy.deepcopy(gramatica_inicial))
            # se valida que exista al menos una produccion
            if len(gr) > 0:
                # se valida si el estado ya existe en el SLR para no crearlo de nuevo y se agrega la transicion
                for x in slr.estados:
                    if gr == x.gramatica:
                        estado.agregar_transicion(simbolo, x)
                        break
                # si el estado no existe en el SLR se crea y se agrega la transicion
                else:
                    newEstado = Estado(id, gr)
                    id += 1
                    estado.agregar_transicion(simbolo, newEstado)
                    slr.estados.add(newEstado)
                    estados_por_evaluar.append(newEstado)

    # ordenar los estados en slr en orden de estado.id e imprimirlos en consola
    slr.estados = sorted(slr.estados, key=lambda estado: estado.id)
    for estado in slr.estados:
        print("estado: " + str(estado.id))
        for x in estado.gramatica:
            print(str(x))
    # devolver slr

    follow = siguientes(gramatica_inicial)

    tablaSLR = {}
    newsimbolos = copy.deepcopy(simbolos)
    newsimbolos.append(Terminal("$"))
    for simbolo in newsimbolos:
        tablaSLR[simbolo] = {}
    for estado in slr.estados:
        for produccion in estado.gramatica:
            # obtener el indice del punto
            dot_index = produccion.produccion.index(Punto())
            # si el punto no esta al final de la produccion
            if dot_index + 1 < len(produccion.produccion):
                # obtener el siguiente simbolo despues del punto
                next_symbol = produccion.produccion[dot_index + 1]
                # si el simbolo es un terminal
                if isinstance(next_symbol, Terminal):
                    # if [next_symbol][estado.id] no esta vacio, return conflict error
                    if estado.id in tablaSLR[next_symbol]:
                        if tablaSLR[next_symbol][estado.id] != "S" + str(
                                estado.transiciones[next_symbol][0].id
                        ):
                            print("conflict error in (%s, %s)" %
                                  (next_symbol, estado.id))
                            print(tablaSLR[next_symbol][estado.id] + " and " +
                                  "S" + str(estado.transiciones[next_symbol][0].id))
                            exit()
                    # agregar shift a la tabla
                    tablaSLR[next_symbol][estado.id] = "S" + str(
                        estado.transiciones[next_symbol][0].id
                    )
                # si el simbolo es un no terminal
                elif isinstance(next_symbol, NoTerminal):
                    # agregar un goto a la tabla
                    tablaSLR[next_symbol][estado.id] = str(
                        estado.transiciones[next_symbol][0].id
                    )
            # si el punto esta al final de la produccion
            else:
                # si la produccion es la inicial
                pr1 = copy.deepcopy(produccion)
                pr1.produccion.pop(dot_index)
                if pr1 == gramatica_inicial[0]:
                    # agregar el estado de aceptacion a la tabla
                    tablaSLR[Terminal("$")][estado.id] = "Accept"
                # si la produccion no es la inicial
                else:
                    # para cada simbolo en el follow del head de la produccion
                    for symbol in follow[produccion.head]:
                        # obtener el indice del punto
                        pr = copy.deepcopy(produccion)
                        # pop Punto
                        pr.produccion.pop(dot_index)
                        ind = gramatica_inicial.index(pr)
                        # if [symbol][estado.id] no esta vacio, return conflict error
                        if estado.id in tablaSLR[symbol]:
                            if tablaSLR[symbol][estado.id] != "R" + str(ind):
                                print("conflict error in (%s, %s)" %
                                      (symbol, estado.id))
                                print(tablaSLR[symbol][estado.id] + " and " +
                                      "R" + str(ind))
                                exit()
                        # agregar reduce a la tabla
                        tablaSLR[symbol][estado.id] = "R" + \
                            str(ind)
    # agregar la tabla al slr
    slr.tabla = tablaSLR
    # convertir todos los objetos a string para poder imprimir la tabla y manejar la simulacion
    new_string_table = {}
    for x in tablaSLR:
        new_string_table[str(x)] = {}
        for y in tablaSLR[x]:
            new_string_table[str(x)][str(y)] = tablaSLR[x][y]
    print("tabla")
    slr.tabla = new_string_table
    print(new_string_table)
    # crear un dataframe para imprimir la tabla en consola para que sea mas facil de leer
    df = pd.DataFrame(new_string_table)
    df = df.sort_index()
    print(df)

    slr.gramatica_inicial = gramatica_inicial
    slr.terminals = terminales
    slr.no_terminals = no_terminales

    return slr


def simularSLR(slr, cadena, gramatica_inicial, no_terminales):
    cadena = cadena.split(" ")
    pila = ['0']
    cadena.append("$")
    i = 0
    while True:
        print(pila)
        estado = pila[-1]
        simbolo = cadena[i]
        if simbolo not in slr.tabla or estado not in slr.tabla[simbolo]:
            print("Error")
            print("Estado: " + str(estado))
            print("Simbolo: " + str(simbolo))
            return False
        accion = slr.tabla[simbolo][estado]
        if accion[0] == "S":
            pila.append((accion[1:]))
            i += 1
        elif accion[0] == "R":
            produccion = gramatica_inicial[int(accion[1:])]
            print(str(produccion))
            for _ in range(len(produccion.produccion)):
                pila.pop()
            estado = pila[-1]
            simbolo_head = copy.deepcopy(produccion.head)
            simbolo_head = simbolo_head.nombre
            pila.append(slr.tabla[simbolo_head][estado])
        elif simbolo in no_terminales:
            pila.append((accion))
        elif accion == "Accept":
            return True
        else:
            return False
