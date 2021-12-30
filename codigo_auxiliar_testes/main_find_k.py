from sklearn.model_selection import GridSearchCV

from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier

import numpy as np
import random
import os
import time

for filename in os.listdir('testes'):
    pontos = []
    mapeamentoAtributos = []
    with open('testes/'+filename) as file:
        for line in file:
            line = line.strip()
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
                
                pontos.append(partesConvertidas)

    pontos = np.array(pontos)

    if len(pontos) > 1000:
        pontos = pontos[:1000]

    X = pontos[:, :-1]
    y = pontos[:, -1:]

    k_range = list(range(3,100))
    weight_options = ["uniform", "distance"]

    param_grid = dict(n_neighbors = k_range, weights = weight_options)


    knn = KNeighborsClassifier()

    grid = GridSearchCV(knn, param_grid, cv = 10, scoring = 'accuracy')
    grid.fit(X,y.ravel())

    print('Melhor k para o arquivo', filename, ':', grid.best_params_['n_neighbors'])
