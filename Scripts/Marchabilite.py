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



def iso (catf, distf):
    # fonction de filtrage des isochrone et maj des points
    print("Sélection des points")
    cat = catf[0:5]
    dist = distf
    ddist = dist /100
    coll = "g"+str(ddist)+"-"+str(cat)
    print(coll)

    isof = isource.setSubsetString(' "cat" = \'%s\'  and "dist" = %d ' % (catf, distf))
    cMarchabilite.startEditing()
    processing.runalg("qgis:selectbylocation",cMarchabilite,isource,['within'],0,0)

    print("Mise à jour des entités séléctionnées")
    for feature in cMarchabilite.selectedFeatures():
        feature[coll] = 1
        cMarchabilite.updateFeature(feature)
    cMarchabilite.commitChanges()
    print("Grille mise à jour")



pathuser = str(QFileDialog.getExistingDirectory(None, "Select Directory"))

filter = "shp(*.shp)"





# Chargement des isochrones
print("Chargement des isochrones")
isource = QgsVectorLayer(pathuser+'/vector/Isochrones_93.shp', "isource", "ogr")
if not isource.isValid():
  print "isource failed to load!"
  
QgsMapLayerRegistry.instance().addMapLayers([isource,])

# Chargement de la table des carreaux source
print("Chargement de la table des carreaux source (carreaux_data_pt)")
csource = QgsVectorLayer(pathuser+'/vector/carreaux_data_pt.shp', "csource", "ogr")
if not csource.isValid():
  print "csource failed to load!"

QgsMapLayerRegistry.instance().addMapLayers([csource,])

# Création du fichier Grille
print("Création du fichier Grille")
QgsVectorFileWriter.writeAsVectorFormat(csource, pathuser+'/vector/'+"grd_Marchabilite.shp", "CP2154", None, "ESRI Shapefile")
cMarchabilite = QgsVectorLayer(pathuser+"/vector/grd_Marchabilite.shp", "grille", "ogr")
QgsMapLayerRegistry.instance().addMapLayers([cMarchabilite,])

#Création des nouveaux champs
print("Ajout des nouveaux champs")

cMarchabilite.startEditing()
provider = cMarchabilite.dataProvider()
provider.addAttributes([
                                    QgsField("g3-pharm", QVariant.Int),
                                    QgsField("g3-medec", QVariant.Int),
                                    QgsField("g3-alim", QVariant.Int),
                                    QgsField("g3-gdsur", QVariant.Int),
                                    QgsField("g3-boula", QVariant.Int),
                                    QgsField("g3-ecole", QVariant.Int),
                                    QgsField("g3-tabac", QVariant.Int),
                                    QgsField("g3-resta", QVariant.Int),
                                    QgsField("g3-sum", QVariant.Int),
                                    QgsField("g3-tsant", QVariant.Int),
                                    QgsField("g3-talim", QVariant.Int),
                                    QgsField("g3-tsoci", QVariant.Int),
                                    QgsField("g3-tglob", QVariant.Int),
                                    QgsField("g5-pharm", QVariant.Int),
                                    QgsField("g5-medec", QVariant.Int),
                                    QgsField("g5-alim", QVariant.Int),
                                    QgsField("g5-gdsur", QVariant.Int),
                                    QgsField("g5-boula", QVariant.Int),
                                    QgsField("g5-ecole", QVariant.Int),
                                    QgsField("g5-tabac", QVariant.Int),
                                    QgsField("g5-resta", QVariant.Int),
                                    QgsField("g5-sum", QVariant.Int),
                                    QgsField("g5-tsant", QVariant.Int),
                                    QgsField("g5-talim", QVariant.Int),
                                    QgsField("g5-tsoci", QVariant.Int),
                                    QgsField("g5-tglob", QVariant.Int),
                                    QgsField("g10-pharm", QVariant.Int),
                                    QgsField("g10-medec", QVariant.Int),
                                    QgsField("g10-alim", QVariant.Int),
                                    QgsField("g10-gdsur", QVariant.Int),
                                    QgsField("g10-boula", QVariant.Int),
                                    QgsField("g10-ecole", QVariant.Int),
                                    QgsField("g10-tabac", QVariant.Int),
                                    QgsField("g10-resta", QVariant.Int),
                                    QgsField("g10-sum", QVariant.Int),
                                    QgsField("g10-tsant", QVariant.Int),
                                    QgsField("g10-talim", QVariant.Int),
                                    QgsField("g10-tsoci", QVariant.Int),
                                    QgsField("g10-tglob", QVariant.Int),
                                    QgsField("g-marchab", QVariant.Double),
                                    QgsField("g-potmar", QVariant.Double),

                                ])
cMarchabilite.updateFields()
print("Mise à jour des valeurs pas défaut")


for feature in cMarchabilite.getFeatures():
    feature["g3-pharm"] = 0
    feature["g3-medec"] = 0
    feature["g3-alim"] = 0
    feature["g3-gdsur"] = 0
    feature["g3-boula"] = 0
    feature["g3-ecole"] = 0
    feature["g3-tabac"] = 0
    feature["g3-resta"] = 0
    feature["g3-sum"] = 0
    feature["g3-tsant"] = 0
    feature["g3-talim"] = 0
    feature["g3-tsoci"] = 0
    feature["g3-tglob"] = 0
    feature["g5-pharm"] = 0
    feature["g5-medec"] = 0
    feature["g5-alim"] = 0
    feature["g5-gdsur"] = 0
    feature["g5-boula"] = 0
    feature["g5-ecole"] = 0
    feature["g5-tabac"] = 0
    feature["g5-resta"] = 0
    feature["g5-sum"] = 0
    feature["g5-tsant"] = 0
    feature["g5-talim"] = 0
    feature["g5-tsoci"] = 0
    feature["g5-tglob"] = 0
    feature["g10-pharm"] = 0
    feature["g10-medec"] = 0
    feature["g10-alim"] = 0
    feature["g10-gdsur"] = 0
    feature["g10-boula"] = 0
    feature["g10-ecole"] = 0
    feature["g10-tabac"] = 0
    feature["g10-resta"] = 0
    feature["g10-sum"] = 0
    feature["g10-tsant"] = 0
    feature["g10-talim"] = 0
    feature["g10-tsoci"] = 0
    feature["g10-tglob"] = 0
    feature["g-marchab"] = 0.0
    feature["g-potmar"] = 0.0
    cMarchabilite.updateFeature(feature)

    print(feature[0])

cMarchabilite.commitChanges()

QgsMapLayerRegistry.instance().addMapLayers([cMarchabilite,])


# Filtrage de la couche isochrones
print("Flitrage des isochrones")
iso("pharma", 300)
iso("medecins", 300)
iso("alim", 300)
iso("gdsurf", 300)
iso("boulang", 300)
iso("ecoles", 300)
iso("tabacpress", 300)
iso("restau", 300)
iso("pharma", 500)
iso("medecins", 500)
iso("alim", 500)
iso("gdsurf", 500)
iso("boulang", 500)
iso("ecoles", 500)
iso("tabacpress", 500)
iso("restau", 500)
iso("pharma", 1000)
iso("medecins", 1000)
iso("alim", 1000)
iso("gdsurf", 1000)
iso("boulang", 1000)
iso("ecoles", 1000)
iso("tabacpress", 1000)
iso("restau", 1000)

# Calcul des somme par distance
print ("Calcul des sommes pour distance :")
cMarchabilite.startEditing()
for row in cMarchabilite.getFeatures():
    print("--> 300 m")
    row["g3-sum"] = row["g3-pharm"] + row["g3-medec"] + row["g3-alim"] + row["g3-gdsur"] + row["g3-boula"] + row["g3-ecole"] + row["g3-tabac"] + row["g3-resta"]
    print("--> 500 m")
    row["g5-sum"] = row["g5-pharm"] + row["g5-medec"] + row["g5-alim"] + row["g5-gdsur"] + row["g5-boula"] + row["g5-ecole"] + row["g5-tabac"] + row["g5-resta"]
    print("--> 1 000 m")
    row["g10-sum"] = row["g10-pharm"] + row["g10-medec"] + row["g10-alim"] + row["g10-gdsur"] + row["g10-boula"] + row["g10-ecole"] + row["g10-tabac"] + row["g10-resta"]
    cMarchabilite.updateFeature(row)
print("Calcul des sommes terminé.")
cMarchabilite.commitChanges()

# Calcul de l'indice de marchabilité
print ("Calcul de l'indice de marchabilité.")
cMarchabilite.startEditing()
for i in cMarchabilite.getFeatures():
    i["g-marchab"] = i["g3-sum"] + (i["g5-sum"]*0.8) + (i["g10-sum"]*0.6)
    cMarchabilite.updateFeature(i)
    print("Marchabilité : " + str(i["g-marchab"]))
print("Calcul des sommes terminé.")
cMarchabilite.commitChanges()

# Calculs des regroupements thématiques
print ("Début de calcul des indicateurs thématiques")
cMarchabilite.startEditing()

# Thématique santé
print ("Thématique Santé")
cMarchabilite.removeSelection()
select = cMarchabilite.getFeatures( QgsFeatureRequest().setFilterExpression ( ' "g3-pharm" = 1 AND "g3-medec" = 1 ' ) )
cMarchabilite.setSelectedFeatures( [ f.id() for f in select ] )
selection = cMarchabilite.selectedFeatures()
for r in selection:
    r["g3-tsant"]=1
    cMarchabilite.updateFeature(r)

cMarchabilite.removeSelection()
select = cMarchabilite.getFeatures( QgsFeatureRequest().setFilterExpression ( ' "g5-pharm" = 1 AND "g5-medec" = 1 ' ) )
cMarchabilite.setSelectedFeatures( [ f.id() for f in select ] )
selection = cMarchabilite.selectedFeatures()
for r in selection:
    r["g5-tsant"]=1
    cMarchabilite.updateFeature(r)

cMarchabilite.removeSelection()
select = cMarchabilite.getFeatures( QgsFeatureRequest().setFilterExpression ( ' "g10-pharm" = 1 AND "g10-medec" = 1 ' ) )
cMarchabilite.setSelectedFeatures( [ f.id() for f in select ] )
selection = cMarchabilite.selectedFeatures()
for r in selection:
    r["g10-tsant"]=1
    cMarchabilite.updateFeature(r)
    
# Thématique Alimentation
print ("Thématique Alimentation")
cMarchabilite.removeSelection()
select = cMarchabilite.getFeatures( QgsFeatureRequest().setFilterExpression ( ' "g3-boula" = 1 AND "g3-alim" = 1 AND "g3-gdsur" = 1 ' ) )
cMarchabilite.setSelectedFeatures( [ f.id() for f in select ] )
selection = cMarchabilite.selectedFeatures()
for r in selection:
    r["g3-talim"]=1
    cMarchabilite.updateFeature(r)

cMarchabilite.removeSelection()
select = cMarchabilite.getFeatures( QgsFeatureRequest().setFilterExpression ( ' "g5-boula" = 1 AND "g5-alim" = 1 AND "g5-gdsur" = 1 ' ) )
cMarchabilite.setSelectedFeatures( [ f.id() for f in select ] )
selection = cMarchabilite.selectedFeatures()
for r in selection:
    r["g5-talim"]=1
    cMarchabilite.updateFeature(r)

cMarchabilite.removeSelection()
select = cMarchabilite.getFeatures( QgsFeatureRequest().setFilterExpression ( ' "g10-boula" = 1 AND "g10-alim" = 1 AND "g10-gdsur" = 1 ' ) )
cMarchabilite.setSelectedFeatures( [ f.id() for f in select ] )
selection = cMarchabilite.selectedFeatures()
for r in selection:
    r["g10-talim"]=1
    cMarchabilite.updateFeature(r)
    
    # Thématique Sociale
print ("Thématique Sociale")
cMarchabilite.removeSelection()
select = cMarchabilite.getFeatures( QgsFeatureRequest().setFilterExpression ( ' "g3-resta" = 1 ' ) )
cMarchabilite.setSelectedFeatures( [ f.id() for f in select ] )
selection = cMarchabilite.selectedFeatures()
for r in selection:
    r["g3-tsoci"]=1
    cMarchabilite.updateFeature(r)

cMarchabilite.removeSelection()
select = cMarchabilite.getFeatures( QgsFeatureRequest().setFilterExpression ( ' "g5-resta" = 1 ' ) )
cMarchabilite.setSelectedFeatures( [ f.id() for f in select ] )
selection = cMarchabilite.selectedFeatures()
for r in selection:
    r["g5-tsoci"]=1
    cMarchabilite.updateFeature(r)

cMarchabilite.removeSelection()
select = cMarchabilite.getFeatures( QgsFeatureRequest().setFilterExpression ( ' "g10-resta" = 1 ' ) )
cMarchabilite.setSelectedFeatures( [ f.id() for f in select ] )
selection = cMarchabilite.selectedFeatures()
for r in selection:
    r["g10-tsoci"]=1
    cMarchabilite.updateFeature(r)

    # Thématique Globale
print ("Thématique Globale")
cMarchabilite.removeSelection()
select = cMarchabilite.getFeatures( QgsFeatureRequest().setFilterExpression ( ' "g3-tsant" = 1 AND "g3-talim" = 1 AND "g3-tsoci" = 1 AND "g3-ecole" = 1 ' ) )
cMarchabilite.setSelectedFeatures( [ f.id() for f in select ] )
selection = cMarchabilite.selectedFeatures()
for r in selection:
    r["g3-tglob"]=1
    cMarchabilite.updateFeature(r)

cMarchabilite.removeSelection()
select = cMarchabilite.getFeatures( QgsFeatureRequest().setFilterExpression ( ' "g5-tsant" = 1 AND "g5-talim" = 1 AND "g5-tsoci" = 1 AND "g5-ecole" = 1' ) )
cMarchabilite.setSelectedFeatures( [ f.id() for f in select ] )
selection = cMarchabilite.selectedFeatures()
for r in selection:
    r["g5-tglob"]=1
    cMarchabilite.updateFeature(r)

cMarchabilite.removeSelection()
select = cMarchabilite.getFeatures( QgsFeatureRequest().setFilterExpression ( ' "g10-tsant" = 1 AND "g10-talim" = 1 AND "g10-tsoci" = 1 AND "g10-ecole" = 1' ) )
cMarchabilite.setSelectedFeatures( [ f.id() for f in select ] )
selection = cMarchabilite.selectedFeatures()
for r in selection:
    r["g10-tglob"]=1
    cMarchabilite.updateFeature(r)

cMarchabilite.removeSelection()
cMarchabilite.commitChanges()

# Calcul du potentiel de de marchabilité
print ("Calcul du potentiel de de marchabilité.")
cMarchabilite.startEditing()
for i in cMarchabilite.getFeatures():
    i["g-potmar"] = i["g3-tglob"] + (i["g5-tglob"]*0.8) + (i["g10-tglob"]*0.6)
    cMarchabilite.updateFeature(i)
    print("Potentiel  Marchabilité : " + str(i["g-potmar"]))
print("Calcul des potentiels terminé.")
cMarchabilite.commitChanges()


