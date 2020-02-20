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

class HelpDialog(gui.QDialog):
    """Help Center"""
  
    def __init__(self, parent):
        """HelpDialog HelpDialog(PyQt4.QtGui.QWidget parent)"""
        gui.QDialog.__init__(self, parent)
        self.ui = uic.loadUi('help.ui')
        self.ui.show()

        self.ui.connect(self.ui.closeButton, cor.SIGNAL('clicked()'), cor.SLOT('close()'))