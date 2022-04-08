import requests
from bs4 import BeautifulSoup

class Curso:
    def __init__(self, nome, versoes_curriculares):
        self.nome = nome
        self.versoes_curriculares = versoes_curriculares

def getListaCursos():
    baseUrl = 'https://siga.ufrj.br/sira/repositorio-curriculo/'
    url = 'https://siga.ufrj.br/sira/repositorio-curriculo/comboListaCursos.html'

    # requests main page
    request_page = requests.get(url)
    request_page_html = BeautifulSoup(request_page.text, 'html.parser')

    # gets specific file through js onload attr
    page_js_link = request_page_html.body.attrs["onload"]
    lista_cursos_file = page_js_link.rsplit(" ")[2].rsplit("'")[1] 

    # does final request 
    lista_cursos_url = (baseUrl + lista_cursos_file)
    request_lista_cursos = requests.get(lista_cursos_url).text
    lista_cursos_html = BeautifulSoup(request_lista_cursos, 'html.parser')

    return lista_cursos_html

def getVersoesCurso(lista_cursos_html):
    versoes_cursos = []

    linhas_lista_cursos = lista_cursos_html.find_all("tr", class_="tableTitleBlue")

    for linha_curso in linhas_lista_cursos:
        try:
            nome_do_curso = linha_curso.contents[0].find("b").text
            versoes_do_curso = linha_curso.contents[2].find_all("a", class_="linkNormal")

            for i, versao_curso in enumerate(versoes_do_curso):
                versoes_do_curso[i] = versao_curso.text                

            versoes_cursos.append(Curso(nome_do_curso, versoes_do_curso))
        except:
            pass

    return versoes_cursos

def viewVersoesCursos(versoes_cursos):
    for curso in versoes_cursos:
        print("Nome:", curso.nome)
        print("Versões curriculares:")
        for versao in curso.versoes_curriculares:
            print(versao)
        print("\n")


lista_cursos_html = getListaCursos()
versoes_cursos = getVersoesCurso(lista_cursos_html)
viewVersoesCursos(versoes_cursos)



