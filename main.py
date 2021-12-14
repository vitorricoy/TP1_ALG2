import random
import xNN

pontos = []

with open('teste.txt') as file:
    for line in file:
        line = line.strip()
        if line == 'EOF':
            break
        else:
            partes = line.split(',')
            partes = [float(parte) for parte in partes]
            pontos.append((tuple(partes[:-1]), 'A' if partes[-1] == 1 else 'B'))

random.shuffle(pontos)

numeroPontosClassificacao = int(len(pontos)*0.3)

pontosClassificacao = pontos[:numeroPontosClassificacao]
pontosTreino = pontos[numeroPontosClassificacao:]

pontosAClassificacao = []
for ponto in pontosClassificacao:
    if ponto[1] == 'A':
        pontosAClassificacao.append(ponto[0])

pontosATreino = []
for ponto in pontosTreino:
    if ponto[1] == 'A':
        pontosATreino.append(ponto[0])

classificador = xNN.xNN(3, [ponto[0] for ponto in pontosTreino], [ponto[0] for ponto in pontosClassificacao], pontosAClassificacao, pontosATreino, len(pontosTreino[0]))

print(classificador.obterAcuracia())
print(classificador.obterRevocacao())
print(classificador.obterPrecisao())