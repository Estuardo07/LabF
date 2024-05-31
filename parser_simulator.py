# Archivo generado automáticamente por el programa de instalación de la aplicación
import copy

def simularSLR(slr, cadena, gramatica_inicial, no_terminales):
    # cadena = cadena.split(" ")
    pila = ['0']
    cadena.append("$")
    i = 0
    while True:
        print(pila)
        estado = pila[-1]
        simbolo = cadena[i]
        if simbolo not in slr.tabla or estado not in slr.tabla[simbolo]:
            # print(slr.tabla['ID']['3'])
            print("Error")
            print("Estado: " + str(estado))
            print("Simbolo: " + str(simbolo))
            return False
        accion = slr.tabla[simbolo][estado]
        if accion[0] == "S":
            # pila.append(simbolo)
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
            # print(simbolo_head)
            # print(slr.tabla['f'])
            # print(type(simbolo_head))
            # print(slr.tabla[simbolo_head.name])
            pila.append(slr.tabla[simbolo_head][estado])
        elif simbolo in no_terminales:
            pila.append((accion))
        elif accion == "Accept":
            return True
        else:
            return False
