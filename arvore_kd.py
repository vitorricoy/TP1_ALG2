# Classe que define um no da arvore KD
class No:
    # Construtor de um no
    def __init__(self, valorNo, isFolha, profundidade, noEsquerda = None, noDireita = None):
        self.esq = noEsquerda
        self.dir = noDireita
        self.folha = isFolha
        self.val = valorNo
        self.profundidade = profundidade

    # Getters e setter dos atributos de um no
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

# Classe que representa uma arvore KD
class ArvoreKD:

    # Construtor da arvore KD
    def __init__(self, pontos, k):
        # Salva o valor de k da árvore, que é a dimensao dos pontos
        self.k = k
        # Constroi a arvores, salvando seu no raiz
        self.raiz = self.construirArvore(pontos, 0)

    # Funcao que constroi a arvore
    def construirArvore(self, pontos, profundidade):
        # Se o subconjunto e vazio
        if len(pontos) == 0:
            return None
        # Se o grupo de pontos possui apenas um ponto
        if len(pontos) == 1:
            # Cria um no folha contendo o ponto
            return No(pontos[0], True, profundidade)
        else:
            # Divide os pontos do grupo de acordo com a mediana
            # Caso o numero de pontos seja impar é escolhido o menor ponto entre os dois pontos da mediana
            pontos.sort(key=lambda pt : pt[profundidade%self.k])
            posMediana = len(pontos)//2
            mediana = pontos[posMediana][profundidade%self.k]
            # Valores iguais a mediana ficam a esquerda
            while posMediana < len(pontos) and pontos[posMediana] == mediana:
                posMediana+=1
            pontos1 = pontos[:posMediana]
            pontos2 = pontos[posMediana:]
            # Executa a funcao de construcao para os dois grupos separados pela mediana
            noEsq = self.construirArvore(pontos1, profundidade+1)
            noDir = self.construirArvore(pontos2, profundidade+1)
            # Cria um no intermediario na arvore
            return No(mediana, False, profundidade, noEsq, noDir)

    # Obtem a raiz da arvore
    def getRaiz(self):
        return self.raiz
    
    # Obtem qual dimensao e representada por um dado no intermediario em uma profundidade
    def getDimensao(self, no):
        return no.getProfundidade()%self.k


