
from estoque import Estoque
from estrutura import Estrutura
from itens import CadastrarItem
from menu import menu_principal
from mps import PlanoMestre
from mrp import MRP
from ordens import Ordens, GestaoOrdens
from capacidade import Capacidade
from custos import CustoPadrao
from relatorios import Relatorios
from graficos import Graficos

def main():
    cadastro_itens = CadastrarItem()
    estrutura = Estrutura(cadastro_itens)
    estoque = Estoque(cadastro_itens)
    mps = PlanoMestre(cadastro_itens)
    ordens = Ordens()
    mrp = MRP(cadastro_itens, estrutura, estoque, mps, ordens)
    gestao = GestaoOrdens(ordens, cadastro_itens, estrutura, estoque)
    capacidade = Capacidade(cadastro_itens, ordens)
    custos = CustoPadrao(cadastro_itens, estrutura, capacidade)
    relatorios = Relatorios(cadastro_itens, estoque, ordens)
    graficos = Graficos(cadastro_itens, estoque, mrp, ordens, capacidade)
    menu_principal(cadastro_itens, estrutura, estoque, mps, mrp, gestao, capacidade, custos, relatorios, graficos)


if __name__ == "__main__":
    main()