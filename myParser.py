from yapar_reader import yaparReader
from SLR import slr_construction
from scanner import get_tokens
from jinja2 import Template
import pickle


def main():
    archivo_yapar = './pruebas/lab-f.yalp'
    terminals, no_terminals, gramatica = yaparReader(archivo_yapar)
    tokens = get_tokens()
    for val in terminals:
        if val in tokens.values():
            pass
        else:
            print("Tokens no definidos", val)
            exit(1)
    print('Todos los tokens estan definidos')
    print(terminals, no_terminals, gramatica)
    slr = slr_construction(gramatica, terminals, no_terminals)
    with open('slr.pickle', 'wb') as f:
        pickle.dump(slr, f)

    with open('template_parser.j2', 'r') as f:
        template = f.read()

    template = Template(template)
    rendered = template.render(slr=slr)
    with open('parser_simulator.py', 'w') as f:
        f.write(rendered)

if __name__ == '__main__':
    main()
