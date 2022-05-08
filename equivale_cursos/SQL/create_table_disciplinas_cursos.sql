CREATE TABLE disciplinas_cursos (
   id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
   versao_curso_id INT NOT NULL,
   codigo_disciplina INT NOT NULL,
   FOREIGN KEY (`versao_curso_id`) REFERENCES versoes_cursos(id),
   FOREIGN KEY (`codigo`) REFERENCES codigos_disciplinas(codigo_disciplina)
)
