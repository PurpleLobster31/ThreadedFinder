import threading
from os import system, path
import PyPDF2 as pydf
from typing import NamedTuple

from utils import ler_PDF, alimenta_dados


contador_palavra = 0
lock = threading.Lock()
ocorrencias = []


def busca_palavra(info:NamedTuple) -> None:
    '''
      função que busca a palavra na linha e adiciona à lista de ocorrências um dicionário
      :param info: namedtuple (subclasses de tuplas com nomes de campo)
    '''
    global contador_palavra
    global ocorrencias
    global lock
    for linha in info.linhas_para_ler:
        num = linha.count(info.alvo)
        if num > 0:
            lock.acquire()
            contador_palavra += num
            ocorrencias.append({'Pagina':info.num_pag, 'Linha': linha})
            lock.release()

if __name__ == "__main__":
    print('Digite o nome do arquivo que deseja ler: ')
    arquivo = input()
    
    system('cls||clear')
    print('Informe a palavra ou frase que deseja procurar: ')
    alvo = input()
    
    linhas, num_threads = ler_PDF(arquivo)
    infos = alimenta_dados(alvo, linhas)
    
    thread_list = []
    for item in infos:
        t = threading.Thread(target=busca_palavra, args=(item,))
        t.start()
        thread_list.append(t)
    
    for thread in thread_list:
        thread.join()
        
    print(f"Número de ocorrências do termo '{alvo}' no arquivo: {contador_palavra}")
    print("-"*30)
    print("| Pg | Conteudo |")
    for item in ocorrencias:
        print(f"| {item['Pagina']} | {item['Linha']} |")

#TODO: joao fazer o README E O .PDF
