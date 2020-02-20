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

import DataHandler as dat
import QImageHandler as qih

from PyQt4 import QtGui as gui
from PyQt4 import QtCore as cor
from PyQt4 import uic

class CategoryDialog(gui.QDialog):
    """Fuzzy Category Manager"""
    
    def __init__(self, parent, rules, categories):
        """CategoryDialog CategoryDialog(PyQt4.QtGui.QWidget parent,
        list rules, dict categories)"""
        gui.QDialog.__init__(self, parent)
        self.ui = uic.loadUi('categories.ui')
        self.ui.show()

        self._ruleSet = rules
        self._categorySet = categories
        self._reversedSet = {}
        
        self._dataHandler = dat.DataHandler()
        self._controlFlag = True
        self._nameSet = {'mRow': 0, 'mCol': 0, 'iDiag': 0, 'edge': 0}
        self._updateReversedSet()
        
        self._setVariables()
        self._setCategories()
        self._setParameters()
        
        self.ui.connect(self.ui.closeButton, cor.SIGNAL('clicked()'), cor.SLOT('close()'))
        self.ui.connect(self.ui.changeButton, cor.SIGNAL('clicked()'), self._changeCategory)
        
        self.ui.connect(self.ui.variableList, cor.SIGNAL('itemSelectionChanged()'), self._setCategories)
        self.ui.connect(self.ui.categoryList, cor.SIGNAL('itemSelectionChanged()'), self._setParameters)
        
        self.ui.connect(self.ui.categoryList, cor.SIGNAL('itemChanged(QListWidgetItem*)'), self._changeCategory)
        
        self.ui.connect(self.ui.meanBox, cor.SIGNAL('valueChanged(double)'), self._getParameters)
        self.ui.connect(self.ui.scaleBox, cor.SIGNAL('valueChanged(double)'), self._getParameters)
        
        self.ui.connect(self.ui.categoryAddButton, cor.SIGNAL('clicked()'), self._addCategory)
        self.ui.connect(self.ui.categoryDeleteButton, cor.SIGNAL('clicked()'), self._deleteCategory)
        
        qImageHandler = qih.QImageHandler()
        self.ui.categoryAddButton.setIcon(qImageHandler.getQIcon('resources\\add.png'))
        self.ui.categoryDeleteButton.setIcon(qImageHandler.getQIcon('resources\\sub.png'))
    
    def _updateReversedSet(self):
        """_updateReversedSet()"""
        reversedSet = self._dataHandler.revertCategorySet(self._categorySet)
        self._dataHandler.sortReversedCategorySet(reversedSet, self._categorySet)
        self._reversedSet = reversedSet
    
    def _setVariables(self):
        """_setVariables()"""
        if (self.ui.variableList.count() == 0):
            for variable in ['mRow', 'mCol', 'iDiag', 'edge']:
                self.ui.variableList.addItem(variable)
                self.ui.variableBox.addItem(variable)
        self.ui.variableList.setCurrentRow(0)
        self.ui.variableBox.setCurrentIndex(0)
    
    def _setCategories(self):
        """_setCategories()"""
        if (self._controlFlag):
            variable = self.ui.variableList.currentItem().text()
            self._generateCategoryListItems(variable)
            self.ui.categoryList.setCurrentRow(0)
            index = self.ui.variableBox.findText(variable)
            self.ui.variableBox.setCurrentIndex(index)
    
    def _generateCategoryListItems(self, variable):
        """_generateCategoryListItems(str variable)"""
        categories = self._reversedSet[variable]
        self.ui.categoryList.clear()
        for category in categories:
            cat = gui.QListWidgetItem(category)
            cat.setFlags(cat.flags() | cor.Qt.ItemIsEditable)
            self.ui.categoryList.addItem(cat)
    
    def _setParameters(self):
        """_setParameters()"""
        if (self._controlFlag):
            category = self.ui.categoryList.currentItem().text()
            mean = self._categorySet[category]['mean']
            scale = self._categorySet[category]['scale']
            self.ui.meanBox.setValue(mean)
            self.ui.scaleBox.setValue(scale)
            self.ui.nameDisplayLabel.setText(category)
    
    def _getParameters(self):
        """_getParameters()"""
        if (self._controlFlag):
            category = self.ui.categoryList.currentItem().text()
            mean = self.ui.meanBox.value()
            scale = self.ui.scaleBox.value()
            self._categorySet[category]['mean'] = mean
            self._categorySet[category]['scale'] = scale
            self._updateReversedSet()
    
    def _changeCategory(self):
        """_changeCategory()"""
        newName = self.ui.categoryList.currentItem().text()
        currentName = self.ui.nameDisplayLabel.text()
        currentVariable = self.ui.variableList.currentItem().text()
        newVariable = self.ui.variableBox.currentText()
        mean = self.ui.meanBox.value()
        scale = self.ui.scaleBox.value()
        newCategory = {}
        newCategory['variable'] = newVariable
        newCategory['mean'] = mean
        newCategory['scale'] = scale
        categoryCount = self.ui.categoryList.count()
        nameStatus = self._checkName(newName)
        sameName = newName == currentName
        sameVariable = newVariable == currentVariable
        if (sameName and not sameVariable and nameStatus != 1):
            nameStatus = 0
        if (not sameName and sameVariable and nameStatus != 1 and categoryCount == 1):
            nameStatus = 0
            categoryCount = 2
        if (nameStatus == 0 and categoryCount > 1):
            self._categorySet.pop(currentName)
            self._categorySet[newName] = newCategory
            self._replaceInRules(currentName, newName)
            self._showMessage()
        else:
            newVariable = currentVariable
            newName = currentName
            if (categoryCount <= 1):
                self._showMessage(3)
            else:
                self._showMessage(nameStatus)
        self._updateReversedSet()
        self._updateSelection(newVariable, newName)
    
    def _addCategory(self):
        """addCategory()"""
        currentVariable = self.ui.variableList.currentItem().text()
        newName = str(currentVariable)
        while (self._checkName(newName + str(self._nameSet[newName])) != 0):
            self._nameSet[newName] += 1
        newName += str(self._nameSet[newName])
        newVariable = self.ui.variableBox.currentText()
        mean = self.ui.meanBox.value()
        scale = self.ui.scaleBox.value()
        newCategory = {}
        newCategory['variable'] = newVariable
        newCategory['mean'] = mean
        newCategory['scale'] = scale
        self._categorySet[newName] = newCategory
        self._updateReversedSet()
        self._updateSelection(newVariable, newName)        
    
    def _deleteCategory(self):
        """deleteCategory()"""
        newVariable = self.ui.variableList.currentItem().text()
        currentName = self.ui.categoryList.currentItem().text()
        categoryCount = self.ui.categoryList.count()
        index = self.ui.categoryList.currentRow() - 1
        if (index < 0): index += 2        
        if (categoryCount > 1):
            newName = self.ui.categoryList.item(index).text()
            self._showMessage(0)
            self._categorySet.pop(currentName)            
            self._updateReversedSet()
            self._removeFromRules(currentName)
            self._updateSelection(newVariable, newName)
        else:
            self._showMessage(3)
        
    def _checkName(self, name):
        """int _checkName(str name)"""
        if (not name.isalnum()): return 1
        nameList = list(self._categorySet.keys())
        if (nameList.count(name) > 0): return 2
        return 0
    
    def _showMessage(self, statusCode = 0):
        """_showMessage(int statusCode = 0)"""
        if (statusCode == 0):
            self.ui.messageLabel.setText('Activo.')
        if (statusCode == 1):
            self.ui.messageLabel.setText('Nombre solo puede contener letras y/o digitos.')
        if (statusCode == 2):
            self.ui.messageLabel.setText('No se permiten categorias con el mismo nombre.')
        if (statusCode == 3):
            self.ui.messageLabel.setText('Cada variable debe tener al menos una categoria.')
    
    def _updateSelection(self, variable, category):
        """_updateSelection(str variable, str category)"""
        self._controlFlag = False

        index = self.ui.variableBox.findText(variable)        
        self.ui.variableBox.setCurrentIndex(index)
        mean = self._categorySet[category]['mean']
        scale = self._categorySet[category]['scale']
        self.ui.meanBox.setValue(mean)
        self.ui.scaleBox.setValue(scale)
        self.ui.nameDisplayLabel.setText(category)
        
        variableItem = self.ui.variableList.findItems(variable, cor.Qt.MatchFixedString | cor.Qt.MatchCaseSensitive)
        index = self.ui.variableList.row(variableItem[0])
        self.ui.variableList.setCurrentRow(index)

        self._generateCategoryListItems(variable)
        
        categoryItem = self.ui.categoryList.findItems(category, cor.Qt.MatchFixedString | cor.Qt.MatchCaseSensitive)
        index = self.ui.categoryList.row(categoryItem[0])
        self.ui.categoryList.setCurrentRow(index)
        
        self._controlFlag = True

    def _replaceInRules(self, oldCategory, newCategory):
        """_replaceInRules(str oldCategory, str newCategory)"""
        ruleCount = len(self._ruleSet)
        for i in xrange(ruleCount):
            categoryCount = len(self._ruleSet[i])
            for j in xrange(categoryCount):
                category = self._ruleSet[i][j]
                if (category == oldCategory):
                    self._ruleSet[i][j] = newCategory
    
    def _removeFromRules(self, category):
        """_removeFromRules(str category)"""
        edgeCategories = list(self._reversedSet['edge'])
        nonEdgeCategories = list(self._reversedSet['mRow'])
        nonEdgeCategories.extend(self._reversedSet['mCol'])
        nonEdgeCategories.extend(self._reversedSet['iDiag'])
        ruleCount = len(self._ruleSet)
        for i in xrange(ruleCount):
            while(self._ruleSet[i].count(category) > 0):
                self._ruleSet[i].remove(category)
            hasEdge = False
            hasNonEdge = False
            categoryCount = len(self._ruleSet[i])
            for j in xrange(categoryCount):
                if (self._ruleSet[i][j] in nonEdgeCategories):
                    hasNonEdge = True
                if (self._ruleSet[i][j] in edgeCategories):
                    hasEdge = True
            if (hasEdge == False or hasNonEdge == False):
                self._ruleSet[i] = '<Remove>'
        while(self._ruleSet.count('<Remove>') > 0):
            self._ruleSet.remove('<Remove>')
        if (len(self._ruleSet) == 0):
            if (nonEdgeCategories.count(category) > 0):
                nonEdgeCategories.remove(category)
            elif (edgeCategories.count(category) > 0):
                edgeCategories.remove(category)
            self._ruleSet.append([nonEdgeCategories[0], edgeCategories[0]])
