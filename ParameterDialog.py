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

import QImageHandler as qim

class ParameterDialog(gui.QDialog):
    """Parameter Management Dialog"""
        
    def __init__(self, parent, parameters, ants = 0):
        """ParameterDialog ParameterDialog(PyQt4.QtGui.QWidget parent,
        dict parameters, int ants=0)"""
        gui.QDialog.__init__(self, parent)
        self.ui = uic.loadUi('parameters.ui')
        self.ui.show()
       
        self._parameterSet = parameters
        self._setParameters(self._parameterSet)
        self._antCountHint = ants

        self.ui.connect(self.ui.closeButton, cor.SIGNAL('clicked()'), cor.SLOT('close()'))
        self.ui.connect(self.ui.autoButton, cor.SIGNAL('clicked()'), self.autoCount)

        self.ui.connect(self.ui.antCountBox, cor.SIGNAL('valueChanged(int)'), self.applyParameters)
        self.ui.connect(self.ui.cycleCountBox, cor.SIGNAL('valueChanged(int)'), self.applyParameters)
        self.ui.connect(self.ui.stepCountBox, cor.SIGNAL('valueChanged(int)'), self.applyParameters)
        self.ui.connect(self.ui.alphaBox, cor.SIGNAL('valueChanged(double)'), self.applyParameters)
        self.ui.connect(self.ui.betaBox, cor.SIGNAL('valueChanged(double)'), self.applyParameters)
        self.ui.connect(self.ui.deltaBox, cor.SIGNAL('valueChanged(double)'), self.applyParameters)
        self.ui.connect(self.ui.tuningBox, cor.SIGNAL('valueChanged(double)'), self.applyParameters)
        self.ui.connect(self.ui.rhoBox, cor.SIGNAL('valueChanged(double)'), self.applyParameters)
        self.ui.connect(self.ui.psiBox, cor.SIGNAL('valueChanged(double)'), self.applyParameters)
        self.ui.connect(self.ui.lomRadioButton, cor.SIGNAL('toggled(bool)'), self.applyParameters)
        self.ui.connect(self.ui.momRadioButton, cor.SIGNAL('toggled(bool)'), self.applyParameters)
        self.ui.connect(self.ui.somRadioButton, cor.SIGNAL('toggled(bool)'), self.applyParameters)
        self.ui.connect(self.ui.coaRadioButton, cor.SIGNAL('toggled(bool)'), self.applyParameters)
        self.ui.connect(self.ui.deterministicRadioButton, cor.SIGNAL('toggled(bool)'), self.applyParameters)
        self.ui.connect(self.ui.nonDeterministicRadioButton, cor.SIGNAL('toggled(bool)'), self.applyParameters)
        
        qImageHandler = qim.QImageHandler()
        self.ui.autoButton.setIcon(qImageHandler.getQIcon('resources\\auto.png'))
    
    def applyParameters(self):
        """applyParameters()"""
        self._getParameters()
    
    def autoCount(self):
        """autoCount()"""
        self.ui.antCountBox.setValue(self._antCountHint)

    def _setParameters(self, parameterSet):
        """_setParameters(dict parameterSet)"""
        self.ui.antCountBox.setValue(parameterSet['antCount'])
        self.ui.cycleCountBox.setValue(parameterSet['cycleCount'])
        self.ui.stepCountBox.setValue(parameterSet['stepCount'])
        self.ui.alphaBox.setValue(parameterSet['alpha'])
        self.ui.betaBox.setValue(parameterSet['beta'])
        self.ui.deltaBox.setValue(parameterSet['delta'])
        self.ui.tuningBox.setValue(parameterSet['tuning'])
        self.ui.rhoBox.setValue(parameterSet['rho'])
        self.ui.psiBox.setValue(parameterSet['psi'])
        self._setDeFuzzificationMode(parameterSet['deFuzzificationMode'])
        self._setAntMovementMode(parameterSet['antMovementMode'])
    
    def _getParameters(self):
        """_getParameters()"""
        self._parameterSet['antCount'] = self.ui.antCountBox.value()
        self._parameterSet['cycleCount'] = self.ui.cycleCountBox.value()
        self._parameterSet['stepCount'] = self.ui.stepCountBox.value()
        self._parameterSet['alpha'] = self.ui.alphaBox.value()
        self._parameterSet['beta'] = self.ui.betaBox.value()
        self._parameterSet['delta'] = self.ui.deltaBox.value()
        self._parameterSet['tuning'] = self.ui.tuningBox.value()
        self._parameterSet['rho'] = self.ui.rhoBox.value()
        self._parameterSet['psi'] = self.ui.psiBox.value()
        self._getDeFuzzificationMode()
        self._getAntMovementMode()
    
    def _setDeFuzzificationMode(self, mode):
        """_setDeFuzzificationMode(int mode)"""
        if mode == -1:
            self.ui.somRadioButton.setChecked(True)
        elif mode == 0:
            self.ui.momRadioButton.setChecked(True)
        elif mode == 1:
            self.ui.lomRadioButton.setChecked(True)
        elif mode == 2:
            self.ui.coaRadioButton.setChecked(True)
    
    def _getDeFuzzificationMode(self):
        """_getDeFuzzificationMode()"""
        if self.ui.somRadioButton.isChecked():
            self._parameterSet['deFuzzificationMode'] = -1
        elif self.ui.momRadioButton.isChecked():
            self._parameterSet['deFuzzificationMode'] = 0
        elif self.ui.lomRadioButton.isChecked():
            self._parameterSet['deFuzzificationMode'] = 1
        elif self.ui.coaRadioButton.isChecked():
            self._parameterSet['deFuzzificationMode'] = 2
    
    def _setAntMovementMode(self, mode):
        """_setAntMovementMode(int mode)"""
        if mode == 1:
            self.ui.deterministicRadioButton.setChecked(True)
        elif mode == 0:
            self.ui.nonDeterministicRadioButton.setChecked(True)
    
    def _getAntMovementMode(self):
        """_getAntMovementMode()"""
        if self.ui.deterministicRadioButton.isChecked():
            self._parameterSet['antMovementMode'] = 1
        elif self.ui.nonDeterministicRadioButton.isChecked():
            self._parameterSet['antMovementMode'] = 0