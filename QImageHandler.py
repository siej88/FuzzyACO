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
from PyQt4 import QtGui as gui
from PyQt4 import QtCore as cor

class QImageHandler(object):
    """Qt Image Manipulator"""

    def getQPixmap(self, matrix):
        """PyQt4.QtGui.QPixmap getQPixmap(numpy.array matrix)"""
        image = img.fromarray(N.uint8(matrix*255))
        color = image.convert('RGBA')
        data = color.tostring('raw', 'RGBA')
        qImage = gui.QImage(data, image.size[0], image.size[1], gui.QImage.Format_ARGB32)
        qPixmap = gui.QPixmap(qImage)
        return qPixmap
    
    def scaleQPixmap(self, pixmap, width, height):
        """PyQt4.QtGui.QPixmap scaleQPixmap(PyQt4.QtGui.QPixmap pixmap, int width, int height)"""
        qPixmap = pixmap.scaled(width, height, cor.Qt.KeepAspectRatio, cor.Qt.FastTransformation)
        return qPixmap
        
    def resizeQPixmap(self, pixmap, width, height):
        """PyQt4.QtGui.QPixmap resizeQPixmap(PyQt4.QtGui.QPixmap pixmap, int width, int height)"""
        qPixmap = pixmap.scaled(width, height, cor.Qt.IgnoreAspectRatio, cor.Qt.FastTransformation)
        return qPixmap
    
    def drawLine(self, pixmap, x1, y1, x2, y2):
        """PyQt4.QtGui.QPixmap drawLine(PyQt4.QtGui.QPixmap pixmap,
            int x1, int y1, int x2, int y2)"""
        qPixmap = gui.QPixmap(pixmap)
        color = gui.QColor(255, 0, 0)
        painter = gui.QPainter()
        painter.begin(qPixmap)
        painter.setPen(color)
        painter.drawLine(x1, y1, x2, y2)
        painter.end()
        return qPixmap
    
    def getQIcon(self, path):
        """PyQt4.QtGui.QIcon getQIcon(str path)"""
        qIcon = gui.QIcon(path)
        return qIcon