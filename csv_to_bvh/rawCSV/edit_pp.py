import os

pp = open("pp.txt", "w")

for r,d,f in os.walk("./"):
    for file in f:
        if ".csv" in file:
            pp.write("../rawCSV/"+file+"\n")

