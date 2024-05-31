from yalex_reader import yalexReader
from AFDD import regex_to_afd
from jinja2 import Template
import pickle


def main():
    archivo_yalex = './tests/lab-f.yal'
    rule_token, token_dic = yalexReader(archivo_yalex)
    with open('template.j2', 'r') as f:
        template = f.read()

    # delete the wor return for every element in the dictionary
    token_dic = {key: value.replace('return ', '')
                 for key, value in token_dic.items()}
    # delete white spaces
    token_dic = {key: value.replace(' ', '')
                 for key, value in token_dic.items()}

    template = Template(template)
    rendered = template.render(tokens=token_dic)
    with open('scanner.py', 'w') as f:
        f.write(rendered)
    afd = regex_to_afd(rule_token, token_dic)

    print("afd generado")
    with open('afd.pickle', 'wb') as f:
        pickle.dump(afd, f)


if __name__ == '__main__':
    main()