# -*- coding: utf-8 -*-
"""
UNIVERSIDAD DE CONCEPCION
Departamento de Ingenieria Informatica y
Ciencias de la Computacion

Memoria de Titulo Ingenieria Civil Informatica
DETECCION DE BORDES EN IMAGENES DGGE USANDO UN
SISTEMA HIBRIDO ACO CON LOGICA DIFUSA

Autor: Sebastian Ignacio Espinoza Jimenez
Patrocinante: Maria Angelica Pinninghoff Junemann
"""

import numpy as N
import MathTools as mat

class AntColonyOptimizer(object):
    """Ant Colony Optimization Engine"""
    
    def __init__(self):
        """AntColonyOptimizer AntColonyOptimizer()"""
        self._pheromoneMatrix = None
        self._imageFlag = False

    def hasPheromoneMatrix(self):
        """bool hasPheromoneMatrix()"""
        return self._imageFlag

    def getPheromoneMatrix(self):
        """numpy.array getPheromoneMatrix()"""
        return N.copy(self._pheromoneMatrix)

    def generatePheromoneMatrix(self, imageMatrix, heuristicMatrix, parameterSet):
        """numpy.array generatePheromoneMatrix(
            numpy.array imageMatrix, numpy.array heuristicMatrix, dict parameterSet)"""
        antMovementMode = parameterSet['antMovementMode']
        antCount = parameterSet['antCount']
        cycleCount = parameterSet['cycleCount']
        stepCount = parameterSet['stepCount']
        alpha = parameterSet['alpha']
        beta = parameterSet['beta']
        delta = parameterSet['delta']
        tuning = parameterSet['tuning']
        rho = parameterSet['rho']
        psi = parameterSet['psi']
        mathTools = mat.MathTools()
        pheromoneMatrix = self._generateInitialPheromoneMatrix(N.copy(imageMatrix))
        matrixHeight = heuristicMatrix.shape[0]
        matrixWidth = heuristicMatrix.shape[1]
        indexes = list(N.ndindex(matrixHeight, matrixWidth))
        N.random.shuffle(indexes)
        antSet = indexes[0:antCount]
        initialPheromoneMatrix = N.copy(pheromoneMatrix)
        heuristiqMatrix = N.copy(heuristicMatrix)
        heuristiqMatrix[N.where(heuristiqMatrix == 0)] = 1e-10
        for cycle in xrange(cycleCount):
            N.random.shuffle(antSet)
            antPrevious = list(antSet)
            for i in xrange(antCount):
                for step in xrange(stepCount):
                    x = antSet[i][0]
                    y = antSet[i][1]
                    dx = antPrevious[i][0] - x
                    dy = antPrevious[i][1] - y
                    top = x > 0
                    bottom = x < matrixHeight - 1
                    left = y > 0
                    right = y < matrixWidth - 1
                    heuristicWindow = heuristiqMatrix[x-top:x+bottom+1, y-left:y+right+1]
                    pheromoneWindow = pheromoneMatrix[x-top:x+bottom+1, y-left:y+right+1]
                    mask = float(heuristicWindow[top, left])
                    heuristicWindow[top, left] = 2.
                    minHeuristic = N.min(heuristicWindow)
                    heuristicWindow[top, left] = -2.
                    maxHeuristic = N.max(heuristicWindow)
                    heuristicWindow[top, left] = mask
                    if (maxHeuristic - minHeuristic > delta):
                        alpha -= tuning
                        beta += tuning
                    else:
                        alpha += tuning
                        beta -= tuning
                    probabilityMatrix = N.power(pheromoneWindow, alpha)*N.power(heuristicWindow, beta)
                    probabilityMatrix[top, left] = -2.
                    probabilityMatrix[top + dx, left + dy] = -2.
                    if antMovementMode == 1:
                        maxProbability = N.max(probabilityMatrix)
                        indexes = N.where(probabilityMatrix == maxProbability)
                        randomIndex = N.random.randint(indexes[0].shape[0])
                        newIndex = (indexes[0][randomIndex], indexes[1][randomIndex])
                    else:
                        indexes = N.where(probabilityMatrix >= 0)
                        probabilityArray = probabilityMatrix[indexes]
                        summationArray = N.cumsum(probabilityArray)
                        randomValue = N.random.rand(1)*summationArray[summationArray.shape[0] - 1]
                        probabilityIndex = N.where(summationArray >= randomValue[0])
                        probabilityValue = probabilityArray[probabilityIndex][0]                        
                        newIndex = N.where(probabilityMatrix == probabilityValue)
                        randomIndex = N.random.randint(newIndex[0].shape[0])
                        newIndex = (newIndex[0][randomIndex], newIndex[1][randomIndex])
                    newX = x+newIndex[0]-top
                    newY = y+newIndex[1]-left
                    antPrevious[i] = (x, y)
                    antSet[i] = (newX, newY)
                    pheromone = pheromoneMatrix[x,y]
                    heuristic = heuristiqMatrix[x,y]
                    pheromoneMatrix[x,y] = (1-rho)*pheromone + rho*heuristic
            pheromoneMatrix = (1-psi)*pheromoneMatrix + psi*initialPheromoneMatrix
        pheromoneMatrix = mathTools.normalize(pheromoneMatrix)
        self._pheromoneMatrix = N.copy(pheromoneMatrix)
        self._imageFlag = True
        return pheromoneMatrix
        
    def _generateInitialPheromoneMatrix(self, inputMatrix):
        """numpy.array _generateInitialPheromoneMatrix(numpy.array inputMatrix)"""
        mathTools = mat.MathTools()
        gaussianMatrix = mathTools.gaussianFilter(inputMatrix)
        gradientMatrix = mathTools.gradient(gaussianMatrix)
        laplacianMatrix = mathTools.gradient(gradientMatrix)
        initialPheromoneMatrix = gradientMatrix-laplacianMatrix
        initialPheromoneMatrix = mathTools.normalize(initialPheromoneMatrix)
        return initialPheromoneMatrix
        