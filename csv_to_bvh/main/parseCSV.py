import csv
import sys
import math 

filename = sys.argv[1]
#filename = "C:/Users/Vikram Jain/Documents/Remote_Access_Cerebrum/yoga-animation/csv_to_bvh/rawCSV/Subj001_Ardhachakrasana_C1N_joints.csv"
pathArr = filename.split("/")
absfilename = pathArr[len(pathArr)-1]
outputfiledir = sys.argv[2]
#outputfiledir = "C:/Users/Vikram Jain/Documents/Remote_Access_Cerebrum/yoga-animation/csv_to_bvh/main"
csvFile = open(filename.strip(),"r")
reader = csv.reader(csvFile)
jointCoord = []


#function for linear interpolation
def linear_interpolation(x1,y1,x2,y2,x):
	term1 = float((x-x1)*(y2-y1))
	term2 = float((x2-x1))
	return (y1+float(term1/term2))

# order is joint name ,x , y ,z,label(tracked or inferred)
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
			if(len(jointCoord)>0):

				#timestamp for previous frame
				prev_time = float(jointCoord[len(jointCoord)-1][0])

				#joints location for previous frame
				prev_oneFrameJoint = jointCoord[len(jointCoord)-1]

				#time interval between current frame and previous frame
				time_interval = float(totalTime) - prev_time

				#since fps=15(0.067sec per frame) for our joints data by Kinect SDK therefor
				if(time_interval>=0.134):
					#print(time_interval)
					extra_data = []

					#number of frames to be inserted between previous and current frame by linear interpolation
					nof_tbi = math.floor(float((time_interval/0.067)))
					#print(nof_tbi)

					for j in range(nof_tbi):
						extra_data_per_frame= []
						extra_data_per_frame.append(str(prev_time+(j+1)*0.067))
						for k in range(1,len(oneFrameJoint)):

							#to get data for linear interpolation for each coordinate axis
							if(k%5!=1 and k%5!=0):
								x1 = prev_time
								x2 = float(totalTime)
								x = x1+float((j+1)*0.067)
								y1 = float(prev_oneFrameJoint[k])
								y2 = float(oneFrameJoint[k])

							#joint name
							if(k%5==1):
								extra_data_per_frame.append(oneFrameJoint[k])
							#x-coordinate for joint
							elif(k%5==2):
								next_insertdata = linear_interpolation(x1,y1,x2,y2,x)
								extra_data_per_frame.append(next_insertdata)
							#y-coordinate for joint
							elif(k%5==3):
								next_insertdata = linear_interpolation(x1,y1,x2,y2,x)
								extra_data_per_frame.append(next_insertdata)
							#z-coordinate for joint
							elif(k%5==4):
								next_insertdata = linear_interpolation(x1,y1,x2,y2,x)
								extra_data_per_frame.append(next_insertdata)
							
							#label for joint coordinates which should be inferred not tracked
							else:
								extra_data_per_frame.append("inferred")
						extra_data.append(extra_data_per_frame)
					jointCoord.extend(extra_data)
					#print(extra_data)
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
			prev_time = totalTime
			oneFrameJoint.append(totalTime)
			timestamp = True
		
		oneFrameJoint.append(line[2])
		oneFrameJoint.append(line[7])
		oneFrameJoint.append(line[8])
		oneFrameJoint.append(line[9])
		#tracked or inferred
		oneFrameJoint.append(line[3])
	except:
		continue;
	i+= 1
totalBvhFrames = int(len(jointCoord))

outputfilename = outputfiledir+absfilename[:-5] + "_processed_"+str(totalBvhFrames)+".csv" 

with open(outputfilename, "w") as f:
    writer = csv.writer(f)
    writer.writerows(jointCoord) 
