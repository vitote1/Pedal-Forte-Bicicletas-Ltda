from utils import validar_entrada_texto


def moeda(valor):
    return f"{valor:.2f}".replace(".", ",")


class CustoPadrao:

    def __init__(self, cadastro_itens, estrutura, capacidade):
        self._itens = cadastro_itens
        self._estrutura = estrutura
        self._capacidade = capacidade

    def mao_de_obra(self, codigo):
        roteiro = self._capacidade.roteiro(codigo)
        if roteiro is None:
            return None
        centro = self._capacidade.centro(roteiro.centro)
        if centro is None:
            return None
        valor = round(roteiro.tempo * centro.custo_hora, 2)
        return centro, roteiro.tempo, valor

    def custo(self, codigo):
        item = self._itens.buscar(codigo)
        if not item.fabricado: 
            return item.custo_unitario

        total = 0.0
        for filho, quantidade in self._estrutura.componentes(codigo).items():
            total += quantidade * self.custo(filho)  

        mao_obra = self.mao_de_obra(codigo)
        if mao_obra is not None:
            total += mao_obra[2]
        return round(total, 2)

    def exibir(self):
        codigo = validar_entrada_texto("Código do produto: ").upper()
        item = self._itens.buscar(codigo)
        if item is None:
            print("ERRO: item não encontrado.")
            return
        if not item.fabricado:
            print(f"{codigo} é matéria-prima: custo unitário "
                  f"R$ {moeda(item.custo_unitario)}.")
            return
        componentes = self._estrutura.componentes(codigo)
        if not componentes:
            print(f"ERRO: {codigo} não possui estrutura cadastrada.")
            return

        print(f"\nCUSTO PADRAO - {item.codigo} {item.descricao}")
        print(f"{'Item':<8} {'Descricao':<28} {'Qtde':>6} "
              f"{'Custo un.':>10} {'Total':>10}")
        for filho, quantidade in componentes.items():
            sub = self._itens.buscar(filho)
            unitario = self.custo(filho)
            print(f"{filho:<8} {sub.descricao:<28} {quantidade:>6g} "
                  f"{moeda(unitario):>10} {moeda(quantidade * unitario):>10}")

        mao_obra = self.mao_de_obra(codigo)
        if mao_obra is None:
            print("AVISO: item sem roteiro; mão de obra não incluída.")
        else:
            centro, tempo, valor = mao_obra
            rotulo = f"Mao de obra {centro.codigo}"
            print(f"{rotulo:<37} {tempo:>6g} h "
                  f"{moeda(centro.custo_hora):>8} {moeda(valor):>10}")

        print("-" * 66)
        print(f"{'CUSTO PADRAO TOTAL':<48} R$ {moeda(self.custo(codigo)):>10}")