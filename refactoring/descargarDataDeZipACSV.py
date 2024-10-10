import os
from urllib.request import urlretrieve
from zipfile import ZipFile
import sys


class descargarDataDeZipACSV:
    def __init__(self,url,zippath,csvpath):
        self.url = url
        self.zippath = zippath
        self.csvpath = csvpath
        self.descargarDeUrl()
        self.extraerDeZip()
        self.borrarZip()

    def descargarDeUrl(self):
        urlretrieve(self.url,self.zippath)

    def extraerDeZip(self):
        with ZipFile(self.zippath) as zObject: 
                zObject.extractall(path=self.csvpath)
    
    def borrarZip(self):
        os.remove(self.zippath)

if __name__ == '__main__':
    url=sys.argv[1]
    zippath=sys.argv[2]+"/"+sys.argv[3]
    csvpath=sys.argv[2]
    descargarDataDeZipACSV(url,zippath,csvpath)