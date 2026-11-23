from persistencia import salvar_dados, carregar_dados
from utils import validar_codigo, validar_entrada_texto, validar_entrada_float, validar_entrada_int, perguntar_modificacao

ARQUIVO = "itens.json"

class Item:
    def __init__(self, codigo, descricao, unidade_medida, custo_unitario, lead_time, estoque_seguranca, lote_minimo):
        self.codigo = codigo
        self.descricao = descricao
        self.unidade_medida = unidade_medida
        self.custo_unitario = custo_unitario
        self.lead_time = lead_time
        self.estoque_seguranca = estoque_seguranca
        self.lote_minimo = lote_minimo

    @property
    def tipo(self):
        return self.codigo[:2]

    @property
    def fabricado(self):
        return self.tipo in ("SA", "PA")

    def transform_dict(self):
        return {
            "codigo": self.codigo,
            "descricao": self.descricao,
            "unidade_medida": self.unidade_medida,
            "custo_unitario": self.custo_unitario,
            "lead_time": self.lead_time,
            "estoque_seguranca": self.estoque_seguranca,
            "lote_minimo": self.lote_minimo,
        }

    def __str__(self):
        return (f"{self.codigo} {self.descricao} {self.unidade_medida}")

    @classmethod
    def de_dict(cls, dados):
        return cls(**dados)

class CadastrarItem:
    def __init__(self):
        self._itens = {}
        self.carregar()

    def carregar(self):
        dados = carregar_dados(ARQUIVO)
        self._itens = {
            codigo: Item.de_dict(campos) 
            for codigo, campos in dados.items()
        }

    def salvar(self):
        dados = {
            codigo: item.transform_dict() 
            for codigo, item in self._itens.items()
        }
        salvar_dados(ARQUIVO, dados)

    def buscar(self, codigo):
        return self._itens.get(codigo)

    def cadastrar(self):
        codigo = validar_entrada_texto("Código (ex.: PA-001): ").upper()

        if not validar_codigo(codigo):
            print("ERRO: formato inválido. Use Tipo-Número (ex.: PA-001).")
            return
        if codigo in self._itens:
            print("ERRO: já existe um item com esse código.")
            return

        item = Item(
            codigo=codigo,
            descricao=validar_entrada_texto("Descrição: "),
            unidade_medida=validar_entrada_texto("Unidade de medida (un, m, L, kg...): "),
            custo_unitario=validar_entrada_float("Custo unitário (R$): "),
            lead_time=validar_entrada_int("Lead time (semanas): "),
            estoque_seguranca=validar_entrada_float("Estoque de segurança: "),
            lote_minimo=validar_entrada_float("Lote mínimo: ", minimo=1),
        )
        self._itens[codigo] = item
        self.salvar()
        print(f"Item {codigo} cadastrado com sucesso.")

    def listar(self):
        if not self._itens:
            print("Nenhum item cadastrado.")
            return
        print(f"{'Código':<8} {'Descrição':<28} {'Tipo':<5} {'Un':<4} "
              f"{'Custo':>9} {'LT':>3} {'ES':>7} {'Lote':>7}")
        print("-" * 78)
        for codigo in sorted(self._itens):
            item = self._itens[codigo]
            print(f"{item.codigo:<8} {item.descricao:<28} {item.tipo:<5} "
                  f"{item.unidade_medida:<4} {item.custo_unitario:>9.2f} "
                  f"{item.lead_time:>3} {item.estoque_seguranca:>7.1f} "
                  f"{item.lote_minimo:>7.1f}")

    def alterar(self):
        codigo = validar_entrada_texto("Código do item que deseja modificar: ").upper()
        item = self.buscar(codigo)

        if item is None:
            print("ERRO: código não existente")
            return

        print(f"Alterando item: {item}")

        if perguntar_modificacao("descrição"):
            item.descricao = validar_entrada_texto(
                f"Descrição [{item.descricao}]: ")

        if perguntar_modificacao("unidade de medida"):
            item.unidade_medida = validar_entrada_texto(
                f"Unidade [{item.unidade_medida}]: ")

        if perguntar_modificacao("custo unitário"):
            item.custo_unitario = validar_entrada_float(
                f"Custo unitário [{item.custo_unitario}]: ")

        if perguntar_modificacao("lead time"):
            item.lead_time = validar_entrada_int(
                f"Lead time [{item.lead_time}]: ")

        if perguntar_modificacao("estoque de segurança"):
            item.estoque_seguranca = validar_entrada_float(
                f"Estoque de segurança [{item.estoque_seguranca}]: ")

        if perguntar_modificacao("lote mínimo"):
            item.lote_minimo = validar_entrada_float(
                f"Lote mínimo [{item.lote_minimo}]: ", minimo=1)

        self.salvar()
        print(f"Item {codigo} alterado com sucesso.")

    def todos(self):
        return [self._itens[codigo] for codigo in sorted(self._itens)]

