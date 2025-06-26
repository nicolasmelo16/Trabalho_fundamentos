import time
import random
import math
import matplotlib.pyplot as plt
import os
import sys

# Ajusta o PATH para que possamos importar a BPlusTree do diretório pai.
# Assumindo a estrutura:
# fakerational/
# ├── bplustree/
# │   └── bplustree.py
# ├── benchmark/
# │   └── benchmark.py
# O diretório 'fakerational' precisa estar no PYTHONPATH ou ajustamos o sys.path
# para encontrar 'bplustree'.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'bplustree')))

from bplustree import ArvoreBPlus # Sua classe BPlusTree está definida como ArvoreBPlus


# Funções para realizar os testes de benchmark
def medir_tempo_insercao(n_elementos, grau_arvore):
    arvore = ArvoreBPlus(grau_arvore)
    chaves = list(range(n_elementos))
    random.shuffle(chaves) # Insere chaves em ordem aleatória para evitar pior caso
    
    start_time = time.time()
    for chave in chaves:
        arvore.inserir(chave, f"valor_{chave}")
    end_time = time.time()
    return end_time - start_time

def medir_tempo_busca(n_elementos, grau_arvore):
    arvore = ArvoreBPlus(grau_arvore)
    chaves_inserir = list(range(n_elementos))
    for chave in chaves_inserir:
        arvore.inserir(chave, f"valor_{chave}")

    chaves_buscar = random.sample(chaves_inserir, min(n_elementos, 1000)) # Busca um subconjunto para agilizar
    
    start_time = time.time()
    for chave in chaves_buscar:
        arvore.buscar(chave)
    end_time = time.time()
    
    # Retorna o tempo médio por busca
    return (end_time - start_time) / len(chaves_buscar) if chaves_buscar else 0

def medir_tempo_remocao(n_elementos, grau_arvore):
    arvore = ArvoreBPlus(grau_arvore)
    chaves_inserir = list(range(n_elementos))
    for chave in chaves_inserir:
        arvore.inserir(chave, f"valor_{chave}")
    
    chaves_remover = random.sample(chaves_inserir, min(n_elementos, 1000)) # Remove um subconjunto
    
    start_time = time.time()
    for chave in chaves_remover:
        arvore.deletar(chave)
    end_time = time.time()

    # Retorna o tempo médio por remoção
    return (end_time - start_time) / len(chaves_remover) if chaves_remover else 0

def main():
    tamanhos_n = [10**3, 10**4, 10**5]  # Reduzindo para evitar execuções muito longas em testes iniciais.
                                       # Você pode voltar para [10**4, 10**5, 10**6] depois.
    grau_arvore = 4 # Grau da B+ Tree (o mesmo usado no Shell)

    tempos_insercao = []
    tempos_busca = []
    tempos_remocao = []
    log_n_valores = []

    print("Iniciando benchmark...")

    for n in tamanhos_n:
        print(f"\nTestando com N = {n} elementos (Grau = {grau_arvore})...")
        
        # Inserção
        tempo_ins = medir_tempo_insercao(n, grau_arvore)
        tempos_insercao.append(tempo_ins)
        print(f"  Tempo de Inserção de {n} elementos: {tempo_ins:.6f} segundos")
        
        # Busca (tempo médio por operação)
        tempo_bus = medir_tempo_busca(n, grau_arvore)
        tempos_busca.append(tempo_bus)
        print(f"  Tempo Médio de Busca (por operação): {tempo_bus:.6f} segundos")

        # Remoção (tempo médio por operação)
        tempo_rem = medir_tempo_remocao(n, grau_arvore)
        tempos_remocao.append(tempo_rem)
        print(f"  Tempo Médio de Remoção (por operação): {tempo_rem:.6f} segundos")
        
        # Valores de referência para O(log N)
        log_n_valores.append(math.log10(n) if n > 0 else 0) # Usando log base 10 para visualização

    print("\nBenchmark concluído.")

    # Normalizar os valores de log_n para comparar na mesma escala
    # Encontrar o maior tempo entre todas as operações para o maior N
    max_time_overall = max(max(tempos_insercao), max(tempos_busca), max(tempos_remocao))

    # Ajustar a escala do log_n para que o último ponto seja próximo ao maior tempo
    if len(log_n_valores) > 0 and log_n_valores[-1] > 0:
        fator_escala = max_time_overall / log_n_valores[-1]
        log_n_escalado = [val * fator_escala for val in log_n_valores]
    else:
        log_n_escalado = [0] * len(tamanhos_n)


    # Geração do gráfico
    plt.figure(figsize=(12, 8))
    plt.plot(tamanhos_n, tempos_insercao, marker='o', label='Inserção Total')
    plt.plot(tamanhos_n, [t * n for t, n in zip(tempos_busca, tamanhos_n)], marker='o', label='Busca Total (tempo médio * N)') # Convertendo para total para comparação
    plt.plot(tamanhos_n, [t * n for t, n in zip(tempos_remocao, tamanhos_n)], marker='o', label='Remoção Total (tempo médio * N)') # Convertendo para total
    plt.plot(tamanhos_n, log_n_escalado, linestyle='--', color='gray', label='O(log N) Escalado')

    plt.xscale('log') # Eixo X em escala logarítmica para N
    plt.xlabel('Número de Elementos (N) - Escala Logarítmica')
    plt.ylabel('Tempo (segundos)')
    plt.title('Desempenho da B+ Tree (Grau = {})'.format(grau_arvore))
    plt.legend()
    plt.grid(True, which="both", ls="--", c='0.7')

    # Garantir que o diretório 'results' exista
    output_dir = 'results'
    os.makedirs(output_dir, exist_ok=True)
    
    grafico_path = os.path.join(output_dir, 'graficos.png')
    plt.savefig(grafico_path)
    print(f"\nGráfico salvo em: {grafico_path}")

if __name__ == "__main__":
    main()