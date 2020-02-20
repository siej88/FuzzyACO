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

class FuzzyMachine(object):
    """Mamdani-Type Fuzzy Inference Engine"""
    
    def __init__(self):
        """FuzzyMachine FuzzyMachine()"""
        self._heuristicMatrix = None
        self._imageFlag = False
        self._mathTools = mat.MathTools()

    def hasHeuristicMatrix(self):
        """bool hasHeuristicMatrix()"""
        return self._imageFlag

    def getHeuristicMatrix(self):
        """numpy.array getHeuristicMatrix()"""
        return N.copy(self._heuristicMatrix)

    def generateHeuristicMatrix(self, intensityMatrix, categorySet, parameterSet, ruleList):
        """numpy.array generateHeuristicMatrix(numpy.array intensityMatrix,
            dict categorySet, dict parameterSet, list ruleSet)"""
        deFuzzificationMode = parameterSet['deFuzzificationMode']
        variableMatrixSet = self._generateVariableMatrixSet(intensityMatrix)
        deFuzzifierAggregator = {}
        categoryKeys = categorySet.keys()
        for k in categoryKeys:
            if categorySet[k]['variable'] == 'edge':
                deFuzzifierAggregator[k] = []
        ruleCount = len(ruleList)
        for i in xrange(ruleCount):
            categoryCount = len(ruleList[i])
            minimumMatrixList = []
            edgeCategory = ''
            for j in xrange(categoryCount):
                category = ruleList[i][j]
                variable = categorySet[category]['variable']
                if variable != 'edge':
                    mean = categorySet[category]['mean']
                    scale = categorySet[category]['scale']
                    minimumMatrixList.append(self._mathTools.gaussian(variableMatrixSet[variable], mean, scale))
                else:
                    edgeCategory = category
            minimumMatrix = self._mathTools.minimum(minimumMatrixList)
            deFuzzifierAggregator[edgeCategory].append(minimumMatrix)
        maximumMatrixSet = {}
        maximumMatrixList = []
        edgeCategoryKeys = deFuzzifierAggregator.keys()
        for k in edgeCategoryKeys:
            if len(deFuzzifierAggregator[k]) > 0:
                maximumMatrixSet[k] = self._mathTools.maximum(deFuzzifierAggregator[k])
                maximumMatrixList.append(maximumMatrixSet[k])
        maximumValues = self._mathTools.maximum(maximumMatrixList)
        heuristicMatrix = N.zeros_like(intensityMatrix)
        edgeCategoryKeys = maximumMatrixSet.keys()
        if deFuzzificationMode != 2:
            for k in edgeCategoryKeys:
                indexes = N.where(maximumValues == maximumMatrixSet[k])
                values = maximumMatrixSet[k][indexes]
                values[N.where(values == 0)] = 1e-10
                mean = categorySet[k]['mean']
                scale = categorySet[k]['scale']
                heuristicMatrix[indexes] = self._mathTools.inverseGaussian(values, mean, scale, deFuzzificationMode)
        else:
            summationMatrix = N.zeros_like(intensityMatrix)
            for k in edgeCategoryKeys:                
                mean = categorySet[k]['mean']
                scale = categorySet[k]['scale']
                heuristicMatrix += maximumMatrixSet[k] * mean * scale
                summationMatrix += maximumMatrixSet[k] * scale
            summationMatrix[N.where(summationMatrix == 0)] = 1e-10
            heuristicMatrix /= summationMatrix
        heuristicMatrix *= self._mathTools.standardDeviation(intensityMatrix)
        heuristicMatrix = self._mathTools.normalize(heuristicMatrix)
        self._heuristicMatrix = N.copy(heuristicMatrix)
        self._imageFlag = True
        return heuristicMatrix
    
    def _generateVariableMatrixSet(self, intensityMatrix):
        """dict _generateFuzzyVariableMatrices(numpy.array intensityMatrix)"""
        variableMatrix = {}
        convolutionMask = {} 
        convolutionMask['mRow'] = N.array([[1,1,1],[-2,-2,-2],[1,1,1]])/3.
        convolutionMask['mCol'] = N.array([[1,-2,1],[1,-2,1],[1,-2,1]])/3.
        convolutionMask['iDiag'] = N.array([[1,1,1],[1,-8,1],[1,1,1]]) 
        for v in convolutionMask.keys():
            variableMatrix[v] = N.abs(self._mathTools.convolve(intensityMatrix, convolutionMask[v]))
        return variableMatrix