import os
import csv
import googlemaps
from datetime import datetime
from PyQt4.QtCore import QVariant
from PyQt4.QtGui import QFileDialog


gmaps = googlemaps.Client(key="AIzaSyDPlT4ARtREvLAVCUFgTX9dRQHG64Lu1Wg")
fsource = QFileDialog.getOpenFileName(None, "Selectionner le fichier source")
layer = QgsVectorLayer('LineString', 'route', "memory") 
pr = layer.dataProvider() 

with open(fsource) as csvfile:
    sources=csv.reader(csvfile, delimiter=';')
    table = []
    next(sources)
    for row in sources:
        
        idd = row[0]
        latO = row[1]
        lngO = row[2]
        latD = row[3]
        lngD = row[4]
        origine = str(latO+","+lngO)
        destination = str(latD+","+lngD)
        now = datetime.now()
        directions_result = gmaps.directions(origine, destination,mode="driving",departure_time=now)
        point_str = directions_result[0]["overview_polyline"]["points"]
        coord_chunks = [[]]
        for char in point_str:
            value = ord(char) - 63
            split_after = not (value & 0x20)
            value &= 0x1F
            coord_chunks[-1].append(value)
            if split_after:
                coord_chunks.append([])

        del coord_chunks[-1]
        coords = []
        for coord_chunk in coord_chunks:
            coord = 0
            for i, chunk in enumerate(coord_chunk):
                coord |= chunk << (i * 5)
            if coord & 0x1:
                coord = ~coord #invert
            coord >>= 1
            coord /= 100000.0
            coords.append(coord)

        points = []
        prev_x = 0
        prev_y = 0
        for i in xrange(0, len(coords) - 1, 2):
            if coords[i] == 0 and coords[i + 1] == 0:
                continue
            prev_x += coords[i + 1]
            prev_y += coords[i]
            points.append((round(prev_x, 6), round(prev_y, 6)))

        #print points

        pr.addAttributes([QgsField("attribution", QVariant.String)])
        layer.updateFields()
        fet = QgsFeature() 
        seg=[]
        for i in range(0,len(points)): 
            seg.append(QgsPoint(points[i][0],points[i][1])) 

        fet.setGeometry(QgsGeometry.fromPolyline(seg)) 
        fet.setAttributes([row[0]])
        pr.addFeatures([fet])
        layer.updateExtents() #update it 
        print(idd +" ok !")
              
QgsMapLayerRegistry.instance().addMapLayer(layer)
