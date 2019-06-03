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
MHX2List = getFiles("/Users/daddysHome/Downloads",".mhx2")
BVHList = getFiles("/Users/daddysHome/Downloads/kinect2bvh 2",".bvh")
backgroundImages = getFiles("/Users/daddysHome/Downloads/backgroundImage",".jpg")
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
for i in range(scn):
    bpy.context.scene.world = bpy.data.worlds[0]
    texture.image=img
    # scene = bpy.context.screen.scenes
    # screen = bpy.context.screen
    bpy.ops.object.camera_add()
    bpy.ops.object.lamp_add(type='HEMI')
    bpy.ops.import_scene.makehuman_mhx2(filepath = MHX2List[i])
    person = bpy.data.scenes[i].objects[2].name
    bpy.context.scene.camera = bpy.data.objects[bpy.data.cameras[i].name]
    bpy.data.scenes[i].objects[bpy.data.cameras[i].name].location = Vector((-1.6719582080841064, -41.433406829833984, 4.720533847808838))
    bpy.data.scenes[i].objects[bpy.data.cameras[i].name].rotation_euler = Euler((1.6681835651397705, -0.0017817476764321327, 6.209451198577881), 'XYZ')
    bpy.data.scenes[i].objects[bpy.data.cameras[i].name].scale = Vector((1.4308398962020874, 1.4057042598724365, 1.8842936754226685))
    bpy.data.scenes[i].objects[bpy.data.lamps[i].name].location = Vector((-1.6768434047698975, -5.329115867614746, 38.93578338623047))
    bpy.data.scenes[i].objects[bpy.data.lamps[i].name].rotation_euler = Euler((0.032153837382793427, 0.0016589768929407, 4.444016933441162), 'XYZ')
    for j in range(len(BVHList)):
        bpy.ops.mcp.load_and_retarget(filter_glob = ".bvh",filepath = BVHList[j])
        bpy.data.scenes[i].frame_start = 1
        bpy.data.scenes[i].frame_end = 50
        bpy.data.scenes[i].render.image_settings.file_format = 'FFMPEG'
        bpy.data.scenes[i].render.filepath = "/Users/daddysHome/Downloads/animation/"+MHX2List[i][28:len(MHX2List[i])-5]+"/"+BVHList[j][40:len(BVHList[j])-5]
        bpy.context.scene.render.use_overwrite = False
        bpy.ops.render.render(animation=True)
        

    bpy.ops.scene.new(type="NEW")
    # bpy.context.scene=bpy.data.scenes[i+1]
