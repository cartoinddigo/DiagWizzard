# -*- coding: utf-8 -*-
import sys
from os.path import exists
import simplejson as json 

import csv, requests, json, math, time, mmap, sys, os, datetime
import requests.certs
build_exe_options = {"include_files":[(requests.certs.where(),'cacert.pem')]}
import datetime
from pprint import pprint

token = "13ae45dd-3938-47a1-a6d5-4b8a2bd58836"
url = 'https://api.navitia.io/v1/coverage/fr-se/journeys?from=6.113463;45.458368&to=5.884282844;45.26704766&max_duration_to_pt=1500&datetime_represents=arrival&datetime=20180319T0900&first_section_mode[]=walking&first_section_mode[]=bike&first_section_mode[]=bss'
reponse = requests.get(url, headers={'Authorization':token})
nav_output = reponse.json()


route = {}
listeseg=[]
segment= {}
print (url)
for journey in nav_output['journeys']:
    route['dureetot']=journey['duration']/60
    route['type']=journey['type']
    route['depart']=journey['departure_date_time']
    route['arrivee']=journey['arrival_date_time']
    route['nbcorres']=journey['nb_transfers']
    
    for s in journey['sections']:
        segment['idsection']=s['id']
        segment['typesection']=s['type']

        
        if s['type']=='street_network':
            segment['modesection']=s['mode']
            segment['dureesection']=s['duration']/60


        elif s['type']=='public_transport':
            segment['modesection']=s['display_informations']['network'], s['display_informations']['physical_mode']
            segment['dureesection']=s['duration']/60

            
        elif s['type']=='transfer':
            segment['modesection']=s['transfer_type']
            segment['dureesection']=s['duration']/60

            
        else :
            segment['modesection']='Autre temps'
            segment['dureesection']=s['duration']/60


        listeseg.append(segment)
        
        pprint(listeseg)
        
#pprint(listeseg)
route['segment']=listeseg
#pprint(route)

         
    

#pprint (glob)
              
              


                  


