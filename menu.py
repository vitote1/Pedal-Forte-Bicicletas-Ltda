

def menu_principal(cadastro_itens, estrutura, estoque, mps, mrp, gestao, capacidade, custos, relatorios, graficos):
    while True:
        menu_geral()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_cadastros(cadastro_itens, estrutura, capacidade)
        elif opcao == "2":
            menu_estoque(estoque)
        elif opcao == "3":
            menu_mps(mps)
        elif opcao == "4":
            menu_mrp(mrp)
        elif opcao == "5":
            menu_ordens(gestao)
        elif opcao == "6":
            capacidade.exibir_crp()
        elif opcao == "7":
            custos.exibir()
        elif opcao == "8":
            menu_relatorios(relatorios, graficos)
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

def menu_cadastros(cadastro_itens, estrutura, capacidade):
    while True:
        print("\n--- CADASTROS ---")
        print("1. Itens")
        print("2. Estrutura de produto (BOM)")
        print("3. Centros e roteiros")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_itens(cadastro_itens)
        elif opcao == "2":
            menu_estrutura(estrutura)
        elif opcao == "3":
            menu_capacidade(capacidade)
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

def menu_capacidade(capacidade):
    while True:
        print("\n--- CENTROS E ROTEIROS ---")
        print("1. Cadastrar centro de trabalho")
        print("2. Listar centros")
        print("3. Definir roteiro de um item")
        print("4. Listar roteiros")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            capacidade.cadastrar_centro()
        elif opcao == "2":
            capacidade.listar_centros()
        elif opcao == "3":
            capacidade.definir_roteiro()
        elif opcao == "4":
            capacidade.listar_roteiros()
        elif opcao == "0":
            return
        else:
            print("ERRO: opção inválida.")


def menu_relatorios(relatorios, graficos):
    while True:
        print("\n--- RELATÓRIOS ---")
        print("1. Exportar posição de estoque (CSV)")
        print("2. Exportar lista de ordens (CSV)")
        print("3. Gráfico: posição de estoque")
        print("4. Gráfico: estoque projetado de um item")
        print("5. Gráfico: ordens por semana")
        print("6. Gráfico: carga x capacidade")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            relatorios.exportar_estoque()
        elif opcao == "2":
            relatorios.exportar_ordens()
        elif opcao == "3":
            graficos.posicao_estoque()
        elif opcao == "4":
            graficos.estoque_projetado()
        elif opcao == "5":
            graficos.ordens_por_semana()
        elif opcao == "6":
            graficos.carga_capacidade()
        elif opcao == "0":
            return
        else:
            print("ERRO: opção inválida.")