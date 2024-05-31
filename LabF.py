from scanner import simulador
import pickle
from parser_simulator import simularSLR


def main():
    tokens_leidos = simulador('tokens.txt')
    tokens_leidos = [[element for element in sublist if element != '']
                     for sublist in tokens_leidos]

    with open('slr.pickle', 'rb') as f:
        slr = pickle.load(f)

    for linea in tokens_leidos:
        print(linea)
        print()
        print(simularSLR(slr, linea,
                         slr.gramatica_inicial, slr.no_terminals))

if __name__ == '__main__':
    main()
