import os
from qgis.core import QgsProject
from qgis.gui import QgsMapCanvas, QgsLayerTreeMapCanvasBridge
from qgis.core.contextmanagers import qgisapp
from PyQt4.QtGui import QFileDialog
from PyQt4.QtCore import QFileInfo

iface.newProject()
pathuser = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
filter = "qgs(*.qgs)"
path = pathuser
project = QFileDialog.getOpenFileName(None, "Selectionner le fichier source", path+'/projects', filter)
canvas = QgsMapCanvas(None)
# Load project
bridge = QgsLayerTreeMapCanvasBridge(QgsProject.instance().layerTreeRoot(), canvas)
QgsProject.instance().read(QFileInfo(projet))
base = QFileInfo(projet)
nom = base.baseName()
print (nom)
# Load the composer
composerView = qgis.utils.iface.activeComposers()[0]
composition = composerView.composition()
atlas = composition.atlasComposition()
composition.setAtlasMode(QgsComposition.ExportAtlas)
atlas.beginRender()
for i in range(0,atlas.numFeatures()):
    atlas.prepareForFeature(i)
    image = composition.printPageAsRaster(i)
    image.save(pathuser+'/export/'+nom+'-'+str(i)+'.png','png')
atlas.endRender()