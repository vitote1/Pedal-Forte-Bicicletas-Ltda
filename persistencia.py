import json
import os
import csv

PASTA_DADOS = os.path.join(os.path.dirname(__file__), 'dados')

def salvar_dados(nome_arquivo, dados): 
    os.makedirs(PASTA_DADOS, exist_ok=True)
    caminho_arquivo = os.path.join(PASTA_DADOS, nome_arquivo)
    with open(caminho_arquivo, 'w', encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

def carregar_dados(nome_arquivo, padrao=None):
    caminho_arquivo = os.path.join(PASTA_DADOS, nome_arquivo)
    try:
        with open(caminho_arquivo, 'r', encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {} if padrao is None else padrao
    
    except json.JSONDecodeError:
        print(f"ERRO: arquivo {nome_arquivo} está corrompido.")
        return {} if padrao is None else padrao

def carregar_csv(nome_arquivo):
    caminho = os.path.join(PASTA_DADOS, nome_arquivo)
    try:
        with open(caminho, "r", encoding="utf-8", newline="") as arquivo:
            return list(csv.DictReader(arquivo))
    except FileNotFoundError:
        return []


def adicionar_csv(nome_arquivo, campos, linha):
    os.makedirs(PASTA_DADOS, exist_ok=True)
    caminho = os.path.join(PASTA_DADOS, nome_arquivo)
    arquivo_novo = not os.path.exists(caminho) or os.path.getsize(caminho) == 0
    with open(caminho, "a", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        if arquivo_novo:
            escritor.writeheader()
        escritor.writerow(linha)