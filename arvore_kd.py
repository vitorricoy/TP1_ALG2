class No:
    def __init__(self, valorNo, isFolha, profundidade, noEsquerda = None, noDireita = None):
        self.esq = noEsquerda
        self.dir = noDireita
        self.folha = isFolha
        self.val = valorNo
        self.profundidade = profundidade

    def getNoEsquerda(self):
        return self.esq
    
    def setNoEsquerda(self, noEsquerda):
        self.esq = noEsquerda
    
    def getNoDireita(self):
        return self.dir
    
    def setNoDireita(self, noDireita):
        self.dir = noDireita

    def setValor(self, valorNo):
        self.val = valorNo
    
    def getValor(self):
        return self.val
    
    def isFolha(self):
        return self.folha
    
    def setFolha(self, isFolha):
        self.folha = isFolha

    def getProfundidade(self):
        return self.profundidade
    
    def setProfundidade(self, profundidade):
        self.profundidade = profundidade


class ArvoreKD:

    def __init__(self, pontos, k):
        self.k = k
        self.raiz = self.construirArvore(pontos, 0)

    def construirArvore(self, pontos, profundidade):
        if len(pontos) == 1:
            # Folha contendo o no
            return No(pontos[0], True, profundidade)
        else:
            # Divide os pontos
            pontos.sort(key=lambda pt : pt[profundidade%self.k])
            posMediana = len(pontos)//2
            mediana = pontos[posMediana][profundidade%self.k]
            pontos1 = pontos[:posMediana]
            pontos2 = pontos[posMediana:]
            noEsq = self.construirArvore(pontos1, profundidade+1)
            noDir = self.construirArvore(pontos2, profundidade+1)
            return No(mediana, False, profundidade, noEsq, noDir)

    def getRaiz(self):
        return self.raiz

    def getValor(self, no):
        return no.getValor()

    def getNoEsquerda(self, no):
        return no.getNoEsquerda()

    def getNoDireita(self, no):
        return no.getNoDireita()

    def isFolha(self, no):
        return no.isFolha()

    def getDimensao(self, no):
        return no.getProfundidade()%self.k
    
    def getProfundidade(self, no):
        return no.getProfundidade()


