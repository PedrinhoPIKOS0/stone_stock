import mysql.connector as connector

def IniciarConexao():
    endereco = "127.0.0.1"
    login = 'root'
    senha = '17122006'
    bd ='stonestock'

    conexao = connector.connect(host=endereco, user=login, password=senha, database=bd)
    return conexao

def createPedido(cpf_2, numeroPedido, codigoProduto, destino, quantidade):
    try:
        conexao = IniciarConexao()
        cursor = conexao.cursor()

        query = "INSERT INTO pedido (cpf_cliente, numero_pedido, cod_produto, cidade_destino, quantidade_produto) VALUES (%s, %s, %s, %s, %s)"
        parametros = [cpf_2, numeroPedido, codigoProduto, destino, quantidade]

        cursor.execute(query, parametros)
        conexao.commit()
    except connector.Error as err:
        print(f"Erro ao inserir pedido: {err}")
        raise
    finally:
        cursor.close()
        conexao.close()


def getPedidos():
    conexao = IniciarConexao()
    cursor = conexao.cursor()
    query = "SELECT cidade_destino, quantidade_produto FROM pedido"
    cursor.execute(query)
    pedidos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return pedidos
