import random
import xNN
import os
import time

# Le todos os arquivos de teste em um diretorio
for filename in os.listdir('testes'):
    # Le o arquivo de testes e preenche a lista de pontos
    pontos = []
    mapeamentoAtributos = []
    valor_k = -1
    # Abre o arquivo de teste
    with open('testes/'+filename) as file:
        # Le os valores contidos nele
        for line in file:
            line = line.strip()
            # Caso seja a primeira linha, ela indica o valor de k
            if valor_k == -1:
                valor_k = int(line)
                continue
            # Caso leia um EOF, interrompe a leitura
            if line == 'EOF':
                break
            else:
                # Le cada dado da linha
                partes = line.split(',')
                # Se a linha e a primeira de dados, inicializa o dicionario usado para atributos nominais
                if len(mapeamentoAtributos) == 0:
                    for i in range(len(partes)):
                        mapeamentoAtributos.append(dict())
                # Preenche a lista de pontos
                partesConvertidas = []
                for i in range(len(partes)):
                    # Se esse dado representa um atributo numerico, que nao seja o rotulo
                    if i != len(partes)-1 and partes[i].isnumeric():
                        partesConvertidas.append(float(partes[i]))
                    else:
                        # Se o atributo é nominal ou é o rótulo
                        if partes[i] not in mapeamentoAtributos[i]:
                            mapeamentoAtributos[i][partes[i]] = len(mapeamentoAtributos[i])
                        partesConvertidas.append(mapeamentoAtributos[i][partes[i]])
                # Salva os atributos em formato de pontos, seguido do rotulo identificado como A ou B
                pontos.append((tuple(partesConvertidas[:-1]), 'A' if partesConvertidas[-1] == 0 else 'B'))

    # Inicializa as variaveis de estatistica das execucoes
    tempoTotal = 0
    acuraciaTotal = 0
    revocacaoTotal = 0
    precisaoTotal = 0
    # Executa o algoritmo de KNN 10 vezes e guarda os valores encontrados
    for i in range(10):
        # Aleatoriza a ordem dos pontos
        random.shuffle(pontos)

        # Escolhe os pontos que serão usados para classificacao e treino
        numeroPontosClassificacao = int(len(pontos)*0.3)
        pontosClassificacao = pontos[:numeroPontosClassificacao]
        pontosTreino = pontos[numeroPontosClassificacao:]

        # Cria um conjunto dos pontos usados para classificacao com o rotulo A
        pontosAClassificacao = set()
        for ponto in pontosClassificacao:
            if ponto[1] == 'A':
                pontosAClassificacao.add(ponto[0])

        # Cria um conjunto dos pontos usados para treino com o rotulo A
        pontosATreino = set()
        for ponto in pontosTreino:
            if ponto[1] == 'A':
                pontosATreino.add(ponto[0])

        # Inicializa o contador de tempo
        start = time.time()

        # Inicializa o classificador
        classificador = xNN.xNN(valor_k, [ponto[0] for ponto in pontosTreino], [ponto[0] for ponto in pontosClassificacao], pontosAClassificacao, pontosATreino, len(pontosTreino[0]))

        # Salva o tempo gasto para a classificacao dos dados
        end = time.time()

        # Salva as estatisticas da execucao
        tempoTotal += end-start
        acuraciaTotal += classificador.obterAcuracia()
        revocacaoTotal += classificador.obterRevocacao()
        precisaoTotal += classificador.obterPrecisao()
    
    # Imprime a media dos resultados encontrados pelas 10 execucoes
    print('Resultados para o arquivo ', filename, ':', sep = '')
    print('Tempo =', tempoTotal/10.0)
    print('Acurácia:', acuraciaTotal/10.0)
    print('Revocação:', revocacaoTotal/10.0)
    print('Precisão:', precisaoTotal/10.0)
    print()
