import bpy
import os
from math import *
from mathutils import *
    
bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.delete(use_global=False)

mhx2path = "C:/Users/Vikram Jain/Documents/GitHub/yoga-pose-estimation/characters"
bvhpath = "C:/Users/Vikram Jain/Documents/GitHub/yoga-pose-estimation/bvhFiles"
OutputDirPath = "C:/Users/Vikram Jain/Documents/GitHub/yoga-pose-estimation/Animation"

def getFiles(folderpath,extension):
    path = folderpath
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if extension in file:
                files.append(os.path.join(r, file))
    return files

#to get mhx2 files and bvh files in list


MHX2List = getFiles(mhx2path,".mhx2")
BVHList = getFiles(bvhpath,".bvh")
#defining number of scenes which is equal to number of characters we have
scn = len(MHX2List)

#loop for each scene 
for i in range(scn):
	#adding camera
    bpy.ops.object.camera_add()   

    #adding lamp                         																	 
    bpy.ops.object.lamp_add(type='HEMI')	

    #importing make human file in blender from list which contains all the files with extension ".mhx2" with their path																	
    bpy.ops.import_scene.makehuman_mhx2(filepath = MHX2List[i])		

    #setting current scene's camera for rendering the current scene's animation
    bpy.context.scene.camera = bpy.data.objects[bpy.data.cameras[i].name]

    #setting location for camera,lamp for current scene which will be same for all the scene
    bpy.data.scenes[i].objects[bpy.data.cameras[i].name].location = Vector((-1.6719582080841064, -41.433406829833984, 4.720533847808838))
    bpy.data.scenes[i].objects[bpy.data.cameras[i].name].rotation_euler = Euler((1.6681835651397705, -0.0017817476764321327, 6.209451198577881), 'XYZ')
    bpy.data.scenes[i].objects[bpy.data.cameras[i].name].scale = Vector((1.4308398962020874, 1.4057042598724365, 1.8842936754226685))
    bpy.data.scenes[i].objects[bpy.data.lamps[i].name].location = Vector((-1.6768434047698975, -5.329115867614746, 38.93578338623047))
    bpy.data.scenes[i].objects[bpy.data.lamps[i].name].rotation_euler = Euler((0.032153837382793427, 0.0016589768929407, 4.444016933441162), 'XYZ')

    #load_and_retarget bvh files
    #looping through all the bvh files which exist in our list "BVHList" and retarget for each character in one scene
    for j in range(len(BVHList)):
        bpy.ops.mcp.load_and_retarget(filter_glob = ".bvh",filepath = BVHList[j])

        #setting frames start and end , we can change accordingly or even can find the appropriate frames for each bvh file and set it as end frame value
        bpy.data.scenes[i].frame_start = 1
        bpy.data.scenes[i].frame_end = 50

        #setting image file format for rendering
        bpy.data.scenes[i].render.image_settings.file_format = 'FFMPEG'

        #setting directory for rendered animation video which will have multiple directory and named by character name and will have all the animation videos for that character
        bpy.data.scenes[i].render.filepath = OutputDirPath+MHX2List[i][len(mhx2path):len(MHX2List[i])-5]+"/"+BVHList[j][len(bvhpath):len(BVHList[j])-4]
        
        #to not overwrite the animated videos
        bpy.context.scene.render.use_overwrite = False
        bpy.ops.render.render(animation = True)

    #after rendering all videos for one character, we will generate new scene in blender for next character
    bpy.ops.scene.new(type="NEW")
    
    #set new generated scene as context scene
    bpy.context.screen.scene=bpy.data.scenes[i+1]
