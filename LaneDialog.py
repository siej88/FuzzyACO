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

import os
from PyQt4 import QtGui as gui
from PyQt4 import QtCore as cor
from PyQt4 import uic

import ImageHandler as imh
import QImageHandler as qim

class LaneDialog(gui.QDialog):
    """Image Lane Separation Dialog"""
    
    def __init__(self, parent, matrix):
        """LaneDialog LaneDialog(PyQt4.QtGui.QWidget parent, numpy.array matrix)"""
        gui.QDialog.__init__(self, parent)
        self.ui = uic.loadUi('lanes.ui')
        self.ui.show()
        
        self.ui.connect(self.ui.closeButton, cor.SIGNAL('clicked()'), cor.SLOT('close()'))
        self.ui.connect(self.ui.addButton, cor.SIGNAL('clicked()'), self.addLane)
        self.ui.connect(self.ui.undoButton, cor.SIGNAL('clicked()'), self.undoLane)
        self.ui.connect(self.ui.clearButton, cor.SIGNAL('clicked()'), self.clearLanes)
        self.ui.connect(self.ui.saveButton, cor.SIGNAL('clicked()'), self.saveLanes)
        
        self._imageMatrix = matrix
        self._imageWidth = 0
        self._imageStack = []
        self._laneSegments = []
        
        self._imageHandler = imh.ImageHandler()
        self._qImageHandler = qim.QImageHandler()

        pixmap = self._qImageHandler.getQPixmap(matrix)
        self._imageStack.append(self._resizePixmap(pixmap))
        self._setPixmap(self._imageStack[0])
        self._imageWidth = pixmap.width()
        self.ui.laneSlider.setMaximum(self._imageWidth)
    
    def addLane(self):
        """addLane()"""
        index = len(self._imageStack) - 1
        pixmap = self._imageStack[index].copy()
        
        width = self.ui.laneLabel.width()
        height = self.ui.laneLabel.height()
        
        value = float(self.ui.laneSlider.value())
        laneValue = value/self._imageWidth
        value = int(laneValue*width)

        painted = self._qImageHandler.drawLine(pixmap, value, 0, value, height)
        self._imageStack.append(painted)
        self._laneSegments.append(laneValue)
        self._setPixmap(painted)
    
    def undoLane(self):
        """undoLane()"""
        count = len(self._imageStack)
        if (count > 1):
            self._laneSegments.pop()
            self._imageStack.pop()
            pixmap = self._imageStack[count - 2]
            self._setPixmap(pixmap)

    def clearLanes(self):
        """clearLanes()"""
        count = len(self._imageStack)
        while(count > 1):
            self._laneSegments.pop()
            self._imageStack.pop()
            count -= 1
        pixmap = self._imageStack[0]
        self._setPixmap(pixmap)

    def saveLanes(self):
        """saveLanes()"""
        self.ui.messageLabel.setText('Guardando Imagenes...')
        path = gui.QFileDialog.getSaveFileName(caption = 'Seleccionar Nombre y Directorio de Destino')
        if (len(path) > 0):
            segments = list(self._laneSegments)
            segments.append(1)
            name = os.path.basename(path)
            path = os.path.dirname(path)
            self._imageHandler.saveImages(self._imageMatrix, segments, path, name)
        self.ui.messageLabel.setText('Activo.')

    def _resizePixmap(self, pixmap):
        """PyQt4.QtGui.QPixmap _resizePixmap(PyQt4.QtGui.QPixmap pixmap)"""
        width = self.ui.laneLabel.width()
        height = self.ui.laneLabel.height()
        return self._qImageHandler.resizeQPixmap(pixmap, width, height)

    def _setPixmap(self, pixmap):
        """_setPixmap(PyQt4.QtGui.QPixmap pixmap)"""
        self.ui.laneLabel.setPixmap(pixmap)