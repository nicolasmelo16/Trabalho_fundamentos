Projeto: Sistema de Arquivos com B+ Tree (fakerational)

📌 Descrição

Este projeto implementa um sistema de arquivos simulado, inspirado em terminais Unix/Linux, com suporte a comandos básicos como ls, cd, mkdir, touch e rm. A estrutura de armazenamento é baseada em uma árvore B+ Tree implementada do zero.

📁 Estrutura do Projeto
fakerational/
├── bplustree/
│   └── bplustree.py           # Implementação da árvore B+
├── terminal/
│   └── shell.py               # Interpretador de comandos fakerational
├── benchmark/
│   └── benchmark.py           # Scripts de benchmark e geração de gráficos
├── results/
│   └── graficos.png           # Gráficos de desempenho
└── README.md                  # Este arquivo
▶️ Como Executar

1. Instalar dependências
Este projeto utiliza apenas a biblioteca matplotlib para o benchmark. Instale com:
pip install matplotlib

2. Rodar o terminal interativo
python terminal/shell.py
Exemplo de uso:
fakerational:~$ mkdir projetos
fakerational:~$ cd projetos
fakerational:~/projetos$ touch experimento.txt
fakerational:~/projetos$ mkdir resultados
fakerational:~/projetos$ ls
experimento.txt
resultados/

3. Rodar o benchmark
python benchmark/benchmark.py
O gráfico será salvo em results/graficos.png.

⚙️ Funcionalidades
- Armazenamento hierárquico com diretórios e arquivos.
- Cada diretório é uma nova instância de uma B+ Tree.
- Encadeamento de folhas para busca sequencial eficiente.
- Comandos suportados: ls, cd, mkdir, touch, rm
- Balanceamento e fusão de nós após remoções

📊 Benchmark
- Mede o tempo médio das operações: inserção, busca, remoção
- Testado para n = 10^4, 10^5, 10^6
- Gráfico compara com crescimento logarítmico esperado O(log n)

✅ Entregáveis
- bplustree.py: implementação da B+ Tree
- shell.py: terminal com comandos
- benchmark.py: testes e gráficos
- graficos.png: comparação empírica
- README.md: instruções e documentação

