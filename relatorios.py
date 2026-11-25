import csv
import os
from datetime import date

from persistencia import PASTA_DADOS


def _caminho(prefixo):
    os.makedirs(PASTA_DADOS, exist_ok=True)
    nome = f"{prefixo}_{date.today().isoformat()}.csv"
    return os.path.join(PASTA_DADOS, nome)


def _gravar(caminho, cabecalho, linhas):
    with open(caminho, "w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(cabecalho)
        escritor.writerows(linhas)


class Relatorios:

    def __init__(self, cadastro_itens, estoque, ordens):
        self._itens = cadastro_itens
        self._estoque = estoque
        self._ordens = ordens

    def exportar_estoque(self):
        linhas = []
        for item in self._itens.todos():
            saldo = self._estoque.saldo(item.codigo)
            situacao = ("ABAIXO DA SEGURANCA"
                        if saldo < item.estoque_seguranca else "OK")
            linhas.append([item.codigo, item.descricao, item.tipo,
                           item.unidade_medida, saldo,
                           item.estoque_seguranca, situacao])
        caminho = _caminho("posicao_estoque")
        _gravar(caminho, ["codigo", "descricao", "tipo", "unidade",
                          "saldo", "estoque_seguranca", "situacao"], linhas)
        print(f"Posição de estoque exportada: {caminho}")

    def exportar_ordens(self):
        ordens = self._ordens.todas()
        if not ordens:
            print("Nenhuma ordem para exportar. Execute o MRP primeiro.")
            return
        linhas = [[o.numero, o.tipo, o.codigo_item, o.quantidade,
                   o.liberar, o.entregar, o.status_exibicao]
                  for o in ordens]
        caminho = _caminho("ordens")
        _gravar(caminho, ["ordem", "tipo", "item", "quantidade",
                          "liberar_semana", "entregar_semana", "status"],
                linhas)
        print(f"Lista de ordens exportada: {caminho}")