"""
Desafio 02:
Tomando por base o banco de dados criado em aula, com a tabela produto, crie uma nova tabela de nome "venda", com os seguintes campos:
 - IdVenda
 - NomeCliente
 - IdProduto
 - Quantidade
 - DataHoraVenda
Faça um programa em Python com um menu interável no Console, usando while, onde o usuário poderá escolher as seguintes opções para executar:
 1) Cadastrar novo produto
 2) Visualizar todos os produtos
 3) Visualizar um produto específico de acordo com o ID
 4) Registrar venda, solicitando que o usuário digite o nome do cliente que está realizando a compra, o ID do produto que será comprado e a quantidade comprada. Ao registrar a venda, deve-se debitar a quantidade de produtos comprados do estoque, e não havendo estoque suficiente para a compra, não concluir a venda e apresentar uma mensagem em tela falando que não é possível comprar aquela determinada quantidade do produto.
A entrega do desafio 02 deve ser feita através de um repositório no GITHub
"""
import mysql.connector
#conexão
import mysql.connector

conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='sua_senha_aqui',
    database='demodb'
)

cursor = conn.cursor()

#funcoes
def f_cadastroProduto():
    nomeProduto = input("Digite o nome do produto:")
    valorProduto = float(input("Digite o valor do produto:"))
    codBarProduto = input("Digite o código de barras do produto:")
    estoqueProduto= float(input("Digite o estoque do produto:"))

    cursor.execute("INSERT INTO demodb.produtos (nome, valor, cod_bar, estoque) "
                   "VALUES(%s, %s, %s, %s);", (nomeProduto, valorProduto, codBarProduto, estoqueProduto))
    conn.commit()

    print("======================================")
    print("= Inserido com sucesso !             =")

def f_buscaProdutos(id):
    listaProduto = []

    if id == 0:
        cursor.execute("SELECT id, nome, valor, cod_bar, estoque FROM demodb.produtos;")
    else:
        cursor.execute(f"SELECT id, nome, valor, cod_bar, estoque FROM demodb.produtos where id = {id}")

    for produto in cursor.fetchall():
        listaProduto.append(produto)

    print("==============================================")
    print("ID, Nome, Valor(R$), Codigo de Barras, Estoque")
    print("==============================================")

    for produto in listaProduto:
        print(f"{produto[0]}, {produto[1]}, {produto[2]}, "
              f"{produto[3]}, {produto[4]}")

def f_novaCompra():
    nomeCliente = input("Digite seu nome:")
    idProduto = int(input("Digite o id do produto:"))
    qtdProduto = int(input("Digite a quantidade desejada:"))
    estoqueProduto = []
    novoEstoque=0

    #consulta quantidade em estoque
    cursor.execute(f"SELECT estoque FROM demodb.produtos where id = {idProduto}")
    estoqueProduto = cursor.fetchone()

    novoEstoque = estoqueProduto[0] - qtdProduto

    if novoEstoque >= 0:
        #atualiza o estoque do produto
        cursor.execute("UPDATE demodb.produtos "
                       "SET estoque = %s WHERE id = %s ", (novoEstoque, idProduto))

        #cadastra novo cliente

        cursor.execute("INSERT INTO demodb.clientes (nomeCliente, idProduto, qtd, dthrVenda) VALUES(%s, %s, %s, NOW());",
                       (nomeCliente, idProduto, qtdProduto))

        conn.commit()

        print("======================================")
        print("= Compra executada com sucesso!      =")
    else:
        print("==========================================")
        print("= Estoque indisponível para este produto =")

def abreMenu():
    opcaoMenu = 0
    qtdErro = 0
    idProduto = 0
    opcaoContinue = ''

    print("======================================")
    print("=              Menu                  =")
    print("======================================")
    print("= 1 - Cadastrar novo produto         =")
    print("= 2 - Visualizar todos os produtos   =")
    print("= 3 - Visualizar produtos específico =")
    print("= 4 - Realizar compra                =")
    print("= 5 - Encerrar                       =")
    print("======================================")

    #tratamento da entrada
    while qtdErro < 3:
        try:
            opcaoMenu = int(input("Escolha uma opcao:"))
        except ValueError:
            qtdErro = qtdErro+1
            if qtdErro < 3:
                print("Escolha uma opção Valida")
            else:
                print("============================================================")
                print("= Esgotada quantidade de erros, tente novamente mais tarde =")
        else:
            if opcaoMenu < 1 or opcaoMenu > 5:
                qtdErro = qtdErro + 1
            else:
                qtdErro = qtdErro + 3

    #chamada da função correspondente
    if opcaoMenu == 1:
        f_cadastroProduto()
    elif opcaoMenu == 2:
        f_buscaProdutos(0)
    elif opcaoMenu == 3:
        idProduto = int(input("Digite algum Id específico de produtos: "))
        f_buscaProdutos(idProduto)
    elif opcaoMenu == 4:
        f_novaCompra()

    if opcaoMenu != 5:
        print("=====================================================")
        opcaoContinue =input("= Deseja mais alguma coisa?(S,N)     =")

        if opcaoContinue == 'S' or opcaoContinue == 's':
            abreMenu()

abreMenu()

print("============================================================")
print("=              Obrigado pela preferência!                  =")
print("============================================================")