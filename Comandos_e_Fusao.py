from bplustree import BPlusTree 

class No:
    """
    Representa um nó no sistema de arquivos. Pode ser um diretório ou um arquivo.
    Se for um diretório, ele contém uma B+ Tree para gerenciar seus próprios filhos (arquivos/subdiretórios).
    """
    def __init__(self, e_diretorio):
        # Indica se o nó representa um diretório (True) ou um arquivo (False)
        self.e_diretorio = e_diretorio
        # Se for um diretório, ele tem uma B+ Tree para armazenar seus conteúdos.
        # Caso contrário (se for um arquivo), não precisa de uma árvore interna.
        # O grau da B+ Tree (4, neste caso) define a capacidade dos nós internos.
        self.arvore = BPlusTree(4) if e_diretorio else None

class Shell:
    """
    Implementa uma interface de linha de comando simples para interagir com o sistema de arquivos.
    Simula comandos básicos como 'ls', 'mkdir', 'touch', 'cd' e 'rm'.
    """
    def __init__(self):
        # O nó raiz do sistema de arquivos, sempre um diretório.
        self.raiz = No(e_diretorio=True)
        # O diretório de trabalho atual (Current Working Directory - CWD).
        # Começa na raiz.
        self.cwd = self.raiz
        # Lista para armazenar o caminho atual, exibido no prompt.
        # Começa com "~" para representar a raiz.
        self.caminho = ["~"]
        # Pilha para rastrear os diretórios pai, usada para o comando 'cd ..'.
        self.pais = []

    def prompt(self):
        """
        Retorna a string do prompt, mostrando o caminho atual.
        Ex: fakerational:~/documentos/meus_arquivos$
        """
        return f"fakerational:{'/'.join(self.caminho)}$ "

    def run(self):
        """
        Loop principal do shell que lê e executa comandos do usuário.
        """
        while True:
            try:
                # Lê a entrada do usuário, remove espaços extras e divide em comando e argumentos.
                comando_completo = input(self.prompt()).strip().split()
                if not comando_completo:
                    continue # Ignora entradas vazias

                # Desempacota o comando principal e seus argumentos
                comando, *argumentos = comando_completo
                
                # Tenta chamar o método correspondente ao comando (ex: do_ls, do_mkdir).
                # Se o método não existir, chama 'unknown'.
                getattr(self, f"do_{comando}", self.desconhecido)(*argumentos)
            except (KeyboardInterrupt, EOFError):
                # Captura Ctrl+C ou Ctrl+D para sair do shell de forma elegante.
                print("\nSaindo do fakerational.")
                break

    def desconhecido(self, *argumentos):
        """
        Método chamado quando um comando digitado não é reconhecido.
        """
        print("Comando desconhecido.")

    def do_ls(self, *argumentos):
        """
        Lista o conteúdo do diretório atual.
        Adiciona '/' ao final dos nomes de diretórios para fácil identificação.
        """
        # Pega todas as chaves (nomes de arquivos/diretórios) da B+ Tree do diretório atual.
        chaves = self.cwd.arvore.listar_chaves()
        for chave in chaves:
            # Busca o nó correspondente à chave para verificar se é um diretório ou arquivo.
            valor = self.cwd.arvore.buscar(chave)
            sufixo = '/' if valor.e_diretorio else '' # Adiciona '/' se for diretório
            print(f"{chave}{sufixo}")

    def do_mkdir(self, nome):
        """
        Cria um novo diretório no diretório atual.
        """
        # Verifica se um item com o mesmo nome já existe.
        if self.cwd.arvore.buscar(nome):
            print("Diretório já existe.")
        else:
            # Insere um novo nó de diretório na B+ Tree do diretório atual.
            self.cwd.arvore.inserir(nome, No(e_diretorio=True))

    def do_touch(self, nome):
        """
        Cria um novo arquivo vazio no diretório atual.
        """
        # Verifica se um item com o mesmo nome já existe.
        if self.cwd.arvore.buscar(nome):
            print("Arquivo já existe.")
        else:
            # Insere um novo nó de arquivo na B+ Tree do diretório atual.
            self.cwd.arvore.inserir(nome, No(e_diretorio=False))

    def do_cd(self, nome):
        """
        Muda o diretório de trabalho atual.
        Suporta ".." para voltar ao diretório pai.
        """
        if nome == "..":
            # Se a lista de pais não estiver vazia, volta para o diretório anterior.
            if self.pais:
                self.cwd = self.pais.pop()    # Restaura o diretório pai
                self.caminho.pop() # Remove o último componente do caminho
        else:
            # Busca o nó com o nome especificado no diretório atual.
            no = self.cwd.arvore.buscar(nome)
            # Verifica se o nó existe e se é de fato um diretório.
            if not no or not no.e_diretorio:
                print("Diretório não encontrado.")
            else:
                # Adiciona o diretório atual à pilha de pais e muda para o novo diretório.
                self.pais.append(self.cwd)
                self.cwd = no
                self.caminho.append(nome) # Adiciona o novo nome ao caminho

    def do_rm(self, nome):
        """
        Remove um arquivo ou diretório vazio.
        Diretórios não vazios não podem ser removidos.
        """
        no = self.cwd.arvore.buscar(nome)
        if not no:
            print("Elemento não encontrado.")
        # Se for um diretório e não estiver vazio (ou seja, tem chaves em sua árvore interna),
        # impede a remoção.
        elif no.e_diretorio and no.arvore.listar_chaves():
            print("Diretório não está vazio.")
        else:
            # Deleta o item da B+ Tree do diretório atual.
            self.cwd.arvore.deletar(nome)

if __name__ == "__main__":
    # Cria uma instância do shell e o executa.
    Shell().run()