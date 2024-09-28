from flask import Flask, render_template, request, redirect, session
import mysql.connector as connector
from graficos import getCidadesMaisFrequentes, getModelosMaisFrequentes  # Importa as funções de graficos.py

app = Flask(__name__)
app.secret_key = "Pedro"

def IniciarConexao():
    endereco = "127.0.0.1"
    login = 'root'
    senha = '17122006'
    bd = 'stonestock'
    conexao = connector.connect(host=endereco, user=login, password=senha, database=bd)
    return conexao

@app.route("/logout")
def deslogar():
    return render_template("deslogar.html")

def getPedidos():
    conexao = IniciarConexao()
    cursor = conexao.cursor()
    query = "SELECT cidade_destino, quantidade_produto FROM pedido"
    cursor.execute(query)
    listaPedidos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return listaPedidos


@app.route("/quantidadeCidade")
def QuantidadeCidades():
    listaProdutos = getProdutos()
    listaVendas = getPedidos()
    return render_template("quantidadeCidades.html", listaVendas=listaVendas, listaProdutos=listaProdutos)

@app.route("/grafico")
def grafico():
    cidades = getCidadesMaisFrequentes()
    modelos = getModelosMaisFrequentes()
    
    cidades_labels = [cidade[0] for cidade in cidades]
    cidades_quantidade = [cidade[1] for cidade in cidades]

    modelos_labels = [modelo[0] for modelo in modelos]
    modelos_quantidade = [modelo[1] for modelo in modelos]

    return render_template(
        "grafico.html",
        cidades_labels=cidades_labels,
        cidades_quantidade=cidades_quantidade,
        modelos_labels=modelos_labels,
        modelos_quantidade=modelos_quantidade
    )


@app.route('/grafico_maquininhas')
def grafico_maquininhas():
    cursor = db.cursor()
    cursor.execute("SELECT cidade_destino, SUM(quantidade_produto) FROM TotalMaquininhasPorCidade GROUP BY cidade_destino")
    listaVendas = cursor.fetchall()

    cidades_labels = [row[0] for row in listaVendas]
    cidades_quantidade = [row[1] for row in listaVendas]

    return render_template('total_maquininhas.html', 
                           listaVendas=listaVendas,
                           cidades_labels=cidades_labels,
                           cidades_quantidade=cidades_quantidade)




@app.route("/perf_usuario")
def perf_usuario():
    return render_template("usuario.html")
    
# Cliente Routes
@app.route("/cadastro")
def cadastro():
    listaClientes = getClientes()
    return render_template("cadastrados.html", listaClientes=listaClientes)

@app.route("/editar_cliente/<cpf>")
def editar_cliente(cpf):
    conexao = IniciarConexao()
    cursor = conexao.cursor()
    query = "SELECT cpf_cliente, nome, cidade FROM cliente WHERE cpf_cliente = %s"
    cursor.execute(query, (cpf,))
    cliente = cursor.fetchone()
    cursor.close()
    conexao.close()
    if cliente:
        return render_template("editar_cliente.html", cliente=cliente)
    else:
        return "Cliente não encontrado", 404

@app.post("/atualizar_cliente/<cpf_antigo>")
def atualizar_cliente(cpf_antigo):
    nome = request.form["nome"]
    cpf_novo = request.form["cpf"]
    cidade = request.form["cidade"]
    conexao = IniciarConexao()
    cursor = conexao.cursor()
    query = "UPDATE cliente SET cpf_cliente = %s, nome = %s, cidade = %s WHERE cpf_cliente = %s"
    cursor.execute(query, (cpf_novo, nome, cidade, cpf_antigo))
    conexao.commit()
    cursor.close()
    conexao.close()
    return redirect("/cadastro")

@app.route("/excluir_cliente/<cpf>")
def excluir_cliente(cpf):
    conexao = IniciarConexao()
    cursor = conexao.cursor()
    query = "DELETE FROM cliente WHERE cpf_cliente = %s"
    cursor.execute(query, (cpf,))
    conexao.commit()
    cursor.close()
    conexao.close()
    return redirect("/cadastro")

# Pedido Routes
@app.route("/cliente")
def cliente():
    return render_template("cliente.html")

@app.route("/pedido")
def pedido():
    return render_template("pedido.html")

@app.route("/pedCad")
def pedCad():
    listaVendas = getPedidos()
    return render_template("pedCad.html", listaVendas=listaVendas)

@app.route("/editar_pedido/<numero_pedido>")
def editar_pedido(numero_pedido):
    conexao = IniciarConexao()
    cursor = conexao.cursor()
    query = """
    SELECT numero_pedido, cidade_destino, cpf_cliente, cod_produto, quantidade_produto
    FROM pedido
    WHERE numero_pedido = %s
    """
    cursor.execute(query, (numero_pedido,))
    pedido = cursor.fetchone()
    cursor.close()
    conexao.close()
    if pedido:
        return render_template("editar_pedido.html", pedido=pedido)
    else:
        return "Pedido não encontrado", 404

@app.post("/atualizar_pedido/<numero_pedido>")
def atualizar_pedido(numero_pedido):
    destino = request.form["destino"]
    cpf_cliente = request.form["cpf_cliente"]
    cod_produto = request.form["cod_produto"]
    quantidade_produto = request.form["quantidade_produto"]
    conexao = IniciarConexao()
    cursor = conexao.cursor()
    query = """
    UPDATE pedido
    SET cidade_destino = %s, cpf_cliente = %s, cod_produto = %s, quantidade_produto = %s
    WHERE numero_pedido = %s
    """
    cursor.execute(query, (destino, cpf_cliente, cod_produto, quantidade_produto, numero_pedido))
    conexao.commit()
    cursor.close()
    conexao.close()
    return redirect("/pedCad")

@app.route("/excluir_pedido/<numero_pedido>")
def excluir_pedido(numero_pedido):
    conexao = IniciarConexao()
    cursor = conexao.cursor()
    query = "DELETE FROM pedido WHERE numero_pedido = %s"
    cursor.execute(query, (numero_pedido,))
    conexao.commit()
    cursor.close()
    conexao.close()
    return redirect("/pedCad")

# Produto Routes
@app.route("/produto")
def produto():
    return render_template("produto.html")

@app.route("/prodCad")
def prodCad():
    listaProdutos = getProdutos()
    return render_template("prodCad.html", listaProdutos=listaProdutos)

@app.post("/add_produto")
def cadproduto():
    cod_produto = request.form["cod_produto"]
    nomeCl = request.form["nomeCl"]
    modelo = request.form["modelo"]
    qtdd = request.form["qtdd"]
    createProduto(cod_produto, nomeCl, modelo, qtdd)
    return redirect("/prodCad")

@app.route("/editar_produto/<codigo_produto>")
def editar_produto(codigo_produto):
    conexao = IniciarConexao()
    cursor = conexao.cursor()
    query = "SELECT codigo_produto, nome_cliente, modelo, quantidade FROM produto WHERE codigo_produto = %s"
    cursor.execute(query, (codigo_produto,))
    produto = cursor.fetchone()
    cursor.close()
    conexao.close()
    if produto:
        return render_template("editar_produto.html", produto=produto)
    else:
        return "Produto não encontrado", 404

@app.post("/atualizar_produto/<codigo_produto>")
def atualizar_produto(codigo_produto):
    nome_cliente = request.form["nome_cliente"]
    modelo = request.form["modelo"]
    quantidade = request.form["quantidade"]
    conexao = IniciarConexao()
    cursor = conexao.cursor()
    query = """
    UPDATE produto
    SET nome_cliente = %s, modelo = %s, quantidade = %s
    WHERE codigo_produto = %s
    """
    cursor.execute(query, (nome_cliente, modelo, quantidade, codigo_produto))
    conexao.commit()
    cursor.close()
    conexao.close()
    return redirect("/prodCad")

@app.route("/excluir_produto/<codigo_produto>")
def excluir_produto(codigo_produto):
    conexao = IniciarConexao()
    cursor = conexao.cursor()
    query = "DELETE FROM produto WHERE codigo_produto = %s"
    cursor.execute(query, (codigo_produto,))
    conexao.commit()
    cursor.close()
    conexao.close()
    return redirect("/prodCad")

# Vendas Routes
@app.route("/vendas")
def vendas():
    listaVendas = getPedidos()
    return render_template("vendas.html", listaVendas=listaVendas)

@app.route("/inicio")
def index():
    return render_template("inicio.html")

@app.route("/")
def login():
    return render_template("login.html")

@app.post("/login")
def logar():
    email = request.form["email"]
    senha = request.form["senha"]
    usuario = verificarUsuario(email)
    if usuario is not None and usuario[2] == senha:
        session["logado"] = True
        return redirect("/inicio")
    else:
        return redirect("/")

@app.post("/add_cliente")
def cadcliente():
    nome = request.form["nome"]
    cpf = request.form["cpf"]
    cidade = request.form["cidade"]
    createCliente(cpf, nome, cidade)
    return redirect("/cadastrados")

@app.post("/add_pedido")
def cadpedido():
    try:
        numeroPedido = request.form.get("numeroPedido")
        destino = request.form.get("destino")
        quantidade = request.form.get("quantidade")
        cpf_2 = request.form.get("cpf")
        codigoProduto = request.form.get("codigoProduto")
        
        if not (numeroPedido and destino and quantidade and cpf_2 and codigoProduto):
            return "Todos os campos são obrigatórios", 400

        createPedido(cpf_2, numeroPedido, codigoProduto, destino, quantidade)
        return redirect("/pedCad")
    except Exception as e:
        return f"Erro interno do servidor: {e}", 500


# Database Functions
def createCliente(cpf, nome, cidade):
    conexao = IniciarConexao()
    cursor = conexao.cursor()
    query = "INSERT INTO cliente (cpf_cliente, nome, cidade) VALUES (%s, %s, %s)"
    cursor.execute(query, [cpf, nome, cidade])
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

def createPedido(cpf_2, numeroPedido, codigoProduto, destino, quantidade):
    conexao = IniciarConexao()
    cursor = conexao.cursor()
    query = "INSERT INTO pedido (cpf_cliente, numero_pedido, cod_produto, cidade_destino, quantidade_produto) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, [cpf_2, numeroPedido, codigoProduto, destino, quantidade])
    conexao.commit()
    cursor.close()
    conexao.close()

def getPedidos():
    conexao = IniciarConexao()
    cursor = conexao.cursor()
    query = "SELECT numero_pedido, cidade_destino, cpf_cliente, cod_produto, quantidade_produto FROM pedido"
    cursor.execute(query)
    listaPedidos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return listaPedidos

def createProduto(cod_produto, nomeCl, modelo, qtdd):
    conexao = IniciarConexao()
    cursor = conexao.cursor()
    query = "INSERT INTO produto (codigo_produto, nome_cliente, modelo, quantidade) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, [cod_produto, nomeCl, modelo, qtdd])
    conexao.commit()
    cursor.close()
    conexao.close()

def getProdutos():
    conexao = IniciarConexao()
    cursor = conexao.cursor()
    query = "SELECT codigo_produto, nome_cliente, modelo, quantidade FROM produto"
    cursor.execute(query)
    listaProdutos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return listaProdutos

def verificarUsuario(email):
    conexao = IniciarConexao()
    cursor = conexao.cursor()
    query = "SELECT * FROM usuario WHERE email = %s"
    cursor.execute(query, (email,))
    usuario = cursor.fetchone()
    cursor.close()
    conexao.close()
    return usuario

if __name__ == "__main__":
    app.run(debug=True)
