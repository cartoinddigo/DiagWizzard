#!/usr/bin/python
# encoding: utf-8

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

pathuser = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
filter = "shp(*.shp)"

# Chargement et regroupent de POI de la BPE
print("Chargement de la table des equipements de la BPE (DonneesBPE_data.shp)")
bpesource = QgsVectorLayer(pathuser+'/vector/DonneesBPE_data.shp', "bpesource", "ogr")
if not bpesource.isValid():
  print "bpesource failed to load!"

QgsVectorFileWriter.writeAsVectorFormat(bpesource, pathuser+'/vector/'+"POI84.shp", "CP4326", None, "ESRI Shapefile")
POI84 = QgsVectorLayer(pathuser+'/vector/POI84.shp', "Poi84", "ogr")
QgsMapLayerRegistry.instance().addMapLayers([POI84,])


POI84.startEditing()
# Création des nouveaux champs
provider = POI84.dataProvider()
provider.addAttributes([QgsField("cat", QVariant.String, '', 50),QgsField("select", QVariant.String, '', 50),])
POI84.updateFields()


# Mise à jour de la cat Pharmacie
select = POI84.getFeatures( QgsFeatureRequest().setFilterExpression ( '"m_Cequip" = \'D301\'' ) )
POI84.setSelectedFeatures( [ f.id() for f in select ] )
selection = POI84.selectedFeatures()
for r in selection:
    r["cat"]='pharma'
    r["select"]='oui'
    POI84.updateFeature(r)

# Mise à jour de la cat Médecins
select = POI84.getFeatures( QgsFeatureRequest().setFilterExpression ( '"m_Cequip" = \'D201\' OR "m_Cequip" = \'D108\'' ) )
POI84.setSelectedFeatures( [ f.id() for f in select ] )
selection = POI84.selectedFeatures()
for r in selection:
    r["cat"]='medecins'
    r["select"]='oui'
    POI84.updateFeature(r)


# Mise à jour de la cat Alim
select = POI84.getFeatures( QgsFeatureRequest().setFilterExpression ( '"m_Cequip" = \'B201\' OR "m_Cequip" = \'B202\' OR "m_Cequip" = \'B204\' OR "m_Cequip" = \'B206\'' ) )
POI84.setSelectedFeatures( [ f.id() for f in select ] )
selection = POI84.selectedFeatures()
for r in selection:
    r["cat"]='alim'
    r["select"]='oui'
    POI84.updateFeature(r)


# Mise à jour de la cat Grandes Surface
select = POI84.getFeatures( QgsFeatureRequest().setFilterExpression ( ' "m_Cequip" = \'B101\' OR "m_Cequip" = \'B102\' ' ) )
POI84.setSelectedFeatures( [ f.id() for f in select ] )
selection = POI84.selectedFeatures()
for r in selection:
    r["cat"]='gdsurf'
    r["select"]='oui'
    POI84.updateFeature(r)


# Mise à jour de la cat Boulangerie
select = POI84.getFeatures( QgsFeatureRequest().setFilterExpression ( ' "m_Cequip" = \'B203\' ' ) )
POI84.setSelectedFeatures( [ f.id() for f in select ] )
selection = POI84.selectedFeatures()
for r in selection:
    r["cat"]='boulang'
    r["select"]='oui'
    POI84.updateFeature(r)


# Mise à jour de la cat Enseignement
select = POI84.getFeatures( QgsFeatureRequest().setFilterExpression ( ' "m_CEns" = \'C1\' OR "m_CEns" = \'C2\' OR "m_CEns" = \'C3\' OR "m_CEns" = \'C5\' ' ) )
POI84.setSelectedFeatures( [ f.id() for f in select ] )
selection = POI84.selectedFeatures()
for r in selection:
    r["cat"]='ecoles'
    r["select"]='oui'
    POI84.updateFeature(r)

# Mise à jour de la cat Restaurants
select = POI84.getFeatures( QgsFeatureRequest().setFilterExpression ( ' "m_Cequip" = \'A504\' ' ) )
POI84.setSelectedFeatures( [ f.id() for f in select ] )
selection = POI84.selectedFeatures()
for r in selection:
    r["cat"]='restau'
    r["select"]='oui'
    POI84.updateFeature(r)

# Mise à jour de la cat Tabacpress
# TODO !!

POI84.commitChanges()
select = POI84.getFeatures( QgsFeatureRequest().setFilterExpression ( ' "select" = \'oui\' ' ) )
POI84.setSelectedFeatures( [ f.id() for f in select ] )
selection = POI84.selectedFeatures()

print("Pret pour la recherche d'isochrones")
