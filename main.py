from downloadZipFile import *

url="https://archive.ics.uci.edu/static/public/878/cirrhosis+patient+survival+prediction+dataset-1.zip"
path="./data/cirrhosis.zip"
destination="./data"

fileDownloader = downloadFileFromURL(url,path)
pathOfFile=fileDownloader()
extractor = zipExtractor(pathOfFile,destination)
pathofFiles = extractor()
extractor.deleteZip()