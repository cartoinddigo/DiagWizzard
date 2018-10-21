#!/usr/bin/python
# encoding: utf-8

#################################
#Charge la liste de communes cible
#et construit le dataset
#################################

# importe les lib python

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from PyQt4.QtGui import QFileDialog
import processing
from pyspatialite import dbapi2 as db

import os
import csv
from shutil import copyfile

pathuser = ""
fsource = ""
sliste = ""

def EspaceTravail(self):
    """Création de l'espace de travail"""
    pathuser = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
    print(pathuser)

    print("Test et creation de l'environnement de travail...")

    if not os.path.exists(pathuser+'/data'):
        os.mkdir(pathuser+'/data')
    if not os.path.exists(pathuser+'/vector'):
        os.mkdir(pathuser+'/vector')
    if not os.path.exists(pathuser+'/export'):
        os.mkdir(pathuser+'/export')
    if not os.path.exists(pathuser+'/projects'):
        os.mkdir(pathuser+'/projects')
    if not os.path.exists(pathuser+'/tableaux'):
        os.mkdir(pathuser+'/tableaux')
    if not os.path.exists(pathuser+'/recu'):
        os.mkdir(pathuser+'/recu')
    listeqgs = os.listdir('C:/CartoInddigo/DiagWizzard/qgs/')
    print(listeqgs)
    for j in listeqgs:
        if not os.path.isfile (pathuser+'/projects/' + j):
            copyfile('C:/CartoInddigo/DiagWizzard/qgs/' + j, pathuser+'/projects/' + j)
    print("...effectue.")
    return pathuser
    
    


def ChargeSource(pathuser):
    """Charge la liste des communes cibles"""
    print("Charge la liste des communes cibles")
    filter = "csv(*.csv)"
    path = pathuser
    fsource = QFileDialog.getOpenFileName(None, "Selectionner le fichier source", path, filter)
    return (fsource)

def ListeSource(fsource):
    """Regroupe les codes insee des communes source dans une liste python"""
    print("Regroupe les codes insee dans la liste Sources")
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
        #print(sliste)
    return (sliste)

def ListeBPE(fsource):
    """Regroupe les codes insee des communes source dans une liste python"""
    print("Regroupe les codes insee dans la liste BPE")
    with open(fsource) as csvfile:
        sources=csv.reader(csvfile, delimiter=';')
        table = []
        next(sources)
        for row in sources:
            table.append(row)
        liste = [i[0] for i in table]
        bliste = str(liste)
        bliste = bliste.replace(" ","").replace("[","").replace("]","").replace("_","")
#        print(bliste)
    return (bliste)
    

def ExtractComPt(sliste):
    """Extrait les centres communaux depuis la base Spatialite"""
    print("Exctraction des centres communaux...")
    uri = QgsDataSourceURI()
    uri.setDatabase('C:\CartoInddigo\DiagBuilder\db\diagBuilder2.sqlite')
    uri.setDataSource("", "communes-pt2","geom", "_INSEE in ("+sliste+")") #filtrer sur un champs, ajouter ,"CHAMP=VALEUR"
    sp_com_pt = iface.addVectorLayer(uri.uri(), "com_pt", "spatialite")
    print("...effectue.")
    if not sp_com_pt:
        print "spatialite communes-pt2 failed to load!"
    compt = QgsVectorFileWriter.writeAsVectorFormat(sp_com_pt, pathuser+'/vector/'+"com_pt.shp", "CP2154", None, "ESRI Shapefile")
    QgsMapLayerRegistry.instance().removeMapLayers( [sp_com_pt.id()] )
    com_pt = iface.addVectorLayer(pathuser+'/vector/'+"com_pt.shp", "com_pt", "ogr")
    if not com_pt:
        print "Selection de centres communaux impossible à charger !"
        
def ExtractComPoly(sliste):
    """Extrait les finages communaux depuis la base Spatialite"""
    print("Exctraction des finages communaux...")
    uri = QgsDataSourceURI()
    uri.setDatabase('C:\CartoInddigo\DiagBuilder\db\diagBuilder2.sqlite')
    uri.setDataSource("", "communes-poly2","geom", "_INSEE in ("+sliste+")") #filtrer sur un champs, ajouter ,"CHAMP=VALEUR"
    sp_com_poly = iface.addVectorLayer(uri.uri(), "com_poly", "spatialite")
    print("...effectue.")
    if not sp_com_poly:
        print "spatialite communes-poly2 failed to load!"
    compoly = QgsVectorFileWriter.writeAsVectorFormat(sp_com_poly, pathuser+'/vector/'+"com_poly.shp", "CP2154", None, "ESRI Shapefile")
    QgsMapLayerRegistry.instance().removeMapLayers( [sp_com_poly.id()] )
    com_poly = iface.addVectorLayer(pathuser+'/vector/'+"com_poly.shp", "com_poly", "ogr")
    if not com_poly:
        print "Selection de limites communales impossible à charger !"
    #Algoritme Dissolve pour créer la ZOI
    print("Dissolve : Creation de la ZOI...")
    dissolve93=processing.runalg('qgis:dissolve', pathuser+'/vector/'+"com_poly.shp",True,None,pathuser+'/vector/'+"zone93")
    zone93 = iface.addVectorLayer(pathuser+'/vector/'+"zone93.shp", "zone 93", "ogr")
    #Algoritme Reprojecte pour créer la ZOI en WGS 84
    print("...effectue.")
    print("Reproject : Reprojection de la ZOI vers WGS84...")
    reproject84 = processing.runalg('qgis:reprojectlayer', pathuser+'/vector/'+"zone93.shp",'EPSG:4326',pathuser+'/vector/'+"zone84")
    zone84 = iface.addVectorLayer(pathuser+'/vector/'+"zone84.shp", "zone 84", "ogr")
    print("...effectue.")

def ExtractComIris(sliste):
    """Extrait le decoupage iris depuis la base Spatialite"""
    print("Exctraction des IRIS...")
    uri = QgsDataSourceURI()
    uri.setDatabase('C:\CartoInddigo\DiagBuilder\db\diagBuilder2.sqlite')
    uri.setDataSource("", "iris3","geom", "_decpcom in ("+sliste+")") #filtrer sur un champs, ajouter ,"CHAMP=VALEUR"
    sp_iris3 = iface.addVectorLayer(uri.uri(), "com_iris", "spatialite")
    if not sp_iris3:
        print "spatialite iris3 failed to load!"
    comiris = QgsVectorFileWriter.writeAsVectorFormat(sp_iris3, pathuser+'/vector/'+"com_iris.shp", "CP2154", None, "ESRI Shapefile")
    QgsMapLayerRegistry.instance().removeMapLayers( [sp_iris3.id()] )
    com_iris = iface.addVectorLayer(pathuser+'/vector/'+"com_iris.shp", "com_iris", "ogr")
    com_iris.startEditing()
    provider = com_iris.dataProvider()
    provider.addAttributes([QgsField("_dcomiris", QVariant.String),])
    com_iris.updateFields()
    for feature in com_iris.getFeatures():
        feature["_dcomiris"] = str("_" + feature["dcomiris"])
        com_iris.updateFeature(feature)
        print(feature["_dcomiris"] )
    com_iris.commitChanges()
    print("...effectue.")
    if not com_iris:
        print "Selection d'iris impossible à charger !"
    return(com_iris)

def ListeIris(iris):
    print("Regroupe les codes insee dans la liste IRIS")
    liris = QgsMapLayerRegistry.instance().mapLayersByName("com_iris")[0]
    liste = []
    for feature in liris.getFeatures():
        attrs = feature.attributes()
        idx = liris.fieldNameIndex("_dcomiris")
        val = (feature.attributes()[idx])
        liste.append(val)
    sliste = str(liste)
    iliste = sliste.replace("'","").replace("[","").replace("]","").replace("u","").replace(" ","")
    print(iliste)
    return (iliste)

def RGP(iliste):
    """Extrait les données RGP"""
    print("Exctraction des donnees du RGP...")
    uri = QgsDataSourceURI()
    uri.setDatabase('C:\CartoInddigo\DiagBuilder\db\diagBuilder2.sqlite')
    uri.setDataSource("", "RGP","","_IRIS in ("+iliste+")") #TODO !!attention au codes iris sans les 0 dans la table RGP !!
    sRGP = iface.addVectorLayer(uri.uri(), "sRGP", "spatialite")
    print("...effectue.")
    print("Export CSV des donnees du RGP...")
    fRGP = QgsVectorFileWriter.writeAsVectorFormat(sRGP, pathuser+'/tableaux/'+"DonneeRGP.csv", "CP1250", None, "CSV")
    res = processing.runalg('qgis:joinattributestable', pathuser+'/vector/'+"com_iris.shp",pathuser+'/tableaux/'+"DonneeRGP.csv",'_dcomiris','_IRIS',pathuser+'/vector/'+"DonneeRGP.shp")
    layer = QgsVectorLayer(res['OUTPUT_LAYER'], "Donnees RGP", "ogr")
    QgsMapLayerRegistry.instance().addMapLayer(layer)
    #QgsMapLayerRegistry.instance().removeMapLayers( [sRGP.id()] )
    print("...effectue.")
    print("Extraction des centres des iris...")
    centroids = processing.runalg('qgis:convertgeometrytype', layer, 0, pathuser+'/vector/'+"iris_data_pt.shp")
    layer = iface.addVectorLayer(pathuser+'/vector/'+"iris_data_pt.shp", "iris_data_pt", "ogr")
    print("...effectue.")

    
def BPE(bliste):
    """Extrait les données RGP"""
    print("Exctraction des donnees de la BPE...")
    uri = QgsDataSourceURI()
    uri.setDatabase('C:\CartoInddigo\DiagBuilder\db\diagBuilder2.sqlite')
    uri.setDataSource("", "bpe","","depcom in ("+bliste+")")
    sBPE = iface.addVectorLayer(uri.uri(), "BPE", "spatialite")
    fBPE = QgsVectorFileWriter.writeAsVectorFormat(sBPE, pathuser+'/tableaux/'+"DonneeBPE.csv", "utf-8", None, "CSV")
    BPEGeom = "file:///"+pathuser+'/tableaux/'+"DonneeBPE.csv?delimiter=%s&crs=epsg:2154&wktField=%s" % (",", "geom")
    vlayer = iface.addVectorLayer(BPEGeom, "DonneesBPE", "delimitedtext")
    uri.setDataSource("", "VariablesBPE","")
    m = iface.addVectorLayer(uri.uri(), "m", "spatialite")
    print("...effectue.")
    print("BPE - Decodage des modalites...")
    shpField='typequ'
    csvField='cEquip'
    joinObject = QgsVectorJoinInfo()
    joinObject.joinLayerId = m.id()
    joinObject.joinFieldName = csvField
    joinObject.targetFieldName = shpField
    joinObject.memoryCache = True
    vlayer.addJoin(joinObject)
    print("...effectue.")
    print("Export CSV des donnees de la BPE...")
    writer = QgsVectorFileWriter.writeAsVectorFormat(vlayer, pathuser+'/vector/'+"DonneesBPE_data.shp", "utf-8", None, "ESRI Shapefile")
    DonneesBPE_data = iface.addVectorLayer(pathuser+'/vector/'+"DonneesBPE_data.shp", "DonneesBPE_data", "ogr")
    print("...effectue.")
    print("Export des donnees acheve")
    print("Veuillez maintenant creer le fichier centres.shp et exportet le réseau routier OSM... (OSM_streets.shp)")
    
    


#uri = QgsDataSourceURI()
#uri.setDatabase('C:\CartoInddigo\DiagBuilder\db\diagBuilder2.sqlite')
#uri.setDataSource("", "RGP","", "_IRIS in ("+sliste+")")


    

#Execution du script
if pathuser == "":
    pathuser = EspaceTravail(None)
if fsource == "":
    fsource = ChargeSource(pathuser)
if sliste == "":
    sliste = ListeSource(fsource)
    bliste = ListeBPE(fsource)
    ExtractComPt(sliste)
    ExtractComPoly(sliste)
    ExtractComIris(sliste)
    iliste = ListeIris("com_iris")
    RGP(iliste)
    BPE(bliste)
