from datetime import date

from persistencia import (adicionar_csv, carregar_csv, carregar_dados,
                          salvar_dados)
from utils import validar_entrada_float, validar_entrada_texto

ARQUIVO_SALDOS = "estoque.json"
ARQUIVO_MOVIMENTOS = "movimentos.csv"
CAMPOS_MOVIMENTO = ("data", "codigo", "tipo", "quantidade", "saldo",
                    "documento")
TIPOS = {"E": "ENTRADA", "S": "SAIDA", "A": "AJUSTE"}


class Estoque:

    def __init__(self, cadastro_itens):
        self._itens = cadastro_itens
        self._saldos = {}
        self._movimentos = []
        self.carregar()

    def carregar(self):
        self._saldos = carregar_dados(ARQUIVO_SALDOS)
        self._movimentos = [
            {
                "data": linha["data"],
                "codigo": linha["codigo"],
                "tipo": linha["tipo"],
                "quantidade": float(linha["quantidade"]),
                "saldo": float(linha["saldo"]),
                "documento": linha["documento"],
            }
            for linha in carregar_csv(ARQUIVO_MOVIMENTOS)
        ]

    def saldo(self, codigo):
        return self._saldos.get(codigo, 0.0)

    def movimentos_do_item(self, codigo):
        return [mov for mov in self._movimentos if mov["codigo"] == codigo]

    def registrar(self, codigo, tipo, quantidade, documento):

        item = self._itens.buscar(codigo)
        if item is None:
            return f"item {codigo} não cadastrado"
        if tipo != "AJUSTE" and quantidade <= 0:
            return "a quantidade deve ser maior que zero"

        variacao = -quantidade if tipo == "SAIDA" else quantidade
        saldo_atual = self.saldo(codigo)
        novo_saldo = round(saldo_atual + variacao, 3)

        if novo_saldo < 0:  
            return (f"saldo insuficiente (saldo atual: "
                    f"{saldo_atual:g} {item.unidade_medida})")

        movimento = {
            "data": date.today().strftime("%d/%m/%Y"),
            "codigo": codigo,
            "tipo": tipo,
            "quantidade": variacao,
            "saldo": novo_saldo,
            "documento": documento,
        }
        self._movimentos.append(movimento)
        self._saldos[codigo] = novo_saldo
        adicionar_csv(ARQUIVO_MOVIMENTOS, CAMPOS_MOVIMENTO, movimento)
        salvar_dados(ARQUIVO_SALDOS, self._saldos)
        return None

    def movimentar(self):
        codigo = validar_entrada_texto("Código do item: ").upper()
        item = self._itens.buscar(codigo)
        if item is None:
            print("ERRO: item não encontrado.")
            return

        saldo_atual = self.saldo(codigo)
        print(f"Saldo atual: {saldo_atual:g} {item.unidade_medida}")
        tipo = self._ler_tipo()

        if tipo == "AJUSTE":
            contado = validar_entrada_float("Saldo contado: ")
            quantidade = round(contado - saldo_atual, 3)
            if quantidade == 0:
                print("ERRO: o saldo contado é igual ao atual.")
                return
            documento = validar_entrada_texto("Motivo do ajuste: ")
        else:
            quantidade = validar_entrada_float(
                "Quantidade: ", minimo=0.001)
            documento = validar_entrada_texto("Documento: ")

        erro = self.registrar(codigo, tipo, quantidade, documento)
        if erro:
            print(f"ERRO: {erro}. Operação cancelada.")
            return
        print(f"Movimento registrado. Novo saldo: "
              f"{self.saldo(codigo):g} {item.unidade_medida}")
        self._alertar_seguranca(item)

    @staticmethod
    def _ler_tipo():
        while True:
            letra = input("[E] - Entrada \n[S] - Saida \n[A] - Ajuste: ").strip().upper()
            if letra in TIPOS:
                return TIPOS[letra]
            print("ERRO: digite E, S ou A.")

    def _alertar_seguranca(self, item):
        saldo = self.saldo(item.codigo)
        if saldo < item.estoque_seguranca:
            print(f"ALERTA: saldo ({saldo:g} {item.unidade_medida}) abaixo "
                  f"do estoque de segurança "
                  f"({item.estoque_seguranca:g} {item.unidade_medida}).")

    def consultar_saldo(self):
        codigo = validar_entrada_texto("Código do item: ").upper()
        item = self._itens.buscar(codigo)
        if item is None:
            print("ERRO: item não encontrado.")
            return
        print(f"{item.codigo} {item.descricao}: "
              f"{self.saldo(codigo):g} {item.unidade_medida}")
        self._alertar_seguranca(item)

    def kardex(self):
        codigo = validar_entrada_texto("Código do item: ").upper()
        item = self._itens.buscar(codigo)
        if item is None:
            print("ERRO: item não encontrado.")
            return

        print(f"\nKARDEX - {item.codigo} {item.descricao} "
              f"({item.unidade_medida})")
        movimentos = self.movimentos_do_item(codigo)
        if not movimentos:
            print("Nenhuma movimentação registrada.")
            return

        print(f"{'Data':<11} {'Tipo':<8} {'Qtde':>8} {'Saldo':>8}  "
              "Documento")
        for mov in movimentos:
            print(f"{mov['data']:<11} {mov['tipo']:<8} "
                  f"{mov['quantidade']:>+8g} {mov['saldo']:>8g}  "
                  f"{mov['documento']}")
        self._alertar_seguranca(item)