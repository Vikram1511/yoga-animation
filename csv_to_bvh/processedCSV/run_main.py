import os

for r,d,f in os.walk("./"):
    for file in f:
        if ".csv" in file:
            pp = open("pp.txt", "w")
            pp.write("../processedCSV/"+file)
            pp.close()
            os.system("myBVHgenerator.bat")
            
        