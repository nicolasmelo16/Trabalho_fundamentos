from math import ceil

class NoBPlus:
    def __init__(self, eh_folha=False):
        self.eh_folha = eh_folha
        self.chaves = []
        self.filhos = []
        self.proximo = None

    def minimo(self, grau):
        return ceil((grau - 1) / 2)

    def esta_cheio(self, grau):
        return len(self.chaves) >= grau - 1

class ArvoreBPlus:
    def __init__(self, grau=3):
        if grau < 3:
            raise ValueError("grau invalido")
        self.grau = grau
        self.raiz = NoBPlus(True)

    def buscar(self, chave, no=None):
        if no is None:
            no = self.raiz
        if no.eh_folha:
            for i, chave_no in enumerate(no.chaves):
                if chave_no == chave:
                    return no.filhos[i]
            return None
        for i, chave_no in enumerate(no.chaves):
            if chave < chave_no:
                return self.buscar(chave, no.filhos[i])
        return self.buscar(chave, no.filhos[-1])

    def inserir(self, chave, valor):
        if self.raiz.esta_cheio(self.grau):
            nova = NoBPlus()
            nova.filhos.append(self.raiz)
            self._dividir_no(nova, 0)
            self.raiz = nova
        self._inserir_rec(self.raiz, chave, valor)

    def _inserir_rec(self, no, chave, valor):
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
            if filho.esta_cheio(self.grau):
                self._dividir_no(no, indice)
                if chave > no.chaves[indice]:
                    indice += 1
            self._inserir_rec(no.filhos[indice], chave, valor)

    def _dividir_no(self, pai, indice):
        no = pai.filhos[indice]
        novo = NoBPlus(no.eh_folha)
        meio = self.grau // 2
        pai.chaves.insert(indice, no.chaves[meio])
        if no.eh_folha:
            novo.chaves = no.chaves[meio:]
            novo.filhos = no.filhos[meio:]
            no.chaves = no.chaves[:meio]
            no.filhos = no.filhos[:meio]
            novo.proximo = no.proximo
            no.proximo = novo
        else:
            novo.chaves = no.chaves[meio + 1:]
            novo.filhos = no.filhos[meio + 1:]
            no.chaves = no.chaves[:meio]
            no.filhos = no.filhos[:meio + 1]
        pai.filhos.insert(indice + 1, novo)

    def deletar(self, chave):
        self._remover_rec(self.raiz, chave)
        if not self.raiz.eh_folha and len(self.raiz.chaves) == 0:
            self.raiz = self.raiz.filhos[0]

    def _remover_rec(self, no, chave, pai=None, indice_pai=0):
        if no.eh_folha:
            if chave in no.chaves:
                pos = no.chaves.index(chave)
                no.chaves.pop(pos)
                no.filhos.pop(pos)
            if pai and len(no.chaves) < no.minimo(self.grau):
                self._rebalancear(pai, indice_pai)
            return
        for i, chave_no in enumerate(no.chaves):
            if chave < chave_no:
                self._remover_rec(no.filhos[i], chave, no, i)
                break
        else:
            self._remover_rec(no.filhos[-1], chave, no, len(no.chaves))
        if indice_pai < len(no.chaves):
            no.chaves[indice_pai] = no.filhos[indice_pai + 1].chaves[0]
        if pai and len(no.chaves) < no.minimo(self.grau):
            self._rebalancear(pai, indice_pai)

    def _rebalancear(self, pai, indice):
        no = pai.filhos[indice]
        if indice > 0:
            irmao_esq = pai.filhos[indice - 1]
            if len(irmao_esq.chaves) > irmao_esq.minimo(self.grau):
                if no.eh_folha:
                    no.chaves.insert(0, irmao_esq.chaves.pop())
                    no.filhos.insert(0, irmao_esq.filhos.pop())
                    pai.chaves[indice - 1] = no.chaves[0]
                else:
                    no.chaves.insert(0, pai.chaves[indice - 1])
                    pai.chaves[indice - 1] = irmao_esq.chaves.pop()
                    no.filhos.insert(0, irmao_esq.filhos.pop())
                return
        if indice < len(pai.filhos) - 1:
            irmao_dir = pai.filhos[indice + 1]
            if len(irmao_dir.chaves) > irmao_dir.minimo(self.grau):
                if no.eh_folha:
                    no.chaves.append(irmao_dir.chaves.pop(0))
                    no.filhos.append(irmao_dir.filhos.pop(0))
                    pai.chaves[indice] = irmao_dir.chaves[0]
                else:
                    no.chaves.append(pai.chaves[indice])
                    pai.chaves[indice] = irmao_dir.chaves.pop(0)
                    no.filhos.append(irmao_dir.filhos.pop(0))
                return
        if indice > 0:
            self._fundir(pai, indice - 1)
        else:
            self._fundir(pai, indice)

    def _fundir(self, pai, indice):
        esquerdo = pai.filhos[indice]
        direito = pai.filhos[indice + 1]
        if esquerdo.eh_folha:
            esquerdo.chaves += direito.chaves
            esquerdo.filhos += direito.filhos
            esquerdo.proximo = direito.proximo
        else:
            esquerdo.chaves.append(pai.chaves[indice])
            esquerdo.chaves += direito.chaves
            esquerdo.filhos += direito.filhos
        pai.chaves.pop(indice)
        pai.filhos.pop(indice + 1)
        if pai is not self.raiz and len(pai.chaves) < pai.minimo(self.grau):
            self._rebalancear_acima(self.raiz, pai)

    def _rebalancear_acima(self, atual, alvo):
        if atual.eh_folha:
            return
        for i, filho in enumerate(atual.filhos):
            if filho is alvo:
                if len(alvo.chaves) < alvo.minimo(self.grau):
                    self._rebalancear(atual, i)
                return
            self._rebalancear_acima(filho, alvo)

    def imprimir(self):
        folha = self.raiz
        while not folha.eh_folha:
            folha = folha.filhos[0]
        while folha:
            print(folha.chaves, end=" -> ")
            folha = folha.proximo
        print("None")

class Arquivo:
    def __init__(self, nome):
        self.nome = nome

class Terminal:
    def __init__(self, grau=3):
        self.arvore = ArvoreBPlus(grau)

    def touch(self, nome):
        if self.arvore.buscar(nome):
            print("ja existe")
            return
        self.arvore.inserir(nome, Arquivo(nome))
        print("criado")

    def rm(self, nome):
        if not self.arvore.buscar(nome):
            print("nao encontrado")
            return
        self.arvore.deletar(nome)
        print("removido")

    def ls(self):
        self.arvore.imprimir()

if __name__ == "__main__":
    terminal = Terminal(grau=3)
    terminal.touch("arquivo1.txt")
    terminal.touch("arquivo2.txt")
    terminal.touch("arquivo3.txt")
    terminal.ls()
    terminal.rm("arquivo2.txt")
    terminal.ls()