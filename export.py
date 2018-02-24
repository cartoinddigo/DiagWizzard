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
listeqgs = os.listdir(pathuser+'/projects')
#canvas = QgsMapCanvas(None)
#bridge = QgsLayerTreeMapCanvasBridge(QgsProject.instance().layerTreeRoot(), canvas)
for j in listeqgs:
    project = pathuser+'/projects/'+str(j)
    
    
    QgsProject.instance().read(QFileInfo(project))
    base = QFileInfo(project)
    nom = base.baseName()
    composerView = qgis.utils.iface.activeComposers()[0]
    composition = composerView.composition()
    atlas = composition.atlasComposition()
    composition.setAtlasMode(QgsComposition.ExportAtlas)
    atlas.beginRender()
    for i in range(0,atlas.numFeatures()):
        atlas.prepareForFeature(i)
        image = composition.printPageAsRaster(0)
        image.save(pathuser+'/export/'+nom+'-Z'+str(i)+'.png','png')
        
    atlas.endRender()
    print (nom+" exporte")
    iface.newProject()
