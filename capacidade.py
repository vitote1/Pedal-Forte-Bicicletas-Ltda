import re

from mps import HORIZONTE
from persistencia import carregar_dados, salvar_dados
from utils import validar_entrada_float, validar_entrada_texto

ARQUIVO_CENTROS = "centros.json"
ARQUIVO_ROTEIROS = "roteiros.json"
PADRAO_CENTRO = re.compile(r"^CT-\d{2}$")
BARRA_MAXIMA = 30


class CentroTrabalho:

    def __init__(self, codigo, descricao, capacidade, custo_hora):
        self.codigo = codigo
        self.descricao = descricao
        self.capacidade = capacidade
        self.custo_hora = custo_hora

    def transform_dict(self):
        return {
            "descricao": self.descricao,
            "capacidade": self.capacidade,
            "custo_hora": self.custo_hora,
        }

    @classmethod
    def de_dict(cls, codigo, dados):
        return cls(codigo, **dados)


class Roteiro:

    def __init__(self, codigo_item, centro, tempo):
        self.codigo_item = codigo_item
        self.centro = centro
        self.tempo = tempo

    def transform_dict(self):
        return {"centro": self.centro, "tempo": self.tempo}

    @classmethod
    def de_dict(cls, codigo_item, dados):
        return cls(codigo_item, **dados)

class Capacidade:

    def __init__(self, cadastro_itens, ordens):
        self._itens = cadastro_itens
        self._ordens = ordens
        self._centros = {}
        self._roteiros = {}
        self.carregar()

    def carregar(self):

        dados = carregar_dados(ARQUIVO_CENTROS)
        self._centros = {
            codigo: CentroTrabalho.de_dict(codigo, campos)
            for codigo, campos in dados.items()
        }
        dados = carregar_dados(ARQUIVO_ROTEIROS)
        self._roteiros = {
            codigo: Roteiro.de_dict(codigo, campos)
            for codigo, campos in dados.items()
        }

    def salvar(self):
        salvar_dados(ARQUIVO_CENTROS, {
            codigo: centro.transform_dict()
            for codigo, centro in self._centros.items()
        })
        salvar_dados(ARQUIVO_ROTEIROS, {
            codigo: roteiro.transform_dict()
            for codigo, roteiro in self._roteiros.items()
        })

    def centro(self, codigo):
        return self._centros.get(codigo)

    def roteiro(self, codigo_item):
        return self._roteiros.get(codigo_item)

    def cadastrar_centro(self):
        codigo = validar_entrada_texto(
            "Código do centro (ex.: CT-03): ").upper()
        if not PADRAO_CENTRO.match(codigo):
            print("ERRO: formato inválido. Use CT-NN (ex.: CT-03).")
            return
        if codigo in self._centros:
            print("ERRO: já existe um centro com esse código.")
            return

        self._centros[codigo] = CentroTrabalho(
            codigo=codigo,
            descricao=validar_entrada_texto("Descrição: "),
            capacidade=validar_entrada_float(
                "Capacidade (horas/semana): ", minimo=0.1),
            custo_hora=validar_entrada_float(
                "Custo-hora (R$): ", minimo=0.01),
        )
        self.salvar()
        print(f"Centro {codigo} cadastrado com sucesso.")

    def listar_centros(self):
        if not self._centros:
            print("Nenhum centro cadastrado.")
            return
        print(f"{'Código':<8} {'Descrição':<26} {'Cap. h/sem':>10} "
              f"{'R$/hora':>9}")
        print("-" * 56)
        for codigo in sorted(self._centros):
            c = self._centros[codigo]
            print(f"{c.codigo:<8} {c.descricao:<26} "
                  f"{c.capacidade:>10.1f} {c.custo_hora:>9.2f}")

    def definir_roteiro(self):
        codigo = validar_entrada_texto("Código do item: ").upper()
        item = self._itens.buscar(codigo)
        if item is None:
            print("ERRO: item não encontrado.")
            return
        if not item.fabricado:
            print("ERRO: só itens fabricados (PA ou SA) têm roteiro; "
                  "MP é comprada.")
            return

        codigo_centro = validar_entrada_texto(
            "Código do centro que produz: ").upper()
        if codigo_centro not in self._centros:
            print("ERRO: centro não cadastrado.")
            return

        tempo = validar_entrada_float(
            "Tempo por unidade (horas): ", minimo=0.001)
        self._roteiros[codigo] = Roteiro(codigo, codigo_centro, tempo)
        self.salvar()
        print(f"Roteiro de {codigo} salvo: {codigo_centro}, "
              f"{tempo:g} h/un.")

    def listar_roteiros(self):
        if not self._roteiros:
            print("Nenhum roteiro cadastrado.")
            return
        print(f"{'Item':<8} {'Descrição':<28} {'Centro':<7} {'h/un':>6}")
        print("-" * 52)
        for codigo in sorted(self._roteiros):
            r = self._roteiros[codigo]
            item = self._itens.buscar(codigo)
            descricao = item.descricao if item else "?"
            print(f"{r.codigo_item:<8} {descricao:<28} {r.centro:<7} "
                  f"{r.tempo:>6g}")

    def carga_semanal(self, codigo_centro):
        carga = [0.0] * HORIZONTE
        for ordem in self._ordens.todas():
            if ordem.tipo != "OP" or ordem.status != "LIBERADA":
                continue
            semana = max(1, ordem.liberar)
            if semana > HORIZONTE:
                continue
            roteiro = self._roteiros.get(ordem.codigo_item)
            if roteiro and roteiro.centro == codigo_centro:
                carga[semana - 1] += ordem.quantidade * roteiro.tempo
        return [round(horas, 3) for horas in carga]

    def exibir_crp(self):
        codigo = validar_entrada_texto(
            "Código do centro (ex.: CT-03): ").upper()
        centro = self._centros.get(codigo)
        if centro is None:
            print("ERRO: centro não encontrado.")
            return

        capacidade = f"{centro.capacidade:.1f}".replace(".", ",")
        print(f"\nCARGA x CAPACIDADE - {centro.codigo} "
              f"{centro.descricao} ({capacidade} h/semana)")
        print(f"{'Sem':<4}{'Carga(h)':>9}{'Uso(%)':>8}")

        sobrecarregadas = []
        for semana, horas in enumerate(self.carga_semanal(codigo), 1):
            uso = horas / centro.capacidade * 100
            barra = "#" * min(int(uso // 10), BARRA_MAXIMA)
            aviso = ""
            if horas > centro.capacidade:  # RN09
                aviso = " SOBRECARGA"
                sobrecarregadas.append(str(semana))
            carga = f"{horas:.1f}".replace(".", ",")
            print(f"{semana:<4}{carga:>9}{uso:>8.0f} {barra}{aviso}")

        if sobrecarregadas:
            print("Sugestao: antecipar OPs ou programar hora extra nas "
                  f"semanas {', '.join(sobrecarregadas)}.")