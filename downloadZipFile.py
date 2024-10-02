from typing import Any
from urllib.request import urlretrieve
from zipfile import ZipFile
import os

class downloadFileFromURL:

    def __init__(self, url, path):
        self.path=path
        self.url=url

    def __call__(self):
        try:
            urlretrieve(self.url,self.path)
            print(f"The file from {self.url} has been downloaded and saved in {self.path}")
        except Exception as e:
            print(f"The following error has ocurred by trying to download the file: {e}")
            raise Exception("Error downloading the file")
        return self.path
    
class zipExtractor:

    def __init__(self,origin,destination):
        self.origin = origin
        self.destination = destination

    def __call__(self):
        try:
            with ZipFile(self.origin) as zObject: 
                zObject.extractall(path=self.destination)
                print(f"File {self.origin} has been succesfully extracted into {self.destination}")
        except Exception as e:
            print(f"The following error has ocurred when extracting the file {self.origin} into {self.destination}: {e}")
            raise Exception("Errorextracting zip file")
        return self.destination

    def deleteZip(self):
        try:
            os.remove(self.origin)
            print(f"Zip File {self.origin} succesfuly removed")
        except Exception as e:
            print(f"error deleting the file {self.origin}, with following error:{e}")



