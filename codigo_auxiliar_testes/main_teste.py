import xNNLib
import random
import os
import time

for filename in os.listdir('testes'):
    pontos = []
    mapeamentoAtributos = []
    valor_k = -1
    with open('testes/'+filename) as file:
        for line in file:
            line = line.strip()
            if valor_k == -1:
                valor_k = int(line)
                continue
            if line == 'EOF':
                break
            else:
                partes = line.split(',')
                if len(mapeamentoAtributos) == 0:
                    for i in range(len(partes)):
                        mapeamentoAtributos.append(dict())
                partesConvertidas = []
                for i in range(len(partes)):
                    if i != len(partes)-1 and partes[i].isnumeric():
                        partesConvertidas.append(float(partes[i]))
                    else:
                        if partes[i] not in mapeamentoAtributos[i]:
                            mapeamentoAtributos[i][partes[i]] = len(mapeamentoAtributos[i])
                        partesConvertidas.append(mapeamentoAtributos[i][partes[i]])
                
                pontos.append((tuple(partesConvertidas[:-1]), 'A' if partesConvertidas[-1] == 0 else 'B'))

    numeroPontosClassificacao = int(len(pontos)*0.3)

    pontosClassificacao = pontos[:numeroPontosClassificacao]
    pontosTreino = pontos[numeroPontosClassificacao:]

    pontosAClassificacao = set()
    for ponto in pontosClassificacao:
        if ponto[1] == 'A':
            pontosAClassificacao.add(ponto[0])

    pontosATreino = set()
    for ponto in pontosTreino:
        if ponto[1] == 'A':
            pontosATreino.add(ponto[0])

    print('Resultados para o arquivo ', filename, ':', sep = '')
    
    start = time.time()
    classificador2 = xNNLib.xNN(valor_k, [ponto[0] for ponto in pontosTreino], [ponto[0] for ponto in pontosClassificacao], pontosAClassificacao, pontosATreino, len(pontosTreino[0]))

    end = time.time()
    print('Tempo =',end - start)
    #print(classificador2.obterClassificacoes())
    print(classificador2.obterAcuracia())
    print(classificador2.obterRevocacao())
    print(classificador2.obterPrecisao())
