#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, json, time, math, mmap
from shapely.geometry import MultiPolygon, shape
import os
import csv
from PyQt4.QtCore import QVariant
from PyQt4.QtGui import QFileDialog

pathuser = QFileDialog.getExistingDirectory(None, "Select Directory")
fsource = QFileDialog.getOpenFileName(None, "Selectionner le fichier source")



def LineBus (coord, dmax):
    token = "fa1756fd-f394-42e2-89b4-3b1c8e116b2b"
    dcoord = coord
    ddmax = str(dmax)
    urla = "https://api.navitia.io/v1/coverage/"
    urlaa = "fr-idf/coords/"
    urldmax = "?distance="
    urlb = "/physical_modes/physical_mode:Bus/lines"
    urlq = urla+urlaa+dcoord+urlb+urldmax+ddmax
    resp = requests.get(urlq, headers={'Authorization':token})
    joutput = resp.json()
    #line = joutput['lines']
    print (urlq)
    nbline = joutput['pagination']['total_result']
    return (nbline)

with open(fsource) as csvfile:
    sources=csv.reader(csvfile, delimiter=';')
    table = []
    next(sources)
    
    for row in sources:
        idd = row[0]
        latO = row[2]
        lngO = row[1]
        origine = str(lngO+";"+latO)
        res = LineBus (origine, 1500)
        table.append(idd)
        table.append(res)

print (table)
with open(pathuser+'res.csv', 'w') as f :
    writer = csv.writer(f,delimiter=';', lineterminator='\n')
    writer.writerow(table)

    