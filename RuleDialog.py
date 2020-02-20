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

class RuleDialog(gui.QDialog):
    """Fuzzy Rule Manager"""
    
    def __init__(self, parent, rules, categories):
        """RuleDialog RuleDialog(PyQt4.QtGui.QWidget parent,
        list rules, dict categories)"""
        gui.QDialog.__init__(self, parent)
        self.ui = uic.loadUi('rules.ui')
        self.ui.show()

        self._ruleSet = rules
        self._categorySet = categories
        
        dataHandler = dat.DataHandler()
        reversedSet = dataHandler.revertCategorySet(categories)
        dataHandler.sortReversedCategorySet(reversedSet, categories)
        self._reversedSet = reversedSet
        
        self._setRuleList()
        self._setVariableList()
        self._setVariableBox()
        self._setCategoryBox()

        self.ui.connect(self.ui.closeButton, cor.SIGNAL('clicked()'), cor.SLOT('close()'))

        self.ui.connect(self.ui.ruleList, cor.SIGNAL('itemSelectionChanged()'), self._setVariableList)
        self.ui.connect(self.ui.variableList, cor.SIGNAL('currentTextChanged(const QString&)'), self._setVariableBox)
        self.ui.connect(self.ui.variableBox, cor.SIGNAL('currentIndexChanged(int)'), self._setCategoryBox)
        self.ui.connect(self.ui.variableBox, cor.SIGNAL('activated(int)'), self._updateCategoryBox)
        self.ui.connect(self.ui.categoryBox, cor.SIGNAL('activated(int)'), self._getVariable)
        
        self.ui.connect(self.ui.ruleDeleteButton, cor.SIGNAL('clicked()'), self.deleteRule)
        self.ui.connect(self.ui.ruleAddButton, cor.SIGNAL('clicked()'), self.addRule)
        self.ui.connect(self.ui.variableDeleteButton, cor.SIGNAL('clicked()'), self.deleteVariable)
        self.ui.connect(self.ui.variableAddButton, cor.SIGNAL('clicked()'), self.addVariable)
        
        qImageHandler = qih.QImageHandler()
        self.ui.ruleAddButton.setIcon(qImageHandler.getQIcon('resources\\add.png'))
        self.ui.variableAddButton.setIcon(qImageHandler.getQIcon('resources\\add.png'))
        self.ui.ruleDeleteButton.setIcon(qImageHandler.getQIcon('resources\\sub.png'))
        self.ui.variableDeleteButton.setIcon(qImageHandler.getQIcon('resources\\sub.png'))

    def deleteRule(self):
        """deleteRule()"""
        ruleCount = len(self._ruleSet)
        if ruleCount > 1:
            ruleIndex = self.ui.ruleList.currentRow()
            currentRule = self._ruleSet[ruleIndex]
            self._ruleSet.remove(currentRule)
            if (ruleIndex > 0):
                self.ui.ruleList.setCurrentRow(ruleIndex - 1)
                self._updateRuleList(ruleIndex - 1, 0)
            else:
                self._updateRuleList(ruleIndex, 0)

    def addRule(self):
        """addRule()"""
        ruleIndex = self.ui.ruleList.currentRow()
        rule = list(self._ruleSet[ruleIndex])
        self._ruleSet.insert(ruleIndex, rule)
        self._updateRuleList(ruleIndex + 1, 0)

    def deleteVariable(self):
        """deleteVariable()"""
        ruleIndex = self.ui.ruleList.currentRow()
        variableIndex = self.ui.variableList.currentRow()
        currentCategory = self._ruleSet[ruleIndex][variableIndex]
        variable = self._categorySet[currentCategory]['variable']
        if variable != 'edge':
            variableCount = len(self._ruleSet[ruleIndex])
            if variableCount > 2:
                self._ruleSet[ruleIndex].remove(currentCategory)
                if (variableIndex > 0):
                    self.ui.variableList.setCurrentRow(variableIndex - 1)
                    self._updateRuleList(ruleIndex, variableIndex - 1)
                else:
                    self._updateRuleList(ruleIndex, variableIndex)

    def _setRuleList(self):
        """_setRuleList()"""
        self._generateRuleListItems()
        if (self.ui.ruleList.count() > 0):
            self.ui.ruleList.setCurrentRow(0)
    
    def _updateRuleList(self, ruleIndex, variableIndex):
        """_updateRuleList(int ruleIndex, int variableIndex)"""
        self._generateRuleListItems()
        if (self.ui.ruleList.count() > 0):
            self.ui.ruleList.setCurrentRow(ruleIndex)
        if (self.ui.variableList.count() > 0):
            self.ui.variableList.setCurrentRow(variableIndex)
    
    def _generateRuleListItems(self):
        """_generateRuleListItems()"""
        self.ui.ruleList.clear()
        ruleCount = len(self._ruleSet)
        for i in xrange(ruleCount):
            prefix = 'SI  '
            suffix = 'ENTONCES  edge es '
            variableCount = len(self._ruleSet[i])
            for j in xrange(variableCount):
                category = self._ruleSet[i][j]
                variable = self._categorySet[category]['variable']
                if (variable == 'edge'):
                    suffix += category
                else:
                    prefix += variable + ' es ' + category + '  '
            self.ui.ruleList.addItem(prefix + suffix)
    
    def _setVariableList(self):
        """_setVariableList()"""
        self.ui.variableList.clear()
        rule = self.ui.ruleList.currentRow()
        variableCount = len(self._ruleSet[rule])
        for i in xrange(variableCount):
            item = self._ruleSet[rule][i]
            variable = self._categorySet[item]['variable']
            self.ui.variableList.addItem(variable +' es '+item)
        if (self.ui.variableList.count() > 0):
            self.ui.variableList.setCurrentRow(0)

    def addVariable(self):
        """addVariable()"""
        ruleIndex = self.ui.ruleList.currentRow()
        variableIndex = self.ui.variableList.currentRow()
        currentCategory = self._ruleSet[ruleIndex][variableIndex]
        variable = self._categorySet[currentCategory]['variable']
        if variable != 'edge':
            category = currentCategory
        else:
            category = self._reversedSet['mRow'][0]
        variableIndex = len(self._ruleSet[ruleIndex]) - 1
        self._ruleSet[ruleIndex].insert(variableIndex, category)
        self._updateRuleList(ruleIndex, variableIndex)

    def _setVariableBox(self):
        """setVariableBox()"""
        currentRule = self.ui.ruleList.currentRow()
        currentVariable = self.ui.variableList.currentRow()
        categoryName = self._ruleSet[currentRule][currentVariable]
        selection = self._categorySet[categoryName]['variable']
        variableList = ['mRow', 'mCol', 'iDiag']
        self.ui.variableBox.clear()
        if selection == 'edge':
            self.ui.variableBox.addItem('edge')
            self.ui.variableBox.setCurrentIndex(0)
        else:
            self.ui.variableBox.addItems(variableList)
            index = variableList.index(selection)
            self.ui.variableBox.setCurrentIndex(index)
    
    def _setCategoryBox(self):
        """_setCategoryBox()"""
        self.ui.categoryBox.clear()
        currentRule = self.ui.ruleList.currentRow()
        currentVariable = self.ui.variableList.currentRow()
        categoryName = self._ruleSet[currentRule][currentVariable]
        variable = self._categorySet[categoryName]['variable']
        categoryList = self._reversedSet[variable]
        self.ui.categoryBox.addItems(categoryList)
        index = categoryList.index(categoryName)
        self.ui.categoryBox.setCurrentIndex(index)
   
    def _updateCategoryBox(self):
        """_updateCategoryBox()"""
        self.ui.categoryBox.clear()
        variable = self.ui.variableBox.currentText()
        categoryList = self._reversedSet[variable]
        self.ui.categoryBox.addItems(categoryList)
        self.ui.categoryBox.setCurrentIndex(0)
        self._getVariable()
    
    def _getVariable(self):
        """_getVariable()"""
        currentRule = self.ui.ruleList.currentRow()
        currentVariable = self.ui.variableList.currentRow()
        categoryName = self.ui.categoryBox.currentText()
        self._ruleSet[currentRule][currentVariable] = categoryName
        self._updateRuleList(currentRule, currentVariable)