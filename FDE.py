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
uri.setDataSource("", "FE","","CODGEO in ("+bliste+") AND DCETU NOT IN ("+bliste+")")
FluxSorants = iface.addVectorLayer(uri.uri(), "EtudeSortants", "spatialite")
uri.setDataSource("", "FE","","DCETU in ("+bliste+") AND CODGEO NOT IN ("+bliste+")")
FluxEntrants = iface.addVectorLayer(uri.uri(), "EtudeEntrants", "spatialite")
uri.setDataSource("", "FE","","DCETU in ("+bliste+") AND CODGEO IN ("+bliste+")")
FluxInternes = iface.addVectorLayer(uri.uri(), "EtudeInternes", "spatialite")

print(FluxInternes)
uri.setDataSource("", "communes-pt2","geom")
compt = iface.addVectorLayer(uri.uri(), "compt", "spatialite")