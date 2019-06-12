import csv
import sys

filename = sys.argv[1]
absfilename = filename.split("/")[1]
outputfiledir = sys.argv[2]
csvFile = open(filename.strip(),"r")
reader = csv.reader(csvFile)
jointCoord = []

# order is joint name ,x , y ,z
oneFrameJoint = []
i = 0 
for line in reader :
	try: 
		if(line[2][0] != "J" ) :
			continue
		# print(i)
		# print("line: " + str(line))
		if(i % 25== 0 and i != 0) :
			jointCoord.append(oneFrameJoint)
			oneFrameJoint = []
		#print(str(i) + " : " + str(line[2]) + " : " + str(len(line[2])))
		oneFrameJoint.append(line[2])
		oneFrameJoint.append(line[7])
		oneFrameJoint.append(line[8])
		oneFrameJoint.append(line[9])
		# print("oneFrameJoint: " + str(oneFrameJoint) )
	except:
		continue;
	i+= 1
totalBvhFrames = (i/25)

outputfilename = outputfiledir+absfilename[:-5] + "_processed_"+str(totalBvhFrames)+".csv" 

with open(outputfilename, "w") as f:
    writer = csv.writer(f)
    writer.writerows(jointCoord) 
