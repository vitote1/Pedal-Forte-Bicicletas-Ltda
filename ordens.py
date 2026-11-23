from mps import HORIZONTE
from persistencia import carregar_dados, salvar_dados
from utils import validar_entrada_texto

ARQUIVO = "ordens.json"

class Ordem:
    def __init__(self, numero, tipo, codigo_item, quantidade,
                liberar, entregar, status="PLANEJADA"):
        self.numero = numero
        self.tipo = tipo
        self.codigo_item = codigo_item
        self.quantidade = quantidade
        self.liberar = liberar
        self.entregar = entregar
        self.status = status   

    PROXIMO_STATUS = {
        "PLANEJADA": "FIRME",
        "FIRME": "LIBERADA",
    }

    def avancar(self):
        self.status = self.PROXIMO_STATUS[self.status]

    @property
    def atrasada(self):
        return self.status == "PLANEJADA" and self.liberar < 1

    @property
    def status_exibicao(self):
        return "ATRASADA" if self.atrasada else self.status

    def transform_dict(self):
        return {
            "numero": self.numero,
            "tipo": self.tipo,
            "codigo_item": self.codigo_item,
            "quantidade": self.quantidade,
            "liberar": self.liberar,
            "entregar": self.entregar,
            "status": self.status,
        }

    @classmethod
    def de_dict(cls, dados):
        return cls(**dados)

class Ordens:
    def __init__(self):
        self._lista = []
        self._proximo = {"OP": 1, "OC": 1}
        self.carregar()

    def carregar(self):
        dados = carregar_dados(ARQUIVO)
        self._proximo = dados.get("proximo", {"OP": 1, "OC": 1})
        self._lista = [Ordem.de_dict(o) for o in dados.get("ordens", [])]

    def salvar(self):
        salvar_dados(ARQUIVO, {
            "proximo": self._proximo,
            "ordens": [o.transform_dict() for o in self._lista],
        })

    def todas(self):
        return list(self._lista)

    def criar(self, tipo, codigo_item, quantidade, liberar, entregar):
        numero = f"{tipo}-{self._proximo[tipo]:04d}"
        self._proximo[tipo] += 1
        ordem = Ordem(numero, tipo, codigo_item, quantidade,
                      liberar, entregar)
        self._lista.append(ordem)
        return ordem

    def apagar_planejadas(self):
        self._lista = [o for o in self._lista if o.status != "PLANEJADA"]

    def abertas_do_item(self, codigo):
        return [o for o in self._lista
                if o.codigo_item == codigo and o.status != "ENCERRADA"]

    def recebimentos_programados(self, codigo):
        recebimentos = [0] * HORIZONTE
        for ordem in self.abertas_do_item(codigo):
            dentro = 1 <= ordem.entregar <= HORIZONTE
            if ordem.status in ("FIRME", "LIBERADA") and dentro:
                recebimentos[ordem.entregar - 1] += ordem.quantidade
        return recebimentos

    def buscar(self, numero):
        for ordem in self._lista:
            if ordem.numero == numero:
                return ordem
        return None

class GestaoOrdens:

    def __init__(self, ordens, cadastro_itens, estrutura, estoque):
        self._ordens = ordens
        self._itens = cadastro_itens
        self._estrutura = estrutura
        self._estoque = estoque

    def listar(self):
        ordens = self._ordens.todas()
        if not ordens:
            print("Nenhuma ordem. Execute o MRP primeiro.")
            return

        print(f"\n{'Ordem':<9} {'Tipo':<5} {'Item':<8} {'Qtde':>8} "
              f"{'Liberar':>8} {'Entregar':>9}  Status")
        for o in ordens:
            print(f"{o.numero:<9} {o.tipo:<5} {o.codigo_item:<8} "
                  f"{o.quantidade:>8g} {'S' + str(o.liberar):>8} "
                  f"{'S' + str(o.entregar):>9}  {o.status_exibicao}")
        excecoes = sum(1 for o in ordens if o.atrasada)
        if excecoes:
            print(f"\n{excecoes} mensagens de exceção: ordens com "
                  "liberação antes da semana 1.")

    def _avancar(self, status_atual, status_novo):
        numero = validar_entrada_texto("Número da ordem: ").upper()
        ordem = self._ordens.buscar(numero)
        if ordem is None:
            print("ERRO: ordem não encontrada.")
            return
        if ordem.status != status_atual:
            print(f"ERRO: a ordem está {ordem.status}; só é possível "
                  f"mudar para {status_novo} a partir de {status_atual}.")
            return
        ordem.avancar()
        self._ordens.salvar()
        print(f"{ordem.numero} agora está {ordem.status}.")

    def firmar(self):
        self._avancar("PLANEJADA", "FIRME")

    def liberar(self):
        self._avancar("FIRME", "LIBERADA")

    def apontar(self):
        numero = validar_entrada_texto("Número da OP: ").upper()
        ordem = self._ordens.buscar(numero)
        if ordem is None:
            print("ERRO: ordem não encontrada.")
            return
        if ordem.tipo != "OP":
            print("ERRO: só OP pode ser apontada. Use o recebimento da OC.")
            return
        if ordem.status != "LIBERADA":
            print(f"ERRO: a OP está {ordem.status}; só é possível "
                  "apontar uma OP LIBERADA.")
            return

        componentes = self._estrutura.componentes(ordem.codigo_item)
        faltas = []
        for filho, qtd in componentes.items():
            necessario = qtd * ordem.quantidade
            saldo = self._estoque.saldo(filho)
            if saldo < necessario:
                faltas.append(f"{filho}: precisa {necessario:g}, "
                              f"saldo {saldo:g}")
        if faltas:
            print("ERRO: apontamento rejeitado, faltam componentes:")
            for falta in faltas:
                print(f"  - {falta}")
            return

        documento = f"{ordem.numero} ({ordem.codigo_item})"
        for filho, qtd in componentes.items():
            self._estoque.registrar(
                filho, "SAIDA", qtd * ordem.quantidade, documento)
        self._estoque.registrar(
            ordem.codigo_item, "ENTRADA", ordem.quantidade, documento)

        ordem.status = "ENCERRADA"
        self._ordens.salvar()
        print(f"{ordem.numero} apontada e encerrada. "
              f"{ordem.quantidade:g} un de {ordem.codigo_item} "
              "entraram no estoque.")

    def receber(self):
        numero = validar_entrada_texto("Número da OC: ").upper()
        ordem = self._ordens.buscar(numero)
        if ordem is None or ordem.tipo != "OC":
            print("ERRO: OC não encontrada.")
            return
        if ordem.status != "LIBERADA":
            print(f"ERRO: a OC está {ordem.status}; só é possível "
                  "receber uma OC LIBERADA.")
            return

        self._estoque.registrar(
            ordem.codigo_item, "ENTRADA", ordem.quantidade, ordem.numero)
        ordem.status = "ENCERRADA"
        self._ordens.salvar()
        print(f"{ordem.numero} recebida e encerrada.")