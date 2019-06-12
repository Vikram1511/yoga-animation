import os

pp = open("raw_csv.txt", "w")

for r,d,f in os.walk("rawCSV/"):
    for file in f:
        if ".csv" in file:
            pp.write("rawCSV/"+file+"\n")
