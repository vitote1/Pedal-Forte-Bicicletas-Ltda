import os

import matplotlib.pyplot as plt

from mps import HORIZONTE
from persistencia import PASTA_DADOS
from utils import validar_entrada_texto

PASTA_GRAFICOS = os.path.join(PASTA_DADOS, "graficos")
SEMANAS = list(range(1, HORIZONTE + 1))


def _salvar_e_mostrar(figura, nome):
    os.makedirs(PASTA_GRAFICOS, exist_ok=True)
    caminho = os.path.join(PASTA_GRAFICOS, nome)
    figura.tight_layout()
    figura.savefig(caminho, dpi=120)
    print(f"Gráfico salvo em: {caminho}")
    plt.show()
    plt.close(figura)


class Graficos:

    def __init__(self, cadastro_itens, estoque, mrp, ordens, capacidade):
        self._itens = cadastro_itens
        self._estoque = estoque
        self._mrp = mrp
        self._ordens = ordens
        self._capacidade = capacidade

    def posicao_estoque(self):
        itens = self._itens.todos()
        if not itens:
            print("Nenhum item cadastrado.")
            return
        codigos = [item.codigo for item in itens]
        saldos = [self._estoque.saldo(item.codigo) for item in itens]
        seguranca = [item.estoque_seguranca for item in itens]
        posicoes = range(len(codigos))
        largura = 0.4

        figura, eixo = plt.subplots(figsize=(11, 5))
        eixo.bar([p - largura / 2 for p in posicoes], saldos, largura,
                 label="Saldo atual")
        eixo.bar([p + largura / 2 for p in posicoes], seguranca, largura,
                 label="Estoque de segurança", color="tab:orange")
        eixo.set_xticks(list(posicoes))
        eixo.set_xticklabels(codigos, rotation=45)
        eixo.set_ylabel("Quantidade")
        eixo.set_title("Posição de estoque: saldo x estoque de segurança")
        eixo.legend()
        _salvar_e_mostrar(figura, "posicao_estoque.png")

    def estoque_projetado(self):
        codigo = validar_entrada_texto("Código do item: ").upper()
        item = self._itens.buscar(codigo)
        if item is None:
            print("ERRO: item não encontrado.")
            return
        registro = self._mrp.registro(codigo)
        if registro is None:
            print("ERRO: execute o MRP antes de gerar este gráfico.")
            return

        figura, eixo = plt.subplots(figsize=(9, 5))
        eixo.plot(SEMANAS, registro["ep"], marker="o",
                  label="Estoque projetado")
        eixo.axhline(item.estoque_seguranca, color="tab:red",
                     linestyle="--", label="Estoque de segurança")
        eixo.set_xlabel("Semana")
        eixo.set_ylabel(f"Quantidade ({item.unidade_medida})")
        eixo.set_title(f"Estoque projetado - {item.codigo} "
                       f"{item.descricao}")
        eixo.legend()
        _salvar_e_mostrar(figura, f"estoque_projetado_{codigo}.png")

    def ordens_por_semana(self):
        ordens_op = [0] * HORIZONTE
        ordens_oc = [0] * HORIZONTE
        for ordem in self._ordens.todas():
            if ordem.status == "ENCERRADA":
                continue
            if not 1 <= ordem.entregar <= HORIZONTE:
                continue
            destino = ordens_op if ordem.tipo == "OP" else ordens_oc
            destino[ordem.entregar - 1] += 1

        if not any(ordens_op) and not any(ordens_oc):
            print("Nenhuma ordem em aberto. Execute o MRP primeiro.")
            return

        figura, eixo = plt.subplots(figsize=(9, 5))
        eixo.bar(SEMANAS, ordens_op, label="OP (produção)")
        eixo.bar(SEMANAS, ordens_oc, bottom=ordens_op,
                 label="OC (compra)", color="tab:green")
        eixo.set_xlabel("Semana de entrega")
        eixo.set_ylabel("Número de ordens")
        eixo.set_title("Ordens de produção e de compra por semana")
        eixo.legend()
        _salvar_e_mostrar(figura, "ordens_por_semana.png")

    def carga_capacidade(self):
        codigo = validar_entrada_texto(
            "Código do centro (ex.: CT-03): ").upper()
        centro = self._capacidade.centro(codigo)
        if centro is None:
            print("ERRO: centro não encontrado.")
            return

        carga = self._capacidade.carga_semanal(codigo)
        cores = ["tab:red" if horas > centro.capacidade else "tab:blue"
                 for horas in carga]

        figura, eixo = plt.subplots(figsize=(9, 5))
        eixo.bar(SEMANAS, carga, color=cores)
        eixo.axhline(centro.capacidade, color="black", linestyle="--",
                     label=f"Capacidade ({centro.capacidade:g} h/sem)")
        eixo.set_xlabel("Semana")
        eixo.set_ylabel("Horas")
        eixo.set_title(f"Carga x capacidade - {centro.codigo} "
                       f"{centro.descricao} (vermelho = sobrecarga)")
        eixo.legend()
        _salvar_e_mostrar(figura, f"carga_capacidade_{codigo}.png")