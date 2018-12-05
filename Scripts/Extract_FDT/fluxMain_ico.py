#!/usr/bin/python
#coding : utf-8

from config import config

import os,sys
import csv
import psycopg2
import psycopg2.extensions
import psycopg2.extras

import numpy as np

# read connection parameters
params = config()
 
print('Connection à la base de données PostgreSQL...')
conn = psycopg2.connect(**params)
     
# create a cursor
cur = conn.cursor()

#effacer données si existantes
cur.execute("DELETE FROM flux_insee.territoire")
cur.execute("""
DROP TABLE IF EXISTS flux_insee.temp_flux;
DROP TABLE IF EXISTS flux_insee.temp_flux_v2;
DROP TABLE IF EXISTS flux_insee.temp_flux_v3;
""")

print("Données effacées")
conn.commit()

#importe les données
fichier = csv.reader(open('territoire.csv'),delimiter=',')
next(fichier)
for row in fichier:
        cur.execute("INSERT INTO flux_insee.territoire (insee,nom)"\
            "VALUES (%s,%s)",
           row)

print("Données importées")

conn.commit()

print("Traitement de la requête SQL")
#requête sql de Postgres
cur.execute("""
CREATE TABLE flux_insee.temp_flux AS
    SELECT fd_mobpro_2015.commune||fd_mobpro_2015.dclt as id_concatener, fd_mobpro_2015.commune as commune_origine, fd_mobpro_2015.dcflt as c_etrangere, comm_etrangere.libelle as nom_com_etrangere, fd_mobpro_2015.dclt as commune_destination, agerevq.libelle as age, trans.libelle as mode_de_transport, cs1.libelle as csp, SUM(fd_mobpro_2015.ipondi) as flux
	FROM flux_insee.territoire, flux_insee.fd_mobpro_2015
		JOIN flux_insee.comm_etrangere ON comm_etrangere.code_com_etranger = fd_mobpro_2015.dcflt
		JOIN flux_insee.trans ON trans.code_trans = fd_mobpro_2015.trans
 		JOIN flux_insee.cs1 ON cs1.code_cs1 = fd_mobpro_2015.cs1
		JOIN flux_insee.agerevq ON agerevq.code_agerevq = fd_mobpro_2015.agerevq
	WHERE territoire.insee = fd_mobpro_2015.commune OR territoire.insee = fd_mobpro_2015.dclt
GROUP BY fd_mobpro_2015.commune,fd_mobpro_2015.dclt,comm_etrangere.libelle,fd_mobpro_2015.dcflt,agerevq.libelle,trans.libelle,cs1.libelle;


ALTER TABLE flux_insee.temp_flux
	ADD type_flux character varying(20),
	ADD nom_commune_origine character varying(150),
	ADD nom_commune_destination character varying(150),
	ADD temp_origine_flux character varying(3),
	ADD temp_destination_flux character varying(3);


UPDATE flux_insee.temp_flux
	SET nom_commune_origine = communes_2018.libelle
	FROM flux_insee.communes_2018
		WHERE commune_origine = communes_2018.code_commune;

UPDATE flux_insee.temp_flux
	SET nom_commune_destination = communes_2018.libelle
	FROM flux_insee.communes_2018
		WHERE commune_destination = communes_2018.code_commune;

UPDATE flux_insee.temp_flux
	SET commune_origine = c_etrangere	
		WHERE commune_origine = '99999';

UPDATE flux_insee.temp_flux		
	SET commune_destination = c_etrangere
		WHERE commune_destination = '99999';

UPDATE flux_insee.temp_flux
	SET nom_commune_origine = nom_com_etrangere
		WHERE commune_origine = c_etrangere;

UPDATE flux_insee.temp_flux
	SET nom_commune_destination = nom_com_etrangere
		WHERE commune_destination = c_etrangere;

UPDATE flux_insee.temp_flux	
	SET nom_commune_destination = 'Lyon'
		WHERE commune_destination IN ('69381', '69382', '69383','69384', '69385', '69386', '69387', '69388', '69389');

UPDATE flux_insee.temp_flux	
	SET nom_commune_destination = 'Paris'
		WHERE commune_destination IN ('75101', '75102', '75103', '75104', '75105', '75106', '75107', '75108', '75109', '75110', '75111', '75112', '75113', '75114', '75115', '75116', '75117', '75118', '75119', '75120');

UPDATE flux_insee.temp_flux	
	SET nom_commune_destination = 'Marseille'
		WHERE commune_destination IN ('13201', '13202', '13203', '13204', '13205', '13206', '13207', '13208', '13209', '13210', '13211', '13212', '13213', '13214', '13215', '13216');

UPDATE flux_insee.temp_flux	
	SET commune_destination = '69123'
		WHERE nom_commune_destination = 'Lyon';

UPDATE flux_insee.temp_flux	
	SET commune_destination = '75056'
		WHERE nom_commune_destination = 'Paris';

UPDATE flux_insee.temp_flux	
	SET commune_destination = '13055'
		WHERE nom_commune_destination = 'Marseille';

UPDATE flux_insee.temp_flux
	SET temp_origine_flux = 'Oui'
	FROM flux_insee.territoire
		WHERE territoire.insee = temp_flux.commune_origine;
UPDATE flux_insee.temp_flux
	SET temp_destination_flux = 'Oui'
	FROM flux_insee.territoire
		WHERE territoire.insee = temp_flux.commune_destination;

UPDATE flux_insee.temp_flux
	SET type_flux = 'Sortant'
		WHERE temp_origine_flux = 'Oui' AND temp_destination_flux IS NULL;

UPDATE flux_insee.temp_flux
	SET type_flux = 'Entrant'
	WHERE temp_origine_flux IS NULL AND temp_destination_flux = 'Oui';

UPDATE flux_insee.temp_flux
	SET type_flux = 'Interne'
	WHERE temp_origine_flux = 'Oui' AND temp_destination_flux = 'Oui';

UPDATE flux_insee.temp_flux
	SET type_flux = 'Intra'
		WHERE temp_flux.commune_origine = temp_flux.commune_destination;


UPDATE flux_insee.temp_flux
	SET id_concatener = commune_origine||commune_destination;
		

CREATE TABLE flux_insee.temp_flux_v2 AS
	SELECT commune_origine||commune_destination as id_concatener, commune_origine, nom_commune_origine, commune_destination, nom_commune_destination, age, mode_de_transport, csp, SUM(flux) as flux, type_flux
	FROM flux_insee.temp_flux		
GROUP BY id_concatener, commune_origine, nom_commune_origine, commune_destination, nom_commune_destination, age, mode_de_transport, csp, type_flux;


CREATE TABLE flux_insee.temp_flux_v3 AS
SELECT id_concatener, commune_origine, nom_commune_origine, commune_destination, nom_commune_destination, SUM(flux) as flux, type_flux
FROM flux_insee.temp_flux
GROUP BY id_concatener, commune_origine, nom_commune_origine, commune_destination, nom_commune_destination, type_flux;
""")
print("Requête SQL réalisée")
conn.commit()

#export des requêtes
#with open ('C://DT_details_flux.csv','w') as fdet:
#    lst_det = []
#    cur.execute("SELECT * FROM flux_insee.temp_flux_v2")
#    for i in range(cur.rowcount):
#        row = cur.fetchone()
#        lst_det.append(row)
#    
##    print(lst_det)
#    wr = csv.writer(fdet, quoting=csv.QUOTE_ALL)
#    wr.writerow(lst_det)

sql = "COPY flux_insee.temp_flux_v2 TO STDOUT WITH CSV HEADER ENCODING 'utf-8' DELIMITER ','"

with open ('C://DT_details_flux.csv','w') as f:
    cur.copy_expert(sql, f)
    
sql = "COPY flux_insee.temp_flux_v3 TO STDOUT WITH CSV HEADER ENCODING 'utf-8' DELIMITER ','"

with open ('C://DT_synthese_flux.csv','w') as f:
    cur.copy_expert(sql, f)
    
print("Fichiers créés dans C://")

#efface les tables temporaires
cur.execute("""
DROP TABLE flux_insee.temp_flux;
DROP TABLE flux_insee.temp_flux_v2;
DROP TABLE flux_insee.temp_flux_v3;
""")
print("Tables temporaires effacées")

conn.commit()

conn.close()

print("Traitement terminé")
