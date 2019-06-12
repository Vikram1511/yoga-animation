import os

pp = open("processed_csv.txt", "w")

for r,d,f in os.walk("processedCSV/"):
    for file in f:
        if ".csv" in file:
            pp.write("../processedCSV/"+file+"\n")  
        