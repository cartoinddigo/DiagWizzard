from PyQt4 import QtGui
from qgis.core import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from PyQt4.QtGui import QFileDialog
from pyspatialite import dbapi2 as db


import os
import csv

pathuser = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
car2 = iface.addVectorLayer(pathuser+'/vector/'+"carreaux.shp", "car2_93", "ogr")
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


    

    
    

    