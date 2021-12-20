import math
import arvore_kd
import bisect

class xNN:
    def __init__(self, k, pontosTreinamento, pontosClassificacao, pontosAClassificacao, pontosATreino, dimensaoPontos):
        self.arvoreKD = arvore_kd.ArvoreKD(pontosTreinamento, dimensaoPontos)
        self.k = k
        self.pontosATreino = pontosATreino
        self.pontosAClassificacao = pontosAClassificacao
        classificacoes = self.classificaPontos(pontosClassificacao)
        self.precisao = self.calculaPrecisao(pontosClassificacao, classificacoes)
        self.acuracia = self.calculaAcuracia(pontosClassificacao, classificacoes)
        self.revocacao = self.calculaRevocacao(pontosClassificacao, classificacoes)
        self.classificacoes = self.construirClassificacoes(pontosClassificacao, classificacoes)
    
    def classificaPontos(self, pontosClassificacao):
        classificacoes = []
        for ponto in pontosClassificacao:
            self.candidatos = []
            self.visitados = set()
            self.ponto = ponto
            self.maiorDistancia = math.inf
            self.classificaPonto(self.arvoreKD.getRaiz())
            rotulos = ['A' if ponto[1] in self.pontosATreino else 'B' for ponto in self.candidatos]
            numeroAs = 0
            numeroBs = 0
            for rotulo in rotulos:
                if rotulo == 'A':
                    numeroAs+=1
                else:
                    numeroBs+=1
            if numeroAs > numeroBs:
                classificacoes.append('A')
            else:
                classificacoes.append('B')
        return classificacoes
    
    def distancia(self, ponto1, ponto2):
        if(len(ponto1) != len(ponto2)):
            raise 'Erro! Pontos de dimensões diferentes'
        
        soma = 0
        for dimensao in range(len(ponto1)):
            soma += (ponto1[dimensao]-ponto2[dimensao])**2
        
        return math.sqrt(soma)

    def classificaPonto(self, noAtual):
        if noAtual is None:
            return
        valorNo = self.arvoreKD.getValor(noAtual)
        profundidade = self.arvoreKD.getProfundidade(noAtual)
        dimensao = self.arvoreKD.getDimensao(noAtual)
        if (profundidade, valorNo) in self.visitados:
            return
        if self.arvoreKD.isFolha(noAtual):
            distancia = self.distancia(self.ponto, valorNo)

            if distancia < self.maiorDistancia:
                bisect.insort(self.candidatos, [distancia, valorNo])
                self.maiorDistancia = self.candidatos[-1][0]

            if len(self.candidatos) > self.k:
                self.candidatos.pop()
                self.maiorDistancia = self.candidatos[-1][0]
        else:
            if self.ponto[dimensao] < valorNo:
                self.classificaPonto(self.arvoreKD.getNoEsquerda(noAtual))
                if valorNo-self.ponto[dimensao] <= self.maiorDistancia:
                    self.classificaPonto(self.arvoreKD.getNoDireita(noAtual))
            else:
                self.classificaPonto(self.arvoreKD.getNoDireita(noAtual))
                if self.ponto[dimensao]-valorNo <= self.maiorDistancia:
                    self.classificaPonto(self.arvoreKD.getNoEsquerda(noAtual))
        self.visitados.add((profundidade, valorNo))

    def classificaPontoIt(self, noAtual, ponto, candidatos, visitados):
        maiorDistancia = math.inf
        pilha = []
        pilha.append(noAtual)
        while len(pilha) > 0:
            noAtual, ponto, candidatos, visitados, maiorDistancia = pilha.pop()
            if noAtual is None:
                return
            valorNo = self.arvoreKD.getValor(noAtual)
            profundidade = self.arvoreKD.getProfundidade(noAtual)
            dimensao = self.arvoreKD.getDimensao(noAtual)
            if (profundidade, valorNo) in visitados:
                return
            if self.arvoreKD.isFolha(noAtual):
                distancia = self.distancia(ponto, valorNo)

                if distancia < maiorDistancia:
                    bisect.insort(candidatos, [distancia, valorNo])
                    maiorDistancia = candidatos[-1]

                if len(candidatos) > self.k:
                    candidatos.pop()
                    maiorDistancia = candidatos[-1]
            else:
                if ponto[dimensao] < valorNo:
                    self.classificaPonto(self.arvoreKD.getNoEsquerda(noAtual), ponto, candidatos, visitados, maiorDistancia)
                    if valorNo-ponto[dimensao] <= maiorDistancia:
                        self.classificaPonto(self.arvoreKD.getNoDireita(noAtual), ponto, candidatos, visitados, maiorDistancia)
                else:
                    self.classificaPonto(self.arvoreKD.getNoDireita(noAtual), ponto, candidatos, visitados, maiorDistancia)
                    if ponto[dimensao]-valorNo <= maiorDistancia:
                        self.classificaPonto(self.arvoreKD.getNoEsquerda(noAtual), ponto, candidatos, visitados, maiorDistancia)
            visitados.add((profundidade, valorNo))


    def obterInformacoesParaMetricaClassificacao(self, pontosClassificacao, classificacoes):
        verdadeiroA = 0
        falsoA = 0
        verdadeiroB = 0
        falsoB = 0
        for indice in range(len(classificacoes)):
            if pontosClassificacao[indice] in self.pontosAClassificacao:
                if classificacoes[indice] == 'A':
                    verdadeiroA+=1
                else:
                    falsoB+=1
            else:
                if classificacoes[indice] == 'A':
                    falsoA+=1
                else:
                    verdadeiroB+=1
        return verdadeiroA, falsoA, verdadeiroB, falsoB

    def calculaPrecisao(self, pontosClassificacao, classificacoes):
        verdadeiroA, falsoA, verdadeiroB, falsoB = self.obterInformacoesParaMetricaClassificacao(pontosClassificacao, classificacoes)
        return verdadeiroA/(verdadeiroA+falsoA)

    def calculaRevocacao(self, pontosClassificacao, classificacoes):
        verdadeiroA, falsoA, verdadeiroB, falsoB = self.obterInformacoesParaMetricaClassificacao(pontosClassificacao, classificacoes)
        return verdadeiroA/(verdadeiroA+falsoB)

    def calculaAcuracia(self, pontosClassificacao, classificacoes):
        verdadeiroA, falsoA, verdadeiroB, falsoB = self.obterInformacoesParaMetricaClassificacao(pontosClassificacao, classificacoes)
        return (verdadeiroA)/(verdadeiroA+falsoA+falsoB+verdadeiroB)

    def construirClassificacoes(self, pontosClassificacao, classificacoes):
        return [(pontosClassificacao[indice], classificacoes[indice]) for indice in range(len(classificacoes))]

    def obterAcuracia(self):
        return self.acuracia

    def obterRevocacao(self):
        return self.revocacao

    def obterPrecisao(self):
        return self.precisao
    
    def obterClassificacoes(self):
        return self.classificacoes