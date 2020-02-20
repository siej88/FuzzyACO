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

from PyQt4 import QtGui as gui
from PyQt4 import QtCore as cor
from PyQt4 import uic

import ImageHandler as imh
import QImageHandler as qim

class BinaryDialog(gui.QDialog):
    """Image Binarization Dialog"""
    
    def __init__(self, parent, imageMatrix, defaultThreshold):
        """BinaryDialog BinaryDialog()"""
        gui.QDialog.__init__(self, parent)
        self.ui = uic.loadUi('binary.ui')
        self.ui.show()
        
        self._imageMatrix = imageMatrix
        self._binarizedMatrix = None
        self._defaultThreshold = defaultThreshold
        
        self.ui.thresholdSlider.setValue(defaultThreshold)
        self.ui.thresholdBox.setValue(defaultThreshold)
        
        self._imageHandler = imh.ImageHandler()
        self._qImageHandler = qim.QImageHandler()
        
        self._width = self.ui.binaryLabel.width()
        self._height = self.ui.binaryLabel.height()
        
        self.ui.connect(self.ui.closeButton, cor.SIGNAL('clicked()'), cor.SLOT('close()'))
        self.ui.connect(self.ui.resetButton, cor.SIGNAL('clicked()'), self.resetThreshold)
        self.ui.connect(self.ui.saveButton, cor.SIGNAL('clicked()'), self.saveImage)
        self.ui.connect(self.ui.updateButton, cor.SIGNAL('clicked()'), self.updateImage)
        self.ui.connect(self.ui.thresholdSlider, cor.SIGNAL('valueChanged(int)'), self.setThresholdBox)
        self.ui.connect(self.ui.thresholdBox, cor.SIGNAL('valueChanged(int)'), self.setThresholdSlider)
        
        self.updateImage()

    def setThresholdSlider(self):
        """setThresholdSlider()"""
        value = self.ui.thresholdBox.value()
        self.ui.thresholdSlider.setValue(value)

    def setThresholdBox(self):
        """setThresholdBox()"""
        value = self.ui.thresholdSlider.value()
        self.ui.thresholdBox.setValue(value)
        
    def resetThreshold(self):
        """resetThreshold()"""
        self.ui.thresholdSlider.setValue(self._defaultThreshold)
        self.updateImage()

    def updateImage(self):
        """updateImage()"""
        value = self.ui.thresholdSlider.value()
        self._binarizedMatrix = self._imageHandler.binarizeMatrix(self._imageMatrix, value/255.)
        pixmap = self._qImageHandler.getQPixmap(self._binarizedMatrix)
        width = self.ui.binaryLabel.width()
        height = self.ui.binaryLabel.height()
        pixmap = self._qImageHandler.scaleQPixmap(pixmap, width, height)
        self.ui.binaryLabel.setPixmap(pixmap)
    
    def saveImage(self):
        """saveImage()"""
        caption = 'Seleccionar Nombre y Directorio de Destino'
        directory = ''
        filters = 'Portable Network Graphics (*.png)'
        path = gui.QFileDialog.getSaveFileName(self, caption, directory, filters)
        if (len(path) > 0):
            self._imageHandler.saveImage(self._binarizedMatrix, path)