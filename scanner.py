# Archivo generado automáticamente por el programa de instalación de la aplicación
import pickle
import sys

TOKENS = {0: 'COMMENT', 1: 'LOWERCASE', 2: 'UPPERCASE', 3: 'TOKEN', 4: 'IGNOREFLAG', 5: 'TWODOTS', 6: 'SEMICOLON', 7: 'OR', 8: 'SPLITTER', 9: 'SPACE', 10: 'NEWLINE'}

def get_tokens():
    return TOKENS


def simular_afd2(afd, cadena):
    tokens_encontrados = []
    estado_actual = afd.get_estado_inicial()
    cadena_aceptada = False
    estado_aceptado = []
    # print(estado_actual.id)
    cadena_leida = ''
    while len(cadena) > 0:
        for char in cadena:
            # print(char)
            estado_siguiente = estado_actual.get_trancisiones(char)
            if estado_siguiente:
                cadena_leida += char
                estado_actual = estado_siguiente[0]
                # print(estado_actual.id)
                if estado_actual.es_final:
                    estado_aceptado.append([estado_actual, cadena_leida])
            else:
                if estado_aceptado != []:
                    token_encontrado = estado_aceptado.pop()
                    # print(token_encontrado[1], token_encontrado[0].token)
                    tokens_encontrados.append(token_encontrado[0].token)

                    cadena = cadena[len(token_encontrado[1]):]
                    estado_actual = afd.get_estado_inicial()
                    cadena_leida = ''
                    estado_aceptado = []
                    break
                else:
                    cadena_leida += char
                    # print(cadena_leida, 'Lexema no encontrado')
                    cadena = cadena[len(cadena_leida):]
                    estado_actual = afd.get_estado_inicial()
                    cadena_leida = ''
                    break
        if estado_aceptado != []:
            token_encontrado = estado_aceptado.pop()
            # print(token_encontrado[1], token_encontrado[0].token)
            tokens_encontrados.append(token_encontrado[0].token)
            break
    return tokens_encontrados

def simulador(archivo):
    with open('afd.pickle', 'rb') as f:
        afd = pickle.load(f)
    
    try:
        with open(archivo, 'r') as f:
            lineas = f.readlines()
            
    except:
        print('Archivo no encontrado')
        exit()

    tokens_per_line = []
    for linea in lineas:
        tokens_per_line.append(simular_afd2(afd, linea))

    return tokens_per_line