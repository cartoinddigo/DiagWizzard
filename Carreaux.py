from PyQt4 import QtGui
from qgis.core import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from PyQt4.QtGui import QFileDialog
from pyspatialite import dbapi2 as db
import processing


import os
import csv
filter = "shp(*.shp)"
pathuser = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
csource = QFileDialog.getOpenFileName(None, "Selectionner le fichier source", pathuser, filter)
car2 = iface.addVectorLayer(csource, "carreaux", "ogr")
layer=qgis.utils.iface.activeLayer()
iter = layer.getFeatures()
table = []
for feature in iter:
    attrs = feature.attributes()
    table.append(attrs[1:2])
cliste = str(table)
cliste = cliste.replace(" ","").replace("[","").replace("]","")
cliste = cliste.replace("u","")
uri = QgsDataSourceURI()
uri.setDatabase('C:\CartoInddigo\DiagBuilder\db\diagBuilder2.sqlite')
uri.setDataSource("", "CR_DATA","", "idINSPIRE in ("+cliste+")")
d = iface.addVectorLayer(uri.uri(), "r", "spatialite")
shpField='idinspire'
csvField='idinspire'
joinObject = QgsVectorJoinInfo()
joinObject.joinLayerId = d.id()
joinObject.joinFieldName = csvField
joinObject.targetFieldName = shpField
joinObject.memoryCache = True
car2.addJoin(joinObject)
QgsVectorFileWriter.writeAsVectorFormat(car2, pathuser+'/vector/'+"carreaux_data.shp", "CP2154", None, "ESRI Shapefile")
centroids = processing.runalg('qgis:convertgeometrytype', car2, 0, pathuser+'/vector/'+"carreaux_data_pt.shp")
iface.addVectorLayer(pathuser+'/vector/'+"carreaux_data_pt.shp", "carreaux_data_pt", "ogr")




    

    
    

    