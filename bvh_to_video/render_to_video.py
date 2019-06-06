import bpy
import os
from math import *
from mathutils import *
import random
    
bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.delete(use_global=False)

def getFiles(folderpath,extension):
    path = folderpath
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if extension in file:
                files.append(os.path.join(r, file))
    return files

# filep1 = "~/Downloads/person2.mhx2"
# filep2 = "/Users/daddysHome/Downloads/tpose_sample.mhx2"

# filebvh1 = "/Users/daddysHome/Downloads/kinect2bvh 2/Subj002_Katichakrasana_joints_processed.bvh"
mhx2path = "C:/Users/Vikram Jain/Documents/GitHub/yoga-pose-estimation/characters"
bvhpath = "C:/Users/Vikram Jain/Documents/GitHub/yoga-pose-estimation/bvhFiles"
backgroundpath ="C:/Users/Vikram Jain/Documents/GitHub/yoga-pose-estimation/BackgroundImages"
OutputDirPath = "C:/Users/Vikram Jain/Documents/GitHub/yoga-pose-estimation/Animation/"

MHX2List = getFiles(mhx2path,".mhx2")
BVHList = getFiles(bvhpath,".bvh")
backgroundImages = getFiles(backgroundpath,".jpg")
for a in bpy.context.screen.areas:
        if a.type == "VIEW_3D":
            break
a.spaces[0].show_background_images=True
img = bpy.data.images.load(backgroundImages[0])
scn = len(MHX2List)
texture = bpy.data.textures.new("Texture.001","IMAGE")
bpy.data.worlds['World'].active_texture = texture
bpy.context.scene.world.texture_slots[0].use_map_horizon=True
bpy.data.worlds[0].use_sky_paper = True
rootlen = len(mhx2path)
for i in range(scn):
    bpy.context.scene.world = bpy.data.worlds[0]
    texture.image=img
    # scene = bpy.context.screen.scenes
    # screen = bpy.context.screen
    bpy.ops.object.camera_add()
    bpy.ops.object.lamp_add(type='HEMI')
    bpy.ops.import_scene.makehuman_mhx2(filepath = MHX2List[i])
    person_name = MHX2List[i][rootlen+1:-5].capitalize()
    for bone in bpy.data.objects[person_name].pose.bones:
        bone.rotation_mode = "ZXY"
    person = bpy.data.scenes[i].objects[2].name
    bpy.context.scene.camera = bpy.data.objects[bpy.data.cameras[i].name]
    bpy.data.scenes[i].objects[bpy.data.cameras[i].name].location = Vector((0, -5, 0))
    bpy.data.scenes[i].objects[bpy.data.cameras[i].name].rotation_euler = Euler((1.57, 0, 6.28), 'XYZ')
    bpy.data.scenes[i].objects[bpy.data.cameras[i].name].scale = Vector((0.5, 0.5, 0.5))
    bpy.data.scenes[i].objects[bpy.data.lamps[i].name].location = Vector((-1.6768434047698975, -5.329115867614746, 38.93578338623047))
    bpy.data.scenes[i].objects[bpy.data.lamps[i].name].rotation_euler = Euler((0.032153837382793427, 0.0016589768929407, 4.444016933441162), 'XYZ')
    for j in range(len(BVHList)):
        bpy.ops.mcp.load_and_retarget(filter_glob = ".bvh",filepath = BVHList[j])
        bpy.data.scenes[i].frame_start = 1
        bpy.data.scenes[i].frame_end = 50
        bpy.data.scenes[i].frame_step = 1
        bpy.data.scenes[i].render.image_settings.file_format = 'FFMPEG'
        bpy.data.scenes[i].render.filepath = OutputDirPath+MHX2List[i][len(mhx2path):len(MHX2List[i])-5]+"/"+BVHList[j][len(bvhpath):len(BVHList[j])-4]
        bpy.context.scene.render.use_overwrite = False
        bpy.ops.render.render(animation=True)
        

    bpy.ops.scene.new(type="NEW")
    # bpy.context.scene=bpy.data.scenes[i+1]
