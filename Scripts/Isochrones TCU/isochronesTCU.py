#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, json, time, math, mmap
from shapely.geometry import MultiPolygon, shape
import csv
from PyQt4.QtGui import QFileDialog
from PyQt4.QtCore import QVariant

fsources = QFileDialog.getOpenFileName(None, "Selectionner le fichier source")
token = "fa1756fd-f394-42e2-89b4-3b1c8e116b2b"


#def isonav (coord, dmax):
#    dcoord = coord
#    ddmax = str(dmax *60)
#    token = "fa1756fd-f394-42e2-89b4-3b1c8e116b2b"
#    urla = "https://api.navitia.io/v1/coverage/"
#    urlaa = "fr-sw/isochrones?from="
#    urldmax = "&max_duration="
#    urlb = "&min_duration=0&datetime_represents=arrival&datetime=20190125T090000&"
#    urlq = urla+urlaa+dcoord+urldmax+ddmax+urlb
##    print(urlq)
#    resp = requests.get(urlq, headers={'Authorization':token})
#    iso_output = resp.json()
#    iso = iso_output['isochrones']

#    for r in range(len(iso)):
#        iso_duration = iso[r]['max_duration']
#        geojson = iso[r]['geojson']
#        geom = shape(geojson)
#        geom = QgsGeometry.fromWkt(geom.wkt)
#        pr = layer.dataProvider()
#        elem= QgsFeature()
#        elem.setGeometry(geom)
#        pr.addFeatures( [ elem ] )
#        layer.updateExtents()
#        QgsMapLayerRegistry.instance().addMapLayers([layer])
        
        
with open(fsources) as csvfile:
    dmax = 10 # Distance en metres
    layer = QgsVectorLayer('Polygon',str(dmax)+" min",'memory')
    pr = layer.dataProvider()

    sources=csv.reader(csvfile, delimiter=';')
    next(sources)
    
    for row in sources:
        idd = row[0]
        coord = row[1]
        dcoord = coord
        ddmax = str(dmax *60)
        urla = "https://api.navitia.io/v1/coverage/"
        urlaa = "fr-sw/isochrones?from="
        urldmax = "&max_duration="
        urlb = "&min_duration=0&datetime_represents=arrival&datetime=20190125T090000&"
        urlq = urla+urlaa+dcoord+urldmax+ddmax+urlb
        resp = requests.get(urlq, headers={'Authorization':token})
        iso_output = resp.json()
        iso = iso_output['isochrones']
        for r in range(len(iso)):
            pr.addAttributes([QgsField("idd", QVariant.String),
                                    QgsField("dist_m", QVariant.Int),
                                    ])
            layer.updateFields()
            iso_duration = iso[r]['max_duration']
            geojson = iso[r]['geojson']
            geom = shape(geojson)
            geomWKT = QgsGeometry.fromWkt(geom.wkt)
            elem= QgsFeature()
            elem.setGeometry(geomWKT)
            elem.setAttributes([row[0],
                            dmax,
                            ])
            pr.addFeatures( [ elem ] )
        
QgsMapLayerRegistry.instance().addMapLayers([layer])
        

#coord = "-0.58165800000000112;44.84019599999993488" #coordonnée du site 
#isonav(coord, 180)
#isonav(coord, 120)
#isonav(coord, 90)
#isonav(coord, 60)
#isonav(coord, 45)
#isonav(coord, 30)
#isonav(coord, 15)
#isonav(coord, 10)
#





