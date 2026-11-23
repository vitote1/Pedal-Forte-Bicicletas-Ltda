
from estoque import Estoque
from estrutura import Estrutura
from itens import CadastrarItem
from menu import menu_principal
from mps import PlanoMestre
from mrp import MRP
from ordens import Ordens, GestaoOrdens

def main():
    cadastro_itens = CadastrarItem()
    estrutura = Estrutura(cadastro_itens)
    estoque = Estoque(cadastro_itens)
    mps = PlanoMestre(cadastro_itens)
    ordens = Ordens()
    mrp = MRP(cadastro_itens, estrutura, estoque, mps, ordens)
    gestao = GestaoOrdens(ordens, cadastro_itens, estrutura, estoque)
    menu_principal(cadastro_itens, estrutura, estoque, mps, mrp, gestao)


if __name__ == "__main__":
    main()