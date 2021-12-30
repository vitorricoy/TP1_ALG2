import math
import arvore_kd
import bisect
import heapq

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
            self.maiorDistancia = math.inf
            self.candidatos = []
            self.pontosPorId = []
            self.classificaPonto(self.arvoreKD.getRaiz(), ponto)
            rotulos = ['A' if self.pontosPorId[ponto[1]] in self.pontosATreino else 'B' for ponto in self.candidatos]
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
                if numeroBs > numeroAs:
                    classificacoes.append('B')
                else:
                    classificacoes.append(rotulos[-1])
        return classificacoes
    
    def distancia(self, ponto1, ponto2):
        if(len(ponto1) != len(ponto2)):
            print(ponto1, ponto2)
            raise 'Erro! Pontos de dimensões diferentes'
        
        soma = 0
        for dimensao in range(len(ponto1)):
            soma += (ponto1[dimensao]-ponto2[dimensao])**2
        
        return math.sqrt(soma)

    def compararPlanoEsfera(self, valorNo, ponto, dist, dir):
        if dir == 'Esq':
            return ponto - dist <= valorNo
        else:
            return ponto + dist >= valorNo

    def classificaPonto(self, noAtual, ponto):
        valorNo = noAtual.getValor()
        profundidade = noAtual.getProfundidade()
        dimensao = self.arvoreKD.getDimensao(noAtual)
        if noAtual.isFolha():
            distancia = self.distancia(ponto, valorNo)
            if distancia < self.maiorDistancia:
                if len(self.candidatos) == self.k:
                    # Remove o ultimo
                    heapq.heappop(self.candidatos)
                self.pontosPorId.append(valorNo)
                heapq.heappush(self.candidatos, [-distancia, len(self.pontosPorId)-1])
                self.maiorDistancia = -self.candidatos[0][0]
        else:
            if self.compararPlanoEsfera(valorNo, ponto[dimensao], self.maiorDistancia, 'Esq') and ponto[dimensao] <= valorNo:
                self.classificaPonto(noAtual.getNoEsquerda(), ponto)
                if self.compararPlanoEsfera(valorNo, ponto[dimensao], self.maiorDistancia, 'Dir'):
                    self.classificaPonto(noAtual.getNoDireita(), ponto)
            else:
                if self.compararPlanoEsfera(valorNo, ponto[dimensao], self.maiorDistancia, 'Dir') and ponto[dimensao] > valorNo:
                    self.classificaPonto(noAtual.getNoDireita(), ponto)
                    if self.compararPlanoEsfera(valorNo, ponto[dimensao], self.maiorDistancia, 'Esq'):
                        self.classificaPonto(noAtual.getNoEsquerda(), ponto)

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
        return [classificacoes[indice] for indice in range(len(classificacoes))]

    def obterAcuracia(self):
        return self.acuracia

    def obterRevocacao(self):
        return self.revocacao

    def obterPrecisao(self):
        return self.precisao
    
    def obterClassificacoes(self):
        return self.classificacoes