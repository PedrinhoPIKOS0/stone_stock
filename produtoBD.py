import mysql.connector as connector

def IniciarConexao():
    endereco = "127.0.0.1"
    login = 'root'
    senha = '17122006'
    bd = 'stonestock'
    conexao = connector.connect(host=endereco, user=login, password=senha, database=bd)
    return conexao

def getCidadesMaisFrequentes():
    conexao = IniciarConexao()
    cursor = conexao.cursor()
    query = """
    SELECT cidade_destino, COUNT(*) as quantidade
    FROM pedido
    GROUP BY cidade_destino
    ORDER BY quantidade DESC
    LIMIT 5
    """
    cursor.execute(query)
    cidades = cursor.fetchall()
    cursor.close()
    conexao.close()
    return cidades

def getModelosMaisFrequentes():
    conexao = IniciarConexao()
    cursor = conexao.cursor()
    query = """
    SELECT modelo, COUNT(*) as quantidade
    FROM produto
    GROUP BY modelo
    ORDER BY quantidade DESC
    LIMIT 5
    """
    cursor.execute(query)
    modelos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return modelos

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
