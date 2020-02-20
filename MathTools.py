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
import scipy.signal as sig
import scipy.ndimage.filters as flt

class MathTools(object):
    """Mathematical Toolset"""
    
    def maximum(self, matrixList):
        """numpy.array maximum(list matrixList)"""
        matrixCount = len(matrixList)
        if matrixCount > 1:
            for i in xrange(matrixCount-1):
                matrixList[i+1] = N.maximum(matrixList[i+1], matrixList[i])
            return matrixList[matrixCount-1]
        else:
            return matrixList[0]

    def minimum(self, matrixList):
        """numpy.array minimum(list matrixList)"""
        matrixCount = len(matrixList)
        if matrixCount > 1:
            for i in xrange(matrixCount-1):
                matrixList[i+1] = N.minimum(matrixList[i+1], matrixList[i])
            return matrixList[matrixCount-1]
        else:
            return matrixList[0]

    def gaussian(self, X, mean, scale):
        """numpy.array gaussian(numpy.array X, float mean, float scale)"""
        return N.exp(-N.square(X-N.ones(X.shape)*mean)*0.5/scale**2)
    
    def inverseGaussian(self, X, mean, scale, mode):
        """numpy.array inverseGaussian(numpy.array X, float mean, float scale, int mode)"""
        return N.ones(X.shape)*mean + mode*scale*N.sqrt(2.*N.log(N.reciprocal(X)))
    
    def mean(self, inputMatrix):
        """numpy.array mean(numpy.array inputMatrix)"""
        convolutionMask = N.ones((3,3))
        return self.convolve(inputMatrix, convolutionMask)/9.
    
    def standardDeviation(self, inputMatrix):
        """numpy.array standardDeviation(numpy.array inputMatrix)"""
        squareMatrix = N.square(inputMatrix)
        convolutionMask = N.ones((3,3))
        EX2_Matrix = self.convolve(squareMatrix, convolutionMask)/9.
        E2X_Matrix = self.convolve(inputMatrix, convolutionMask)/9.
        return N.sqrt(N.abs(EX2_Matrix-E2X_Matrix**2))

    def gradient(self, inputMatrix, horizontalWeight = 1., verticalWeight = 1.):
        """numpy.array gradient(numpy.array inputMatrix,
        float horizontalWeight = 1., float verticalWeight = 1.)"""
        horizontalMask = N.array([[0, 0, 0], [-1, 0, 1], [0, 0, 0]])*horizontalWeight
        verticalMask = N.array([[0, -1, 0], [0, 0, 0], [0, 1, 0]])*verticalWeight
        horizontalMatrix = self.convolve(inputMatrix, horizontalMask)
        verticalMatrix = self.convolve(inputMatrix, verticalMask)
        gradientMatrix = N.sqrt(N.square(horizontalMatrix) + N.square(verticalMatrix))
        return gradientMatrix
    
    def gaussianFilter(self, inputMatrix, standardDeviation = 1.):
        """numpy.array gaussianFilter(numpy.array inputMatrix, float standardDeviation = 1.)"""
        return flt.gaussian_filter(inputMatrix, standardDeviation)
    
    def normalize(self, inputMatrix):
        """numpy.array normalize(numpy.array inputMatrix)"""
        normalizedMatrix = N.copy(inputMatrix)
        normalizedMatrix[N.where(inputMatrix < 0.)] = 0.
        normalizedMatrix[N.where(inputMatrix > 1.)] = 1.
        return normalizedMatrix

    def convolve(self, matrix, mask):
        """numpy.array convolve(numpy.array matrix, numpy.array mask)"""
        return sig.convolve2d(matrix, mask, 'same', 'symm')

