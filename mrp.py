"""Cálculo MRP (RF08, RF09)."""
from mps import HORIZONTE
from utils import validar_entrada_texto

LINHAS = (
    ("Necessidade bruta", "nb"),
    ("Receb. programados", "rp"),
    ("Estoque projetado", "ep"),
    ("Necessidade liquida", "nl"),
    ("Receb. planejados", "rpl"),
    ("Liberacao planejada", "lib"),
)


def calcular_registro(nb, rp, estoque_inicial, item):
    registro = {"nb": list(nb), "rp": list(rp), "ep": [], "nl": [],
                "rpl": [], "lib": [0] * HORIZONTE}
    planejadas = []
    ep_anterior = estoque_inicial

    for indice in range(HORIZONTE):
        semana = indice + 1
        nl = max(0, round(nb[indice] + item.estoque_seguranca
                          - (ep_anterior + rp[indice]), 3))
        rpl = max(nl, item.lote_minimo) if nl > 0 else 0
        ep_anterior = round(ep_anterior + rp[indice] + rpl - nb[indice], 3)

        registro["nl"].append(nl)
        registro["rpl"].append(rpl)
        registro["ep"].append(ep_anterior)

        if rpl > 0:
            liberar = semana - item.lead_time 
            planejadas.append((rpl, liberar, semana))
            if liberar >= 1:
                registro["lib"][liberar - 1] = rpl
    return registro, planejadas

class MRP:
    def __init__(self, cadastro_itens, estrutura, estoque, mps, ordens):
        self._itens = cadastro_itens
        self._estrutura = estrutura
        self._estoque = estoque
        self._mps = mps
        self._ordens = ordens
        self._registros = {}

    def executar(self):
        self._ordens.apagar_planejadas() 
        itens = self._itens.todos()
        nb = {item.codigo: [0] * HORIZONTE for item in itens}
        for codigo in self._mps.produtos():
            if codigo in nb:
                nb[codigo] = list(self._mps.demanda(codigo))

        self._registros = {}
        for tipo in ("PA", "SA", "MP"): 
            for item in itens:
                if item.tipo == tipo:
                    self._processar_item(item, nb)
        self._ordens.salvar()

        planejadas = [o for o in self._ordens.todas()
                      if o.status == "PLANEJADA"]
        atrasadas = [o for o in planejadas if o.atrasada]
        print(f"MRP executado: {len(planejadas)} ordens planejadas.")
        if atrasadas:
            print(f"{len(atrasadas)} mensagens de exceção: ordens com "
                  "liberação antes da semana 1.")

    def _processar_item(self, item, nb):
        registro, planejadas = calcular_registro(
            nb[item.codigo],
            self._ordens.recebimentos_programados(item.codigo),
            self._estoque.saldo(item.codigo),
            item,
        )
        tipo_ordem = "OP" if item.fabricado else "OC"
        for quantidade, liberar, entregar in planejadas:
            self._ordens.criar(
                tipo_ordem, item.codigo, quantidade, liberar, entregar)
        self._registros[item.codigo] = registro
        self._propagar(item.codigo, nb)

    def _propagar(self, codigo_pai, nb):
        componentes = self._estrutura.componentes(codigo_pai)
        for ordem in self._ordens.abertas_do_item(codigo_pai):
            semana = max(1, ordem.liberar)
            if semana > HORIZONTE:
                continue
            for filho, qtd_por_unidade in componentes.items():
                nb[filho][semana - 1] += ordem.quantidade * qtd_por_unidade

    def exibir_registro(self):
        if not self._registros:
            print("ERRO: execute o MRP antes de consultar um registro.")
            return
        codigo = validar_entrada_texto("Código do item: ").upper()
        item = self._itens.buscar(codigo)
        if item is None:
            print("ERRO: item não encontrado.")
            return
        registro = self._registros.get(codigo)
        if registro is None:
            print("ERRO: item novo, execute o MRP novamente.")
            return

        print(f"\nREGISTRO MRP - {item.codigo} {item.descricao}")
        print(f"Lead time: {item.lead_time} sem | "
              f"Est. seguranca: {item.estoque_seguranca:g} | "
              f"Lote min.: {item.lote_minimo:g} | "
              f"Estoque: {self._estoque.saldo(codigo):g}")
        semanas = "".join(f"{s:>6}" for s in range(1, HORIZONTE + 1))
        print(f"{'Semana':<21}{semanas}")
        for rotulo, chave in LINHAS:
            valores = "".join(f"{v:>6g}" for v in registro[chave])
            print(f"{rotulo:<21}{valores}")

    def registro(self, codigo):
        return self._registros.get(codigo)