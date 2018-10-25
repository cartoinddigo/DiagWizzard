#!/usr/bin/python
# encoding: utf-8

from PyQt4 import QtGui
from qgis.core import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.gui import QgsMessageBar
from PyQt4.QtGui import QFileDialog
from pyspatialite import dbapi2 as db
import processing
import os
import csv

pathuser = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
filter = "shp(*.shp)"

grd = QgsVectorLayer(pathuser+'/vector/grd_Marchabilite.shp', "grid", "ogr")
iris = QgsVectorLayer(pathuser+'/vector/DonneeRGP.shp', "donnees iris", "ogr")



res = processing.runalg("qgis:joinattributesbylocation",grd,iris,u'within', 0,0, '', 1, pathuser+'/vector/grd_Marchabilite_RGP.shp')
join = QgsVectorLayer(pathuser+'/vector/grd_Marchabilite_RGP.shp', "donnees iris", "ogr")
QgsMapLayerRegistry.instance().addMapLayers([grd, iris, join])