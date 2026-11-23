from persistencia import salvar_dados, carregar_dados
from utils import validar_entrada_texto, validar_entrada_float

ARQUIVO = "estrutura.json"

COMPONENTES_PERMITIDOS = {
    "PA": ("SA", "MP"),
    "SA": ("MP",),
    "MP": (),
}

class Estrutura:

    def __init__(self, cadastro_itens):
        self._itens = cadastro_itens
        self._bom = {}
        self.carregar()

    def carregar(self):
        self._bom = carregar_dados(ARQUIVO)

    def salvar(self):
        salvar_dados(ARQUIVO, self._bom)

    def componentes(self, codigo_pai):
        return self._bom.get(codigo_pai, {})

    def _validar_vinculo(self, pai, filho):
        item_pai = self._itens.buscar(pai)
        item_filho = self._itens.buscar(filho)

        if item_pai is None:
            return f"item pai {pai} não cadastrado"
        if item_filho is None:
            return f"componente {filho} não cadastrado"
        if item_filho.tipo not in COMPONENTES_PERMITIDOS[item_pai.tipo]:
            return (f"um {item_pai.tipo} não pode ter componente do tipo "
                    f"{item_filho.tipo}")
        return None

    def adicionar_componente(self):
        pai = validar_entrada_texto("Código do item pai: ").upper()
        filho = validar_entrada_texto("Código do componente: ").upper()

        erro = self._validar_vinculo(pai, filho)
        if erro:
            print(f"ERRO: {erro}.")
            return
        if filho in self.componentes(pai):
            print("ERRO: esse componente já está na estrutura do pai.")
            return

        quantidade = validar_entrada_float(
            "Quantidade por unidade: ", minimo=0.0000001)
        self._bom.setdefault(pai, {})[filho] = quantidade
        self.salvar()
        print(f"{filho} adicionado à estrutura de {pai}.")

    def exibir(self):
        codigo = validar_entrada_texto("Código do produto: ").upper()
        item = self._itens.buscar(codigo)

        if item is None:
            print("ERRO: item não encontrado.")
            return
        if not self.componentes(codigo):
            print(f"{item.codigo} não possui estrutura cadastrada.")
            return

        niveis = {0: [codigo]}
        print(f"{item.codigo} {item.descricao}")
        self._exibir_filhos(codigo, "", 1, niveis)

        resumo = " | ".join(
            f"{nivel} = {', '.join(codigos)}"
            for nivel, codigos in sorted(niveis.items())
        )
        print(f"Níveis: {resumo}")

    def _exibir_filhos(self, codigo_pai, prefixo, nivel, niveis):
        filhos = list(self.componentes(codigo_pai).items())

        for posicao, (codigo, quantidade) in enumerate(filhos):
            ultimo = posicao == len(filhos) - 1
            conector = "└── " if ultimo else "├── "
            item = self._itens.buscar(codigo)

            texto = f"{prefixo}{conector}{codigo} {item.descricao}"
            pontos = "." * max(2, 45 - len(texto))
            qtd = f"{quantidade:g}".replace(".", ",")
            print(f"{texto} {pontos} {qtd} {item.unidade_medida}")

            niveis.setdefault(nivel, []).append(codigo)
            extensao = "    " if ultimo else "│   "
            self._exibir_filhos(codigo, prefixo + extensao, nivel + 1, niveis)