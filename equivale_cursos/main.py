import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://siga.ufrj.br/'
SIRA_PATH = 'sira/repositorio-curriculo/'

class VersoesCursos:
    url_cursos_versoes = []
    versoes_cursos = []

    def __init__(self, nome, versoes_curriculares):
        self.nome = nome
        self.versoes_curriculares = versoes_curriculares
class DisciplinasCursos():
    disciplinas_por_curso = []

    def __init__(self, nome, versao_curricular, codigos_disciplinas):
        self.nome = nome
        self.versao_curricular = versao_curricular
        self.codigos_disciplinas = codigos_disciplinas
class DisciplinasCodigos():
    disciplinas = []

    def __init__(self, nome, codigo):
        self.nome = nome
        self.codigo = codigo

def main():
    lista_cursos_html = get_lista_cursos()
    get_versoes_curso(lista_cursos_html)
    get_disciplinas_links(VersoesCursos.url_cursos_versoes)

def get_lista_cursos():
    url = f"{BASE_URL + SIRA_PATH}comboListaCursos.html"

    request_page = requests.get(url)
    request_page_html = BeautifulSoup(request_page.text, 'html.parser')

    page_js_link = request_page_html.body.attrs["onload"]
    lista_cursos_file = page_js_link.rsplit(" ")[2].rsplit("'")[1] 

    lista_cursos_url = (BASE_URL + SIRA_PATH + lista_cursos_file)
    request_lista_cursos = requests.get(lista_cursos_url).text
    lista_cursos_html = BeautifulSoup(request_lista_cursos, 'html.parser')

    return lista_cursos_html

def get_versoes_curso(lista_cursos_html):
    versoes_cursos = VersoesCursos.versoes_cursos
    url_cursos_versoes = VersoesCursos.url_cursos_versoes

    linhas_lista_cursos = lista_cursos_html.find_all("tr", class_="tableTitleBlue")

    for linha_curso in linhas_lista_cursos:
        try:
            nome_do_curso = linha_curso.contents[0].find("b").text
            versoes_do_curso = linha_curso.contents[2].find_all("a", class_="linkNormal")

            for i, versao_curso in enumerate(versoes_do_curso):
                versoes_do_curso[i] = versao_curso.text
                url_cursos_versoes.append(versao_curso['href'])          

            versoes_cursos.append(VersoesCursos(nome_do_curso, versoes_do_curso))
        except:
            pass

def get_disciplinas_links(disciplina_url):
    for url in disciplina_url:
        url = url.split("'")[1]
        url = f"https://siga.ufrj.br{url}"
        
        request_page = requests.get(url)
        request_page_html = BeautifulSoup(request_page.text, 'html.parser')

        frame = request_page_html.find(id='main').attrs['src']
        url = f"https://siga.ufrj.br{frame}"

        request_page = requests.get(url)
        request_page_html = BeautifulSoup(request_page.text, 'html.parser')

        frame = request_page_html.find(id='frameDynamic').attrs['src']
        url = f"https://siga.ufrj.br/sira/repositorio-curriculo/{frame}"

        get_disciplinas(url)

def get_disciplinas(curso_page):
    request_page = requests.get(curso_page)
    request_page_html = BeautifulSoup(request_page.text, 'html.parser')

    nome_curso = request_page_html.findAll("tr", class_="tableTitle")[0].find("b").contents[0]
    nome_curso = nome_curso.split("em ")[1]

    curriculo = request_page_html.findAll("tr", class_="tableTitleBlue")[0].find("b").text
    curriculo = curriculo.split("de ")[1]

    periodos = request_page_html.findAll("table", class_="cellspacingTable")
    del periodos[0] 

    codigos_do_curso = []

    disciplinas = DisciplinasCodigos.disciplinas
    disciplinas_por_curso = DisciplinasCursos.disciplinas_por_curso

    for periodo in periodos:
        linhas_das_disciplinas = periodo.findAll("tr", class_="tableBodyBlue2")
        linhas_das_disciplinas += periodo.findAll("tr", class_="tableBodyBlue1")
        codigo = periodo.findAll("a", class_="linkNormal")

        for linha_disciplina in linhas_das_disciplinas:
            try:
                codigo = linha_disciplina.find("a", class_="linkNormal").text
                nome = linha_disciplina.findAll("td")[1].text
                disciplinas.append(DisciplinasCodigos(nome, codigo))
                codigos_do_curso.append(codigo)
            except Exception:
                pass

    disciplinas_por_curso.append(DisciplinasCursos(nome_curso, curriculo, codigos_do_curso))

if __name__ == "__main__":
    main()