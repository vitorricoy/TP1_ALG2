import math
import arvore_kd
import bisect
import heapq

class xNN:
    # Construtor da classe xNN
    def __init__(self, k, pontosTreinamento, pontosClassificacao, pontosAClassificacao, pontosATreino, dimensaoPontos):
        # Constroi a arvore KD
        self.arvoreKD = arvore_kd.ArvoreKD(pontosTreinamento, dimensaoPontos)
        # Atribui o valor de k
        self.k = k
        # Atribui o conjunto de pontos de treino que possuem o rótulo A
        self.pontosATreino = pontosATreino
        # Atribui o conjunto de pontos de classificacao que possuem o rótulo A
        self.pontosAClassificacao = pontosAClassificacao
        # Classifica os pontos recebidos por argumento
        classificacoes = self.classificaPontos(pontosClassificacao)
        # Calcula a precisão das classificacoes
        self.precisao = self.calculaPrecisao(pontosClassificacao, classificacoes)
        # Calcula a acuracia das classificacoes
        self.acuracia = self.calculaAcuracia(pontosClassificacao, classificacoes)
        # Calcula a revocacao das classificacoes
        self.revocacao = self.calculaRevocacao(pontosClassificacao, classificacoes)
        # Constroi uma lista que contém cada ponto seguido de sua classificacao
        self.classificacoes = self.construirClassificacoes(pontosClassificacao, classificacoes)
    
    # Classifica os pontos recebidos por argumento executando o algoritmo de KNN para cada um deles na Árvore KD construída
    def classificaPontos(self, pontosClassificacao):
        # Guarda as classificacoes de cada ponto
        classificacoes = []
        # Para cada ponto que deve ser classificado
        for ponto in pontosClassificacao:
            # Inicializa os parâmetros da funcao de classificacao como membros da classe para diminuir o overhead causado por esses parametros na recursao
            # A maior menor distancia encontrada ate o momento e inicializada como infinito
            self.maiorDistancia = math.inf
            # A fila de prioridades dos k vizinhos mais proximmos inicia vazia
            self.candidatos = []
            # Guarda cada ponto que e representado por um id salvo na fila de prioridades
            # Essa lista foi implementada para evitar a copia dos pontos ao atualizar a fila de prioridades, ja que os pontos sao representados por tuplas que podem
            # ter um tamanho razoavel. Com essa lista podemos salvar apenas um inteiro no lugar do ponto em si
            self.pontosPorId = []
            # Executa a classificacao do ponto, que retorna os k vizinhos mais proximos no array 'candidatos'
            self.buscaKVizinhosMaisProximos(self.arvoreKD.getRaiz(), ponto)
            # Salva os rotulos de cada ponto
            rotulos = ['A' if self.pontosPorId[ponto[1]] in self.pontosATreino else 'B' for ponto in self.candidatos]
            # Conta a frequencia de cada rotulo nos k vizinhos mais proximos
            numeroAs = 0
            numeroBs = 0
            for rotulo in rotulos:
                if rotulo == 'A':
                    numeroAs+=1
                else:
                    numeroBs+=1
            # Se o rotulo A for mais frequente, classifica o ponto como A
            if numeroAs > numeroBs:
                classificacoes.append('A')
            else:
                # Se o rotulo B for mais frequente, classifica o ponto como B
                if numeroBs > numeroAs:
                    classificacoes.append('B')
                else:
                    # Se a frequencia for igual, classifica o ponto com o mesmo rotulo do ponto mais proximo
                    classificacoes.append(rotulos[-1])
        # Retorna as classificacoes de cada ponto
        return classificacoes
    
    # Calcula a distancia euclidiana de dois pontos
    def distancia(self, ponto1, ponto2):
        if(len(ponto1) != len(ponto2)):
            print(ponto1, ponto2)
            raise 'Erro! Pontos de dimensões diferentes'
        
        soma = 0
        for dimensao in range(len(ponto1)):
            soma += (ponto1[dimensao]-ponto2[dimensao])**2
        
        return math.sqrt(soma)

    # Verifica se existe uma interseção entre a hiperesfera definida por 'ponto' e 'dist' com o hiperplano definido por 'valorNo'
    def compararPlanoEsfera(self, valorNo, ponto, dist, hiperplanoAEsquerda):
        # Caso o hiperplano esteja à esquerda do ponto
        if hiperplanoAEsquerda:
            return ponto - dist <= valorNo
        else:
            # Caso o hiperplano esteja à direita do ponto
            return ponto + dist >= valorNo

    # Funcao recursiva que busca os k vizinhos mais proximos de 'ponto'
    def buscaKVizinhosMaisProximos(self, noAtual, ponto):
        # Salva as informacoes do no atual da Arvore KD
        valorNo = noAtual.getValor()
        profundidade = noAtual.getProfundidade()
        dimensao = self.arvoreKD.getDimensao(noAtual)
        # Se o no atual e uma folha
        if noAtual.isFolha():
            # Calcula a distancia do ponto contido na folha e 'ponto'
            distancia = self.distancia(ponto, valorNo)
            # Se a distancia for menor do que a maior menor distancia encontrada ate o momento
            if distancia < self.maiorDistancia:
                # Verifica se a fila de prioridades ja tem k elementos
                if len(self.candidatos) == self.k:
                    # Remove o ultimo elemento da fila de prioridades
                    heapq.heappop(self.candidatos)
                # Adiciona o ponto na lista de ids de pontos
                self.pontosPorId.append(valorNo)
                # Adiciona o ponto na fila de prioridades, de acordo com a sua distancia
                heapq.heappush(self.candidatos, [-distancia, len(self.pontosPorId)-1])
                # Atualiza o valor da maior menor distancia encontrada ate o momento
                self.maiorDistancia = -self.candidatos[0][0]
        else:
            # Se o filho a esquerda pode conter pontos com distancias menores que a maior menor distancia e se o ponto sendo buscado
            # seria inserido nesse filho na Árvore KD
            if self.compararPlanoEsfera(valorNo, ponto[dimensao], self.maiorDistancia, True) and ponto[dimensao] <= valorNo:
                # Executa a funcao recursivamente para o filho a esquerda
                self.buscaKVizinhosMaisProximos(noAtual.getNoEsquerda(), ponto)
                # Caso o filho a direita possa ter pontos com a distancia menor do que a maior menor distancia apos a recursao no filho a esquerda
                if self.compararPlanoEsfera(valorNo, ponto[dimensao], self.maiorDistancia, False):
                    # Executa a funcao recursivamente para o filho a direita 
                    self.buscaKVizinhosMaisProximos(noAtual.getNoDireita(), ponto)
            else:
                # Se o filho a direita pode conter pontos com distancias menores que a maior menor distancia e se o ponto sendo buscado
                # seria inserido nesse filho na Árvore KD
                if self.compararPlanoEsfera(valorNo, ponto[dimensao], self.maiorDistancia, False) and ponto[dimensao] > valorNo:
                     # Executa a funcao recursivamente para o filho a direita 
                    self.buscaKVizinhosMaisProximos(noAtual.getNoDireita(), ponto)
                    # Caso o filho a esquerda possa ter pontos com a distancia menor do que a maior menor distancia apos a recursao no filho a direita
                    if self.compararPlanoEsfera(valorNo, ponto[dimensao], self.maiorDistancia, True):
                        # Executa a funcao recursivamente para o filho a esquerda
                        self.buscaKVizinhosMaisProximos(noAtual.getNoEsquerda(), ponto)

    # Calcula informacoes necessarias para as metricas da classificacao
    def obterInformacoesParaMetricaClassificacao(self, pontosClassificacao, classificacoes):
        verdadeiroA = 0
        falsoA = 0
        verdadeiroB = 0
        falsoB = 0
        # Calcula o numero de pontos classificados com cada rotulo, sendo falso negativo, falso positivo, verdadeiro negativo ou verdadeiro positivo
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

    # Calcula o valor da precisao da classificacao
    def calculaPrecisao(self, pontosClassificacao, classificacoes):
        verdadeiroA, falsoA, verdadeiroB, falsoB = self.obterInformacoesParaMetricaClassificacao(pontosClassificacao, classificacoes)
        return verdadeiroA/(verdadeiroA+falsoA)

    # Calcula o valor da revocacao da classificacao
    def calculaRevocacao(self, pontosClassificacao, classificacoes):
        verdadeiroA, falsoA, verdadeiroB, falsoB = self.obterInformacoesParaMetricaClassificacao(pontosClassificacao, classificacoes)
        return verdadeiroA/(verdadeiroA+falsoB)

    # Calcula o valor da acuracia da classificacao
    def calculaAcuracia(self, pontosClassificacao, classificacoes):
        verdadeiroA, falsoA, verdadeiroB, falsoB = self.obterInformacoesParaMetricaClassificacao(pontosClassificacao, classificacoes)
        return (verdadeiroA)/(verdadeiroA+falsoA+falsoB+verdadeiroB)

    # Calcula uma lista dos pontos em conjunto de sua classificacao
    def construirClassificacoes(self, pontosClassificacao, classificacoes):
        return [classificacoes[indice] for indice in range(len(classificacoes))]

    # Le o valor da acuracia
    def obterAcuracia(self):
        return self.acuracia

    # Le o valor da revocacao
    def obterRevocacao(self):
        return self.revocacao

    # Le o valor da precisao
    def obterPrecisao(self):
        return self.precisao
    
    # Le o valor das classificacoes
    def obterClassificacoes(self):
        return self.classificacoes