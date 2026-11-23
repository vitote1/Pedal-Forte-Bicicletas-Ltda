
from persistencia import salvar_dados, carregar_dados
from utils import validar_entrada_int, validar_entrada_texto

ARQUIVO = "mps.json"
HORIZONTE = 8


class PlanoMestre:

    def __init__(self, cadastro_itens):
        self._itens = cadastro_itens
        self._demanda = {}
        self.carregar()

    def carregar(self):
        self._demanda = carregar_dados(ARQUIVO)

    def salvar(self):
        salvar_dados(ARQUIVO, self._demanda)

    def demanda(self, codigo):
        return self._demanda.get(codigo, [0] * HORIZONTE)

    def produtos(self):
        return list(self._demanda)

    def _validar_produto(self, codigo):
        item = self._itens.buscar(codigo)
        if item is None:
            return f"item {codigo} não cadastrado"
        if item.tipo != "PA":
            return "o MPS aceita apenas produtos acabados (PA)"
        return None

    def cadastrar(self):
        codigo = validar_entrada_texto("Código do PA: ").upper()
        erro = self._validar_produto(codigo)
        if erro:
            print(f"ERRO: {erro}.")
            return

        atual = self.demanda(codigo)
        nova = []
        for semana in range(1, HORIZONTE + 1):
            valor = validar_entrada_int(
                f"Semana {semana} [{atual[semana - 1]}]: ")
            nova.append(valor)

        self._demanda[codigo] = nova
        self.salvar()
        print(f"MPS de {codigo} salvo.")

    def exibir(self):
        if not self._demanda:
            print("MPS vazio.")
            return

        cabecalho = "".join(f"{semana:>6}" for semana in range(1, 9))
        print(f"{'Item':<8}{cabecalho}")
        print("-" * 56)
        for codigo, valores in sorted(self._demanda.items()):
            linha = "".join(f"{valor:>6}" for valor in valores)
            print(f"{codigo:<8}{linha}")