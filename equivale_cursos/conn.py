import mysql.connector

mydb = mysql.connector.connect(
  host="172.17.0.2",
  user="root",
  password="4813",
  database="equivale_cursos"
)

mycursor = mydb.cursor()
