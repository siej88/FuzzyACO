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

class DataHandler(object):
    """Data File Manipulator"""
    
    def __init___(self):
        """DataHandler Datahandler()"""
        self._categories = {}
        self._parameters = {}
        self._rules = []
        self._hasData = False
    
    def hasData(self):
        """bool hasData()"""
        return self._hasData

    def getCategories(self):
        """dict getCategories()"""
        return self._categories
    
    def getParameters(self):
        """dict getParameters()"""
        return self._parameters
    
    def getRules(self):
        """list getRules()"""
        return self._rules
    
    def revertCategorySet(self, categories):
        """dict revertCategorySetd(dict categories)"""
        reversedSet = {}
        for var in ['mRow', 'mCol', 'iDiag', 'edge']:
            reversedSet[var] = []
        keys = categories.keys()
        for key in keys:
            variable = categories[key]['variable']
            reversedSet[variable].append(key)
        return reversedSet
    
    def sortReversedCategorySet(self, reverse, categories):
        """sortReversedCategorySet(dict reverse, dict categories)"""
        keys = reverse.keys()
        for key in keys:
            categoryList = reverse[key]
            categoryCount = len(categoryList)
            meanList = []
            for i in xrange(categoryCount):
                category = categoryList[i]
                mean = categories[category]['mean']
                meanList.append(mean)
            sortedList = [x for (y,x) in sorted(zip(meanList, categoryList))]
            reverse[key] = sortedList
    
    def loadConfiguration(self, path):
        """loadConfiguration(str path)"""
        self._categories = {}
        self._parameters = {}
        self._rules = []
        data = open(path)
        lines = data.readlines()
        data.close()
        index = lines.index('[CATEGORIES]\n') + 1
        while(lines[index].count('[END]') == 0):
            name = lines[index].strip('\n')
            variable = lines[index+1].strip('\n').split('=')[1]
            mean = float(lines[index+2].strip('\n').split('=')[1])
            scale = float(lines[index+3].strip('\n').split('=')[1])
            self._categories[name] = {}
            self._categories[name]['variable'] = variable
            self._categories[name]['mean'] = mean
            self._categories[name]['scale'] = scale
            index += 4
        integers = ['deFuzzificationMode', 'antMovementMode', 'antCount', 'cycleCount', 'stepCount']
        floats = ['alpha', 'beta', 'delta', 'tuning', 'rho', 'psi']
        index = lines.index('[PARAMETERS]\n') + 1
        while(lines[index].count('[END]') == 0):
            lines[index] = lines[index].strip('\n')
            split = lines[index].split('=')
            if split[0] in integers:
                self._parameters[split[0]] = int(split[1])
            elif split[0] in floats:
                self._parameters[split[0]] = float(split[1])
            index += 1
        index = lines.index('[RULES]\n') + 1
        while(lines[index].count('[END]') == 0):
            lines[index] = lines[index].strip('\n')
            split = lines[index].split(',')
            self._rules.append(split)
            index += 1
        self._isLoaded = True
    
    def saveConfiguration(self, path):
        """saveConfiguration(str path)"""
        data = open(path, 'w')
        data.write('[CATEGORIES]\n')
        keys = self._categories.keys()
        for key in keys:
            data.write(key + '\n')
            data.write('variable=' + self._categories[key]['variable'] + '\n')
            data.write('mean=' + str(self._categories[key]['mean']) + '\n')
            data.write('scale=' + str(self._categories[key]['scale']) + '\n')
        data.write('[END]\n\n[PARAMETERS]\n')
        parameterList = ['deFuzzificationMode', 'antMovementMode', 'antCount', 'cycleCount', 'stepCount', 'alpha', 'beta', 'delta', 'tuning', 'rho', 'psi']
        parameterCount = len(parameterList)
        for i in xrange(parameterCount):
            data.write(parameterList[i] + '=' + str(self._parameters[parameterList[i]]) + '\n')
        data.write('[END]\n\n[RULES]\n')
        ruleCount = len(self._rules)
        for i in xrange(ruleCount):
            categoryCount = len(self._rules[i])
            for j in xrange(categoryCount):
                if j < categoryCount - 1:
                    data.write(self._rules[i][j] + ',')
                else:
                    data.write(self._rules[i][j] + '\n')
        data.write('[END]')
        data.close()
