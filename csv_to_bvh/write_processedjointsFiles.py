import os
scriptpath = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(scriptpath,"processedCSV/")
path = path.replace("\\","/")
textfile_path = os.path.join(scriptpath,"processed_csv.txt")
pp = open(textfile_path, "w")

for r,d,f in os.walk(path):
    for file in f:
        if ".csv" in file:
            pp.write(path+file+"\n")  
        
