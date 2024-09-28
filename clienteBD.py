from flask import Flask, render_template
import mysql.connector as connector

app = Flask(__name__)

def IniciarConexao():
    endereco = "127.0.0.1"
    login = 'root'
    senha = '17122006'
    bd ='stonestock'

    conexao = connector.connect(host=endereco, user=login, password=senha, database=bd)
    return conexao

def createCliente(cpf, nome, cidade):
    conexao = IniciarConexao()
    cursor = conexao.cursor()

    query = "INSERT INTO cliente (cpf_cliente, nome, cidade) VALUES (%s, %s, %s)"
    parametros = [cpf, nome, cidade]

    cursor.execute(query, parametros)
    
    conexao.commit()
    cursor.close()
    conexao.close()
    
def getClientes():
    conexao = IniciarConexao()
    cursor = conexao.cursor()

    query = "SELECT cpf_cliente, nome, cidade FROM cliente"
    cursor.execute(query)
    
    listaClientes = cursor.fetchall() 
    
    cursor.close()
    conexao.close()
    
    return listaClientes

@app.route("/cadastro")
def cadastro():
    listaClientes = getClientes() 
    return render_template("cadastrados.html", listaClientes=listaClientes)

if __name__ == "__main__":
    app.run(debug=True)
