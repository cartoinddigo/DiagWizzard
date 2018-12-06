# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from IsoIgnQt import Ui_Isochrones_IGN
import sys
import csv, requests, json, math, time, mmap, sys, os, urllib

appver = "IDD Isochrones IGN 2.2"
headers = {'User-Agent':'*'}

class IGN:
    """Classe regroupant les fonction de l'PAI IGN Isochrones"""
    def __init__(self):
        toto="toto"
        
    def show_entry_fields(self,p_olat, p_olng, p_dist):
    
        self.coord = p_olat,p_olng
        self.dist = p_dist
        self.coord = ','.join(self.coord)
        #result = isochrone(coord)
        #print (coord)
        self.urla = 'http://wxs.ign.fr/c98qkvawt3ygddluuz68vybf/isochrone/isochrone.json?location='
        #self.urlb = '&smoothing=true&holes=false&reverse=true&method=time&time=' #<- pour recherche durée

        self.urlb = '&smoothing=true&holes=false&reverse=true&method=distance&distance=' #<- pour recherche distance
        self.urlc = '&graphName=Voiture&srs=EPSG:4326'
        self.destination = self.coord
        self.distance = self.dist
        self.urlq = self.urla+self.destination+self.urlb+self.distance+self.urlc
        print (self.urlq)
        self.resp = requests.get(self.urlq, headers=headers)
        print (self.resp)
        self.iso_output = self.resp.json()
        self.iso_output_str = json.dumps(self.iso_output, sort_keys=True, indent=2)
        self.iso_statu = self.iso_output['status']
        try:
            #print (iso_output_str)
            self.pgeom = self.iso_output['wktGeometry']
            return (self.pgeom)
            print (urlq)

    
        except:
            self.iso_statu == "ERROR"
            print (self.iso_statu,'\n',self.iso_output['message'])

class IsoIGN(QtGui.QMainWindow):
    
    def __init__(self, title = "Default", parent = None):
        
        super (IsoIGN, self).__init__(parent)
        self.title = title
        self.ui = Ui_Isochrones_IGN()
        self.ui.setupUi(self)
        self.setWindowTitle(self.title)
        self._initSlotButtons()
        
    def consol(self, message):
        """Fonction de gestion de l'affichage des consignes
        dans la console"""
        self.txt0 = message
        print (self.txt0)
        self.ui.console.setHtml(self.txt0)
        
    def consolresult(self, message):
        """Fonction de gestion de l'affichage des resultats
        dans la console"""
        self.txt0 = message
        print (self.txt0)
        self.ui.console.append(self.txt0)
        QtGui.QApplication.processEvents()

    def _initSlotButtons(self):
        self.ui.btSource.clicked.connect(self.chargerfichier)
        self.ui.btSave.clicked.connect(self.exportresult)
        self.ui.btSource_2.clicked.connect(self.BtExecuter)

    def chargerfichier(self):
        """Fonction de chargement des données en entree"""
        self.pbarval = 0
        try:
            self.fichiersal = QtGui.QFileDialog.getOpenFileName(self, "Selectionnez le fichiers sources", "/sources", "*.csv")
            with open(self.fichiersal, "r+") as f:
                
                self.buf = mmap.mmap(f.fileno(), 0)
                self.lines = 0
                self.readline = self.buf.readline
                while self.readline():
                    self.lines += 1
                self.line_result = str(self.lines)
                self.msgcharge = ('Ce fichier compte '+self.line_result) #Tester si la dernière ligne est vide
                self.consol(self.msgcharge)
                self.salvalid = 1
                self.pbarmax = int(self.line_result)
                
        except IOError as e:
            self.salvalid = 0
            self.msgcharge = "<h2>Impossible d'ouvrir le fichier</h2>"+"I/O error({0}): {1}".format(e.errno, e.strerror)+"<br>Erreure lors de l'ouverture du fichier.<br><br>Est-il déjà ouvert dans Excel ou une autre application ?"
            self.consol(self.msgcharge)
            
    def exportresult(self):
        """Fonction de chargement de l'emplacement des resultats"""
        try:
            self.resultfichier = QtGui.QFileDialog.getSaveFileName(self, "Selectionnez l'emplacement et donnez un nom", "/results", "*.csv")
            ext = self.resultfichier[-4:]
            #print (ext)
            try:
                ext != ".csv"
                self.resultfichier = self.resultfichier
            except :
                self.resultfichier = self.resultfichier.replace('.csv','')

            self.msgcharge = ('Les résultats seront enregistrés dans le fichier :<br>'+self.resultfichier)
            self.consol(self.msgcharge)
            self.testsave = 1
        except IOError as e:
            self.msgcharge = ("Impossible d'enregistrer le fichier<br>"+"I/O error({0}): {1}".format(e.errno, e.strerror)+"<br>Erreure lors de l'écriture du fichier.<br>Est-il déjà ouvert dans Excel\nou une autre application ?")
            self.consol(self.msgcharge)

    def BtExecuter(self):
        """Action sur le Boutont Executer"""
        self.consol("Initialisation de la recherche...")
        try:
            fichier = open(self.fichiersal)
        except IOError as e:
            self.msgcharge = (e)
            self.consol(self.msgcharge)
            print (e)
        self.rechercherIGN()

    def rechercherIGN(self):
        """Fonction de construction du resultat"""
        self.consol('\n\n\nDébut de la recherche le:\n\n'+time.strftime('%d/%m/%y %H:%M',time.localtime())+'\n\n\n')
        ign = IGN()

        with open(self.fichiersal) as f:
            with open(self.resultfichier, 'w')as sortie:
                csv_out=csv.writer(sortie, delimiter=';', lineterminator='\n')
                csv_out.writerow(['poi',
                                  'latitude',
                                  'longitude',
                                  'dist',
                                  'geom'])
                reader = csv.reader(f, delimiter = ";")
                next (reader, None)
                self.lstresult=[]
                for row in reader:
                    #time.sleep(.500)
                    p_id = row[0]
                    p_olat = row[1]
                    p_olng = row[2]
                    p_dist = row[3]

                    pgeom = ign.show_entry_fields(p_olat, p_olng, p_dist)




                    result = p_id,p_olat,p_olng,p_dist,pgeom
                    self.msgcharge = str(result).strip('()')
                    #self.consol = str(self.resultgui).replace("'",'')
                    #self.consol = str(self.resultgui).replace(" ",'')
                    #self.consol = str(self.resultgui).replace(",",';')                    

                    #print(self.resultgui)
                    csv_out.writerow((p_id,p_olat,p_olng,p_dist,pgeom))
                    self.line_result = str(self.lines)
                    
                    #self.msgcharge = (self.resultgui)
                    #self.lblresult.insert(0.0, '\n'+str(self.msgcharge))
                    self.consolresult(self.msgcharge)
                    #self.lblresult.update()
           
        f.close()
        sortie.close()
        print ('ok')
        self.consolresult("\nOk, votre recherche s'est achevée le\n"+time.strftime('%d/%m/%y %H:%M',time.localtime()) +"\nLes résultats sont enregistrés dans le fichier "+self.resultfichier+"\n")


if __name__ == "__main__" :
    app = QtGui.QApplication(sys.argv)
    w = IsoIGN("Isochrones @IGN")
    w.show()
    sys.exit(app.exec_())
