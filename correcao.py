import mysql.connector

conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='minuano',
    database='demodb'
)
cursor = conn.cursor()
def CadastrarProduto():
    try:
        produto = {}
        produto["nome"] = input("Digite o nome do produto: ")
        produto["valor"] = input("Digite o valor do produto: ")
        produto["cod_barras"] = input("Digite o código de barras do produto: ")
        produto["estoque"] = input("Digite o estoque do produto: ")
        cursor.execute("insert into produtos (nome, valor, cod_barras, estoque) "
                       "values (%s, %s, %s, %s)", (produto["nome"], produto["valor"],
                                                   produto["cod_barras"], produto["estoque"]))
        conn.commit()
        print("Produto cadastrado com sucesso...")
    except:
        print("Infelizmente tivemos um erro no cadastro do produto. Tente novamente mais tarde...")

def VisualizarProdutos():
    try:
        cursor.execute("select id, nome, valor, cod_barras, estoque from produtos")
        print("Produtos:")
        for produto in cursor.fetchall():
            print(produto)
        print("\n")
        input("digite qualquer tecla para continuar...")
    except:
        print("Infelizmente tivemos problemas ao selecionar produtos. Tente novamente mais tarde...")

def VisualizarProdutoEspecifico():
    try:
        idProduto = input("Digite um ID de produto: ")
        cursor.execute("select id, nome, valor, cod_barras, estoque from produtos where id = %s",
                       (idProduto,))
        for produto in cursor.fetchall():
            print(produto)
        print("\n")
        input("digite qualquer tecla para continuar...")
    except:
        print("Infelizmente não foi possível selecionar um produto. Tente novamente mais tarde...")

def RegistrarVenda():
    nomeCliente = input("Digite o nome do cliente: ")
    idProduto = input("Digite o ID produto que será vendido: ")
    quantidade = float(input("Digite a quantidade do produto que será vendida: "))

    estoqueProduto = 0
    cursor.execute("select estoque from produtos where id = %s", (idProduto,))
    for produto in cursor.fetchall():
        estoqueProduto = float(produto[0])

    if estoqueProduto < quantidade:
        print("Venda não pode ser efetivada. Não há estoque suficiente...")
    else:
        novoEstoque = estoqueProduto - quantidade
        cursor.execute("insert into venda (NomeCliente, IdProduto, Quantidade, DataHoraVenda) "
                       "values (%s, %s, %s, now())", (nomeCliente, idProduto, quantidade))
        cursor.execute("update produtos set estoque = %s where id = %s",
                       (novoEstoque, idProduto))
        conn.commit()
        print("Venda registrada com sucesso")

opcao = 0
while opcao >= 0 and opcao < 5:
    if opcao == 0:
        print("Escolha uma opção:\n"
              "1) Cadastrar Novo Produto\n"
              "2) Visualizar todos os produtos\n"
              "3) Visualizar um produto específico\n"
              "4) Registrar Venda\n"
              "5) Sair")
        digitacaoInvalida = True
        while digitacaoInvalida:
            try:
                opcao = int(input("Digite um comando: "))
                if opcao == 0:
                    print("comando inválido...")
                else:
                    digitacaoInvalida = False
            except Exception as e:
                print("comando inválido...")
    elif opcao == 1:
        print("Opção selecionada: 1) Cadastrar Novo Produto")
        CadastrarProduto()
        opcao = 0
    elif opcao == 2:
        print("Opção selecionada: 2) Visualizar todos os produtos")
        VisualizarProdutos()
        opcao = 0
    elif opcao == 3:
        print("Opção selecionada: 3) Visualizar um produto específico")
        VisualizarProdutoEspecifico()
        opcao = 0
    elif opcao == 4:
        print("Opção selecionada: 4) Registrar Venda")
        RegistrarVenda()
        opcao = 0