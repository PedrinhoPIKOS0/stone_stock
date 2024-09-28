import mysql.connector as connector

def IniciarConexao():
    endereco = "127.0.0.1"
    login = 'root'
    senha = '17122006'
    bd ='stonestock'

    conexao = connector.connect(host=endereco,user=login,password=senha,database=bd)
    return conexao

def verificarUsuario(email):
    conexao = IniciarConexao()
    cursor = conexao.cursor()


    query="SELECT * FROM usuario WHERE email = %s"
    parametros=[email]

    cursor.execute(query,parametros)

    usuario = cursor.fetchone()
    cursor.close()
    conexao.close()
    return usuario 