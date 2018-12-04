import googlemaps
from datetime import datetime
import csv
from PyQt4.QtGui import QFileDialog
from PyQt4.QtCore import QVariant

gmaps = googlemaps.Client(key="AIzaSyDPlT4ARtREvLAVCUFgTX9dRQHG64Lu1Wg")
tsources = "C:/CartoInddigo/DiagWizzard/Scripts/Directions/SourcesDirections.csv"
fsources = QFileDialog.getOpenFileName(None, "Selectionner le fichier source")

layer = QgsVectorLayer('LineString', 'Sements', "memory")
start_pt = QgsVectorLayer('Point', 'start_pt', "memory")
pr = layer.dataProvider() 
sdata = start_pt.dataProvider() 
def gootogis(enc_polyline):


    coord_chunks = [[]]
    for char in enc_polyline:
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
    pr.addAttributes([QgsField("id", QVariant.String),
                            QgsField("dist_m", QVariant.Int),
                            QgsField("tp_s", QVariant.Int),
                            ])
    layer.updateFields()
    fet = QgsFeature() 
    seg=[]
    for i in range(0,len(points)): 
        seg.append(QgsPoint(points[i][0],points[i][1])) 
    fet.setGeometry(QgsGeometry.fromPolyline(seg)) 
    fet.setAttributes([row[0],
                            dist,
                            temps,
                            ])
    pr.addFeatures([fet])

    # layer.updateExtents() #update it 
    print(idd +" ok !")




with open(fsources) as csvfile:
    sources=csv.reader(csvfile, delimiter=';')
    next(sources)
    
    #R
    routes = []
    legs = []
    steps = []
    for row in sources:
        idd = row[0]
        latO = row[1]
        lngO = row[2]
        latD = row[3]
        lngD = row[4]
        origine = str(latO+","+lngO)
        destination = str(latD+","+lngD)
        now = datetime.now()
        route = gmaps.directions(origine, destination,mode="driving",departure_time=now)
        legs = route[0]["legs"]
        for l in legs:
            steps = l["steps"]
#            print steps
            for s in steps:
                lines = s["polyline"]["points"]
                dist = s["distance"]["value"]
                temps = s["duration"]["value"]
                gootogis(lines)
                
QgsMapLayerRegistry.instance().addMapLayer(layer)




