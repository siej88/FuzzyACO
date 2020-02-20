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

import time
import math
from PyQt4 import QtGui as gui
from PyQt4 import QtCore as cor
from PyQt4 import uic

import DataHandler as dat
import ImageHandler as imh
import QImageHandler as qih

import FuzzyMachine as fm
import AntColonyOptimizer as aco

import LaneDialog as lad
import ParameterDialog as pad
import RuleDialog as rud
import BinaryDialog as bid
import CategoryDialog as cad
import HelpDialog as hed

class MainWindow(gui.QMainWindow):
    """FuzzyACO GUI"""

    def __init__(self):
        """MainWindow MainWindow()"""
        gui.QMainWindow.__init__(self)
        self.ui = uic.loadUi('fuzzyaco.ui')
        self.ui.statusBar().showMessage('Activo.')
        self.ui.show()
        
        self.ui.connect(self.ui.exitButton, cor.SIGNAL('clicked()'), gui.qApp, cor.SLOT('quit()'))
        self.ui.connect(self.ui.imageButton, cor.SIGNAL('clicked()'), self.loadImage)
        self.ui.connect(self.ui.laneButton, cor.SIGNAL('clicked()'), self.openLaneDialog)
        self.ui.connect(self.ui.parameterButton, cor.SIGNAL('clicked()'), self.openParameterDialog)
        self.ui.connect(self.ui.fuzzyRuleButton, cor.SIGNAL('clicked()'), self.openRuleDialog)
        self.ui.connect(self.ui.fuzzyCategoryButton, cor.SIGNAL('clicked()'), self.openCategoryDialog)
        self.ui.connect(self.ui.loadConfigurationButton, cor.SIGNAL('clicked()'), self.loadConfiguration)
        self.ui.connect(self.ui.saveConfigurationButton, cor.SIGNAL('clicked()'), self.saveConfiguration)
        self.ui.connect(self.ui.runButton, cor.SIGNAL('clicked()'), self.runFuzzyACO)
        self.ui.connect(self.ui.binaryButton, cor.SIGNAL('clicked()'), self.openBinaryDialog)
        self.ui.connect(self.ui.helpButton, cor.SIGNAL('clicked()'), self.openHelpDialog)
        
        self._dataHandler = dat.DataHandler()
        self._imageHandler = imh.ImageHandler()
        self._qImageHandler = qih.QImageHandler()

        self._fuzzyMachine = fm.FuzzyMachine()
        self._antColonyOptimizer = aco.AntColonyOptimizer()

        self._parameterSet = {}
        self._categorySet = {}
        self._ruleSet = []

        self._loadConfiguration('config\\default.cfg')
        
        self._imageMatrix = None
        self._imageFlag = False
        self._binaryFlag = False
        self._isoData = 0
    
    def loadImage(self):
        """loadImage()"""
        self._showMessage('Cargando Imagen...')
        path = self._openImageFile()
        if(len(path) > 0):
            self._imageMatrix = self._imageHandler.getGrayscaleMatrix(path)
            imageQPixmap = self._qImageHandler.getQPixmap(self._imageMatrix)
            pixmap = self._scalePixmap(imageQPixmap)
            self.ui.imageLabel.setPixmap(pixmap)
            self._imageFlag = True
            self._binaryFlag = False
        self._showMessage('Activo.')
    
    def runFuzzyACO(self):
        """runFuzzyACO()"""
        if (self._imageFlag == False):
            self._showMessage('Debe cargar una imagen primero.')
        else:
            maxAnts = self._getMaxAntCount()
            if (self._parameterSet['antCount'] > maxAnts):
                self._showMessage('Debe reducir cantidad de hormigas (Max = '+ str(maxAnts) + ').')
            else:
                self._setGUI(False)
                self._showMessage('Procesando...')                
                start = time.time()
                heuristicMatrix = self._fuzzyMachine.generateHeuristicMatrix(self._imageMatrix, self._categorySet, self._parameterSet, self._ruleSet)
                pheromoneMatrix = self._antColonyOptimizer.generatePheromoneMatrix(self._imageMatrix, heuristicMatrix, self._parameterSet)
                self._isoData = int(self._imageHandler.computeIsodata(pheromoneMatrix)*255)
                bid.BinaryDialog(self, pheromoneMatrix, self._isoData)
                end = time.time()
                runTime = end - start
                self._showMessage('Ejecucion Finalizada. Tiempo = ' + str(runTime))  
                log = open('runlog.txt', 'a')
                log.write(str(runTime) + '\n')
                log.close()                              
                self._setGUI(True)
                self._binaryFlag = True
    
    def openBinaryDialog(self):
        """openBinaryDialog()"""
        if (self._binaryFlag == True):
            pheromoneMatrix = self._antColonyOptimizer.getPheromoneMatrix()
            bid.BinaryDialog(self, pheromoneMatrix, self._isoData)
        else:
            self._showMessage('Debe ejecutar el programa primero.')
        
    def openLaneDialog(self):
        """openLaneDialog()"""
        if self._imageFlag == False:
            self._showMessage('Debe cargar una imagen primero.')
        else:
            lad.LaneDialog(self, self._imageMatrix)
            self._showMessage('Activo.')

    def openParameterDialog(self):
        """openParameterDialog()"""
        antCountHint = self._getAntCountHint()
        pad.ParameterDialog(self, self._parameterSet, antCountHint)
    
    def openRuleDialog(self):
        """openRuleDialog()"""
        rud.RuleDialog(self, self._ruleSet, self._categorySet)
    
    def openCategoryDialog(self):
        """openCategoryDialog()"""
        cad.CategoryDialog(self, self._ruleSet, self._categorySet)
    
    def loadConfiguration(self):
        """loadConfiguration()"""
        self._showMessage('Cargando Configuracion...')
        caption = 'Seleccionar Archivo'
        directory = ''
        filters = 'Configuracion FuzzyACO (*.cfg)'
        path = gui.QFileDialog.getOpenFileName(self, caption, directory, filters)
        if len(path) > 0:
            self._loadConfiguration(path)
        self._showMessage('Activo.')
    
    def saveConfiguration(self):
        """saveConfiguration()"""
        self._showMessage('Guardando Configuracion...')
        caption = 'Seleccionar Archivo'
        directory = ''
        filters = 'Configuracion FuzzyACO (*.cfg)'
        path = gui.QFileDialog.getSaveFileName(self, caption, directory, filters)
        if len(path) > 0:
            self._dataHandler.saveConfiguration(path)
        self._showMessage('Activo.')
    
    def openHelpDialog(self):
        """openHelpDialog()"""
        hed.HelpDialog(self)
    
    def _getAntCountHint(self):
        """int _getAntCountHint()"""
        if self._imageFlag == True:
            height = self._imageMatrix.shape[0]
            width = self._imageMatrix.shape[1]           
            return int(math.sqrt(width*height))
        else:
            return 0
    
    def _getMaxAntCount(self):
        """int _getMaxAntCount()"""
        height = self._imageMatrix.shape[0]
        width = self._imageMatrix.shape[1]            
        return width*height
    
    def _setGUI(self, state):
        """_setGUI(bool state)"""
        self.ui.imageButton.setEnabled(state)
        self.ui.fuzzyCategoryButton.setEnabled(state)
        self.ui.fuzzyRuleButton.setEnabled(state)
        self.ui.parameterButton.setEnabled(state)
        self.ui.loadConfigurationButton.setEnabled(state)
        self.ui.saveConfigurationButton.setEnabled(state)
        self.ui.helpButton.setEnabled(state)
        self.ui.exitButton.setEnabled(state)
        self.ui.runButton.setEnabled(state)
        self.ui.laneButton.setEnabled(state)
        self.ui.binaryButton.setEnabled(state)
    
    def _loadConfiguration(self, path):
        """_loadConfiguration(str path)"""
        self._dataHandler.loadConfiguration(path)
        self._parameterSet = self._dataHandler.getParameters()
        self._ruleSet = self._dataHandler.getRules()
        self._categorySet = self._dataHandler.getCategories()
    
    def _scalePixmap(self, pixmap):
        """PyQt4.QtGui.QPixmap _scalePixmap(PyQt4.QtGui.QPixmap pixmap)"""
        width = self.ui.imageLabel.width()
        height = self.ui.imageLabel.height()
        return self._qImageHandler.scaleQPixmap(pixmap, width, height)
    
    def _openImageFile(self):
        """str _openImageFile()"""
        caption = 'Seleccionar Imagen'
        directory = ''
        filters = 'Archivos de Imagen (*.png *.jpg *.bmp)'
        path = gui.QFileDialog.getOpenFileName(self, caption, directory, filters)
        return path
    
    def _showMessage(self, message):
        """_showMessage(str message)"""
        self.ui.statusBar().showMessage(message)