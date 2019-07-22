import os
import sys
scriptpath = os.path.dirname(os.path.realpath(__file__))
basedir = sys.argv[1]
path = os.path.join(scriptpath,"rawCSV/")
path=path.replace("\\","/")
basedir=basedir.replace("\\","/")
print(basedir)
textfile_path = os.path.join(scriptpath,"raw_csv.txt")
pp = open(textfile_path, "w")
#basedir = "/mnt/project2/Kinect/data/joints/"

for r,d,f in os.walk(basedir):
    for file in f:
        if ".csv" in file:
            print(file)
            pp.write(str(basedir)+file+"\n")
