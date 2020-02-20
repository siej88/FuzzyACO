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

import MainWindow as mw

import sys
from PyQt4 import QtGui as gui

def main():
    app = gui.QApplication(sys.argv)
    qIcon = gui.QIcon('resources\\icon.png')
    app.setWindowIcon(qIcon)
    mainWindow = mw.MainWindow()
    sys.exit(app.exec_())
 
if __name__ == '__main__':
    main()