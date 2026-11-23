

def menu_principal(cadastro_itens, estrutura, estoque, mps, mrp, gestao):
    while True:
        menu_geral()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_cadastros(cadastro_itens, estrutura)
        elif opcao == "2":
            menu_estoque(estoque)
        elif opcao == "3":
            menu_mps(mps)
        elif opcao == "4":
            menu_mrp(mrp)
        elif opcao == "5":
            menu_ordens(gestao)
        elif opcao in ("6", "7", "8"):
            print("Em desenvolvimento.")
        elif opcao == "0":
            print("Encerrando o sistema.")
            return
        else:
            print("ERRO: opção inválida.")

def menu_geral():
    print("=" * 50)
    print("MRP II - PEDAL FORTE BICICLETAS")
    print("=" * 50)
    print("1. Cadastros (itens, estrutura, centros, roteiros)")
    print("2. Estoque (movimentar, saldo, kardex)")
    print("3. Plano Mestre de Produção (MPS)")
    print("4. Executar MRP")
    print("5. Ordens de produção e de compra")
    print("6. Carga x capacidade (CRP)")
    print("7. Custo padrão dos produtos")
    print("8. Relatórios (exportar CSV)")
    print("0. Sair")
    print("-" * 50)

def menu_itens(cadastro):
    while True:
        print("\n--- ITENS ---")
        print("1. Cadastrar")
        print("2. Listar")
        print("3. Alterar")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastro.cadastrar()
        elif opcao == "2":
            cadastro.listar()
        elif opcao == "3":
            cadastro.alterar()
        elif opcao == "0":
            return
        else:
            print("ERRO: opção inválida.") 

def menu_cadastros(cadastro_itens, estrutura):
    while True:
        print("\n--- CADASTROS ---")
        print("1. Itens")
        print("2. Estrutura de produto (BOM)")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_itens(cadastro_itens)
        elif opcao == "2":
            menu_estrutura(estrutura)
        elif opcao == "0":
            return
        else:
            print("ERRO: opção inválida.")

def menu_estrutura(estrutura):
    while True:
        print("\n--- ESTRUTURA DE PRODUTO ---")
        print("1. Adicionar componente")
        print("2. Exibir estrutura (explosão)")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            estrutura.adicionar_componente()
        elif opcao == "2":
            estrutura.exibir()
        elif opcao == "0":
            return
        else:
            print("ERRO: opção inválida.")

def menu_estoque(estoque):
    while True:
        print("\n--- ESTOQUE ---")
        print("1. Movimentar (entrada, saída, ajuste)")
        print("2. Consultar saldo")
        print("3. Kardex")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            estoque.movimentar()
        elif opcao == "2":
            estoque.consultar_saldo()
        elif opcao == "3":
            estoque.kardex()
        elif opcao == "0":
            return
        else:
            print("ERRO: opção inválida.")

def menu_mps(mps):
    while True:
        print("\n--- PLANO MESTRE DE PRODUÇÃO ---")
        print("1. Cadastrar / alterar demanda")
        print("2. Exibir MPS")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            mps.cadastrar()
        elif opcao == "2":
            mps.exibir()
        elif opcao == "0":
            return
        else:
            print("ERRO: opção inválida.")


def menu_mrp(mrp):
    while True:
        print("\n--- MRP ---")
        print("1. Executar MRP")
        print("2. Exibir registro de um item")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            mrp.executar()
        elif opcao == "2":
            mrp.exibir_registro()
        elif opcao == "0":
            return
        else:
            print("ERRO: opção inválida.")

def menu_mrp(mrp):
    while True:
        print("\n--- MRP ---")
        print("1. Executar MRP")
        print("2. Exibir registro de um item")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            mrp.executar()
        elif opcao == "2":
            mrp.exibir_registro()
        elif opcao == "0":
            return
        else:
            print("ERRO: opção inválida.")

def menu_ordens(gestao):
    while True:
        print("\n--- ORDENS ---")
        print("1. Listar ordens")
        print("2. Firmar ordem")
        print("3. Liberar ordem")
        print("4. Apontar produção (OP)")
        print("5. Receber compra (OC)")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            gestao.listar()
        elif opcao == "2":
            gestao.firmar()
        elif opcao == "3":
            gestao.liberar()
        elif opcao == "4":
            gestao.apontar()
        elif opcao == "5":
            gestao.receber()
        elif opcao == "0":
            return
        else:
            print("ERRO: opção inválida.")