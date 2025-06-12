class NoBPlus:
    def __init__(self, eh_folha=False):
        self.eh_folha = eh_folha
        self.chaves = [] 
        self.filhos = [] 
        self.proximo = None 


class ArvoreBPlus:
    def __init__(self, grau):
        self.raiz = NoBPlus(eh_folha=True)  # Começa com uma folha
        self.grau = grau  # Número máximo de chaves por nó

    def buscar(self, chave, no=None):
        if no is None:
            no = self.raiz

        if no.eh_folha:
            for i, item in enumerate(no.chaves):
                if item == chave:
                    return no.filhos[i]
            return None 

        for i, item in enumerate(no.chaves):
            if chave < item:
                return self.buscar(chave, no.filhos[i])
        return self.buscar(chave, no.filhos[-1])

    def inserir(self, chave, valor):
        raiz = self.raiz
        if len(raiz.chaves) == self.grau - 1:
            nova_raiz = NoBPlus()
            nova_raiz.filhos.append(self.raiz)
            self._dividir_no(nova_raiz, 0)
            self.raiz = nova_raiz

        self._inserir_em_no_nao_cheio(self.raiz, chave, valor)

    def _inserir_em_no_nao_cheio(self, no, chave, valor):
        if no.eh_folha:
            indice = 0
            while indice < len(no.chaves) and chave > no.chaves[indice]:
                indice += 1
            no.chaves.insert(indice, chave)
            no.filhos.insert(indice, valor)
        else:
            indice = 0
            while indice < len(no.chaves) and chave > no.chaves[indice]:
                indice += 1
            filho = no.filhos[indice]
            if len(filho.chaves) == self.grau - 1:
                self._dividir_no(no, indice)
                if chave > no.chaves[indice]:
                    indice += 1
            self._inserir_em_no_nao_cheio(no.filhos[indice], chave, valor)

    def _dividir_no(self, pai, indice):
        grau = self.grau
        no = pai.filhos[indice]
        novo_no = NoBPlus(eh_folha=no.eh_folha)

        meio = grau // 2
        pai.chaves.insert(indice, no.chaves[meio])

        novo_no.chaves = no.chaves[meio:] if no.eh_folha else no.chaves[meio + 1:]
        novo_no.filhos = no.filhos[meio:] if no.eh_folha else no.filhos[meio + 1:]

        no.chaves = no.chaves[:meio] if no.eh_folha else no.chaves[:meio]
        no.filhos = no.filhos[:meio] if no.eh_folha else no.filhos[:meio + 1]

        pai.filhos.insert(indice + 1, novo_no)

        if no.eh_folha:
            novo_no.proximo = no.proximo
            no.proximo = novo_no

    def deletar(self, chave):
        pass

    def imprimir_folhas(self):
        no = self.raiz
        while not no.eh_folha:
            no = no.filhos[0]
        while no:
            print(no.chaves)
            no = no.proximo
