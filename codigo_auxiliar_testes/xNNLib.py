import math
import numpy as np
from sklearn.neighbors import KDTree

class xNN:
    def __init__(self, k, pontosTreinamento, pontosClassificacao, pontosAClassificacao, pontosATreino, dimensaoPontos):
        self.k = k
        self.pontosATreino = pontosATreino
        self.pontosAClassificacao = pontosAClassificacao
        classificacoes = self.classificaPontos(pontosClassificacao, pontosTreinamento)
        self.precisao = self.calculaPrecisao(pontosClassificacao, classificacoes)
        self.acuracia = self.calculaAcuracia(pontosClassificacao, classificacoes)
        self.revocacao = self.calculaRevocacao(pontosClassificacao, classificacoes)
        self.classificacoes = self.construirClassificacoes(pontosClassificacao, classificacoes)
    
    def classificaPontos(self, pontosClassificacao, pontosTreinamento):
        pontosTreino_temp = [list(ponto) for ponto in pontosTreinamento]
        pontosClassificacao_temp = [list(ponto) for ponto in pontosClassificacao]
        kdt = KDTree(np.array(pontosTreino_temp), leaf_size=1, metric='euclidean')
        res = kdt.query(np.array(pontosClassificacao_temp), k=self.k, return_distance=False)
        classi = []
        for classificacoes in res:
            rotulos = ['A' if pontosTreinamento[ind] in self.pontosATreino else 'B' for ind in classificacoes]
            numeroAs = 0
            numeroBs = 0
            for rotulo in rotulos:
                if rotulo == 'A':
                    numeroAs+=1
                else:
                    numeroBs+=1
            if numeroAs > numeroBs:
                classi.append('A')
            else:
                classi.append('B')
        return classi
    
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