class NoArvoreBPlus:
    """
    Representa um nó na B+ Tree.
    Pode ser um nó folha (que armazena os dados reais) ou um nó interno (que aponta para outros nós).
    """
    def __init__(self, e_folha=False):
        # Indica se este nó é uma folha ou um nó interno
        self.e_folha = e_folha
        # Lista para armazenar as chaves (valores para comparação)
        self.chaves = []
        # Lista para armazenar os filhos (outros nós ou os próprios valores dos dados se for folha)
        self.filhos = []
        # Ponteiro para o próximo nó folha na sequência (apenas para nós folha, para travessia sequencial)
        self.proximo = None
        # Ponteiro para o nó folha anterior na sequência (apenas para nós folha)
        self.anterior = None

class ArvoreBPlus:
    """
    Implementação de uma B+ Tree.
    Ideal para sistemas de banco de dados e sistemas de arquivos devido à sua eficiência em operações
    de busca, inserção e remoção, especialmente quando os dados são armazenados em disco.
    """
    def __init__(self, grau):
        # O nó raiz da árvore, inicialmente uma folha
        self.raiz = NoArvoreBPlus(e_folha=True)
        # O grau (ou ordem) da árvore, que determina o número máximo de chaves e filhos em um nó
        self.grau = grau

    def _encontrar_folha(self, chave, no=None):
        """
        Método auxiliar para encontrar o nó folha correto onde uma chave específica deveria estar.
        """
        if no is None:
            no = self.raiz
        # Percorre a árvore até encontrar um nó folha
        while not no.e_folha:
            i = 0
            # Encontra o índice do filho apropriado para seguir
            while i < len(no.chaves) and chave >= no.chaves[i]:
                i += 1
            no = no.filhos[i]
        return no

    def buscar(self, chave):
        """
        Busca um valor associado a uma chave na árvore.
        Retorna o valor se encontrado, caso contrário, retorna None.
        """
        no = self._encontrar_folha(chave)
        # Itera sobre as chaves do nó folha para encontrar a chave desejada
        for i, item in enumerate(no.chaves):
            if item == chave:
                # Os valores são armazenados na lista 'filhos' dos nós folha, na mesma posição que a chave
                return no.filhos[i]
        return None

    def inserir(self, chave, valor):
        """
        Insere uma nova chave-valor na árvore.
        """
        # Evita a inserção de chaves duplicadas para manter a unicidade
        if self.buscar(chave):
            return

        raiz_atual = self.raiz
        # Verifica se a raiz está cheia e precisa ser dividida antes da inserção
        if len(raiz_atual.chaves) == (self.grau - 1):
            nova_raiz = NoArvoreBPlus()
            nova_raiz.filhos.append(self.raiz)
            # Divide a raiz antiga e promove uma chave para a nova raiz
            self._dividir_filho(nova_raiz, 0)
            self.raiz = nova_raiz
        # Chama o método auxiliar para inserir no nó que não está cheio
        self._inserir_nao_cheio(self.raiz, chave, valor)

    def _inserir_nao_cheio(self, no, chave, valor):
        """
        Método auxiliar para inserir uma chave-valor em um nó que não está cheio.
        Garante que a propriedade de não estar cheio seja mantida.
        """
        if no.e_folha:
            i = 0
            # Encontra a posição correta para inserir a nova chave-valor, mantendo a ordem
            while i < len(no.chaves) and chave > no.chaves[i]:
                i += 1
            no.chaves.insert(i, chave)
            no.filhos.insert(i, valor)
        else:
            i = 0
            # Encontra o filho apropriado para descer
            while i < len(no.chaves) and chave >= no.chaves[i]:
                i += 1
            # Se o filho estiver cheio, divide-o
            if len(no.filhos[i].chaves) == (self.grau - 1):
                self._dividir_filho(no, i)
                # Decide qual dos dois novos filhos seguir após a divisão
                if chave > no.chaves[i]:
                    i += 1
            # Recursivamente insere no filho apropriado
            self._inserir_nao_cheio(no.filhos[i], chave, valor)

    def _dividir_filho(self, pai, indice):
        """
        Divide um filho cheio do nó pai em dois, promovendo uma chave para o nó pai.
        Essencial para manter as propriedades da B+ Tree durante a inserção.
        """
        no = pai.filhos[indice]
        novo_no = NoArvoreBPlus(e_folha=no.e_folha)
        # Ponto médio para a divisão das chaves
        meio = len(no.chaves) // 2

        if no.e_folha:
            # Para nós folha, o meio e os elementos à direita vão para o novo nó
            novo_no.chaves = no.chaves[meio:]
            novo_no.filhos = no.filhos[meio:]
            # O nó original fica com a parte esquerda
            no.chaves = no.chaves[:meio]
            no.filhos = no.filhos[:meio]

            # Ajusta os ponteiros de 'proximo' e 'anterior' para manter a lista ligada das folhas
            novo_no.proximo = no.proximo
            novo_no.anterior = no
            if no.proximo:
                no.proximo.anterior = novo_no
            no.proximo = novo_no

            # A primeira chave do novo nó é promovida para o pai
            pai.chaves.insert(indice, novo_no.chaves[0])
        else:
            # Para nós internos, a chave do meio é promovida para o pai
            # e os elementos à direita do meio vão para o novo nó
            novo_no.chaves = no.chaves[meio+1:]
            novo_no.filhos = no.filhos[meio+1:]
            pai.chaves.insert(indice, no.chaves[meio])
            # O nó original fica com a parte esquerda (sem a chave promovida)
            no.chaves = no.chaves[:meio]
            no.filhos = no.filhos[:meio+1]

        # Insere o novo nó como filho do pai
        pai.filhos.insert(indice + 1, novo_no)

    def listar_chaves(self):
        """
        Percorre todas as chaves da árvore em ordem, começando pela folha mais à esquerda.
        Útil para depuração ou para listar todos os dados.
        """
        no = self.raiz
        # Desce até a folha mais à esquerda
        while not no.e_folha:
            no = no.filhos[0]
        resultado = []
        # Percorre a lista ligada de folhas para coletar todas as chaves
        while no:
            resultado.extend(no.chaves)
            no = no.proximo
        return resultado

    def deletar(self, chave):
        """
        Deleta uma chave e seu valor associado da árvore.
        """
        self._deletar(self.raiz, chave)
        # Se a raiz não for mais uma folha e tiver apenas um filho, esse filho se torna a nova raiz
        if not self.raiz.e_folha and len(self.raiz.filhos) == 1:
            self.raiz = self.raiz.filhos[0]

    def _deletar(self, no, chave):
        """
        Método auxiliar recursivo para deletar uma chave da árvore.
        Lida com a fusão e redistribuição de nós para manter as propriedades da B+ Tree.
        """
        if no.e_folha:
            # Se for um nó folha e a chave estiver presente, remove-a
            if chave in no.chaves:
                indice = no.chaves.index(chave)
                no.chaves.pop(indice)
                no.filhos.pop(indice)
            return

        i = 0
        # Encontra o índice do filho apropriado para descer ou o índice da chave no nó atual
        while i < len(no.chaves) and chave >= no.chaves[i]:
            i += 1

        filho = no.filhos[i]
        self._deletar(filho, chave) # Chama recursivamente para deletar no filho

        # Verifica se o filho está abaixo do limite mínimo de chaves após a deleção
        # O limite é (grau - 1) // 2
        if len(filho.chaves) < (self.grau - 1) // 2:
            # Tenta redistribuir chaves com um irmão ou fundir nós
            irmao_esq = no.filhos[i - 1] if i > 0 else None
            irmao_dir = no.filhos[i + 1] if i + 1 < len(no.filhos) else None

            # Caso 1: Redistribuir do irmão esquerdo (se existir e tiver chaves suficientes)
            if irmao_esq and len(irmao_esq.chaves) > (self.grau - 1) // 2:
                # Pega a chave do pai e move para o filho, e a maior chave do irmão esquerdo para o pai
                filho.chaves.insert(0, no.chaves[i - 1])
                no.chaves[i - 1] = irmao_esq.chaves.pop()
                if not filho.e_folha:
                    filho.filhos.insert(0, irmao_esq.filhos.pop())
            # Caso 2: Redistribuir do irmão direito (se existir e tiver chaves suficientes)
            elif irmao_dir and len(irmao_dir.chaves) > (self.grau - 1) // 2:
                # Pega a chave do pai e move para o filho, e a menor chave do irmão direito para o pai
                filho.chaves.append(no.chaves[i])
                no.chaves[i] = irmao_dir.chaves.pop(0)
                if not filho.e_folha:
                    filho.filhos.append(irmao_dir.filhos.pop(0))
            # Caso 3: Fundir com um irmão (se nenhum irmão tiver chaves suficientes para redistribuir)
            else:
                if irmao_esq:
                    # Funde o filho com o irmão esquerdo
                    # A chave do pai que separava os dois é movida para o irmão esquerdo
                    irmao_esq.chaves += [no.chaves.pop(i - 1)] + filho.chaves
                    if not irmao_esq.e_folha:
                        irmao_esq.filhos += filho.filhos
                    no.filhos.pop(i) # Remove o filho fundido do pai
                elif irmao_dir:
                    # Funde o filho com o irmão direito
                    # A chave do pai que separava os dois é movida para o filho
                    filho.chaves += [no.chaves.pop(i)] + irmao_dir.chaves
                    if not filho.e_folha:
                        filho.filhos += irmao_dir.filhos
                    no.filhos.pop(i + 1) # Remove o irmão direito fundido do pai