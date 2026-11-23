import re

PADRAO_CODE = re.compile(r"^(PA|SA|MP)-\d{3}$") 

def validar_codigo(codigo):
    return bool(PADRAO_CODE.match(codigo))

def validar_entrada_texto(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor

        print("ERRO: o valor não pode ser vazio.")


def validar_entrada_float(mensagem, minimo=0.0):
    while True:
        texto = input(mensagem).strip()
        try:
            valor = float(texto.replace(",", "."))
        except ValueError:
            print("ERRO: digite um número válido.")
            continue
        if valor < minimo:
            print(f"ERRO: o valor deve ser >= {minimo}.")
            continue
        return valor


def validar_entrada_int(mensagem, minimo=0):
    while True:
        texto = input(mensagem).strip()
        try:
            valor = int(texto)
        except ValueError:
            print("ERRO: digite um número inteiro.")
            continue
        if valor < minimo:
            print(f"ERRO: o valor deve ser >= {minimo}.")
            continue
        return valor

def perguntar_modificacao(mensagem):
 while True:
        valor = input(f"Deseja alterar o/a {mensagem} do produto? ([S] - Sim | [N] - Não): ").strip().upper()
        if valor in ("S" , "N"):
           valor = True if valor == "S" else False
           return valor

        print("ERRO: o valor não é válido.")