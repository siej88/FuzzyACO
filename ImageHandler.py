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
import Image as img

class ImageHandler(object):
    """Image File and Image Manipulator"""
    
    def getGrayscaleMatrix(self, path):
        """numpy.array getGrayscaleMatrix(str path)"""
        inputImage = img.open(path).convert('L')
        grayscaleMatrix = N.array(inputImage)/255.
        return N.copy(grayscaleMatrix)
    
    def saveImage(self, matrix, path):
        """saveImage(numpy.array matrix, str path)"""
        outputImage = img.fromarray(N.uint8(matrix*255))
        outputImage.save(path)
    
    def saveImages(self, matrix, segments, path, name = ''):
        """saveImages(numpy.array matrix, list segments, str path[, str name=''])"""
        if name != '':
            name = name + ' '
        width = len(matrix[0])
        segment = list(segments)
        segment.sort()
        segment = N.floor(N.array(segment)*width)
        count = len(segment)
        anchor = 0
        for i in xrange(count):
            current = segment[i]
            if(current - anchor > 0):
                partialMatrix = matrix[:,anchor:current]
                fullPath = path + '\\' + name + str(i) + '.png'
                self.saveImage(partialMatrix, fullPath)
                anchor = current
    
    def computeIsodata(self, matrix):
        """float computeIsodata(numpy.array matrix)"""
        currentThreshold = N.mean(matrix)
        previousThreshold = 0
        while(N.abs(currentThreshold - previousThreshold) > 0.0001):
            previousThreshold = currentThreshold
            m = N.mean(matrix[N.where(matrix > currentThreshold)])
            n = N.mean(matrix[N.where(matrix <= currentThreshold)])
            currentThreshold = 0.5*m+0.5*n
        return currentThreshold
    
    def binarizeMatrix(self, matrix, threshold):
        """numpy.array binarizeMatrix(self, numpy.array matrix, float threshold)"""
        binarizedMatrix = N.zeros_like(matrix)
        binarizedMatrix[N.where(matrix > threshold)] = 1.
        binarizedMatrix[N.where(matrix <= threshold)] = 0.
        return N.copy(binarizedMatrix)