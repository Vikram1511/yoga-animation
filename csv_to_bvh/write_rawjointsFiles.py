import os
scriptpath = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(scriptpath,"rawCSV/")
path=path.replace("\\","/")
textfile_path = os.path.join(scriptpath,"raw_csv.txt")
pp = open(textfile_path, "w")
#basedir = "/mnt/project2/Kinect/data/joints/"

for r,d,f in os.walk(path):
    for file in f:
        if ".csv" in file:
            pp.write(str(path)+file+"\n")
