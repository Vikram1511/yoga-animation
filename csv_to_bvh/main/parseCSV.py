import csv
import sys

filename = sys.argv[1]
#filename = "C:/Users/Vikram Jain/Documents/GitHub/yoga-pose-estimation/csv_to_bvh/main/joints.csv"
pathArr = filename.split("/")
absfilename = pathArr[len(pathArr)-1]
outputfiledir = sys.argv[2]
#outputfiledir = "C:/Users/Vikram Jain/Documents/GitHub/yoga-pose-estimation/csv_to_bvh/main"
csvFile = open(filename.strip(),"r")
reader = csv.reader(csvFile)
jointCoord = []

# order is joint name ,x , y ,z
oneFrameJoint = []
i = 0 
timestamp = False
for line in reader :
	try:
		if(line[2][0] != "J" ) :
			continue;
		# print(i)
		# print("line: " + str(line))
		if(i % 25== 0 and i != 0) :
			jointCoord.append(oneFrameJoint)
			#print(jointCoord)
			oneFrameJoint = []
			timestamp=False
		if(timestamp==False):
			splitted = line[1].split(".")
			timeHMS = splitted[0]
			timeMicroSec = splitted[1]
			arr_timeHMS =  splitted[0].split(":")
			H_time = int(arr_timeHMS[0])
			M_time = int(arr_timeHMS[1])
			S_time = int(arr_timeHMS[2])
			#neglecting Hourse stamp
			totalTime = str(M_time*60 + S_time)+"."+splitted[1]
			oneFrameJoint.append(totalTime)
			timestamp = True
		#print(str(i) + " : " + str(line[2]) + " : " + str(len(line[2])))
		oneFrameJoint.append(line[2])
		oneFrameJoint.append(line[7])
		oneFrameJoint.append(line[8])
		oneFrameJoint.append(line[9])
		#tracked or inferred
		oneFrameJoint.append(line[3])
		# print("oneFrameJoint: " + str(oneFrameJoint) )
	except:
		continue;
	i+= 1
totalBvhFrames = (i/25)

outputfilename = outputfiledir+absfilename[:-5] + "_processed_"+str(totalBvhFrames)+".csv" 

with open(outputfilename, "w") as f:
    writer = csv.writer(f)
    writer.writerows(jointCoord) 
