from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from PyQt4.QtGui import QFileDialog
import processing
from pyspatialite import dbapi2 as db

import os
import csv

pathuser = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
filter = "csv(*.csv)"
path = pathuser
fsource = QFileDialog.getOpenFileName(None, "Selectionner le fichier source", path, filter)

with open(fsource) as csvfile:
        sources=csv.reader(csvfile, delimiter=';')
        table = []
        next(sources)
        for row in sources:
            table.append(row)
        liste = [i[0] for i in table]
        sliste = str(liste)
        sliste = sliste.replace(" ","").replace("[","").replace("]","")
        bliste = sliste.replace("_","")
        print(bliste)
    
uri = QgsDataSourceURI()
uri.setDatabase('C:\CartoInddigo\DiagBuilder\db\diagBuilder2.sqlite')
uri.setDataSource("", "FD","","CODGEO in ("+bliste+") AND DCLT NOT IN ("+bliste+")")
FluxSorants = iface.addVectorLayer(uri.uri(), "FluxSortants", "spatialite")
uri.setDataSource("", "FD","","DCLT in ("+bliste+") AND CODGEO NOT IN ("+bliste+")")
FluxEntrants = iface.addVectorLayer(uri.uri(), "FluxEntrants", "spatialite")
uri.setDataSource("", "FD","","DCLT in ("+bliste+") AND CODGEO IN ("+bliste+")")
FluxInternes = iface.addVectorLayer(uri.uri(), "FluxInternes", "spatialite")

print(FluxInternes)
uri.setDataSource("", "communes-pt2","geom")
compt = iface.addVectorLayer(uri.uri(), "compt", "spatialite")
