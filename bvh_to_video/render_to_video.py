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
    bpy.ops.import_scene.makehuman_mhx2(filepath = MHX2List[i],useOverride = True,rigType = "MHX")
    # for fk to ik switching of leg bones

    #bpy.ops.mhx2.toggle_fk_ik(toggle="MhaLegIk_L 1 4 5")
    #bpy.ops.mhx2.toggle_fk_ik(toggle="MhaLegIk_R 1 20 21")
    ## bpy.ops.mhx2.toggle_fk_ik(toggle="MhaArmIk_L 1 2 3")   - arm is not necessary
    ## bpy.ops.mhx2.toggle_fk_ik(toggle="MhaArmIk_R 1 18 19")  - arm is not necessary
    person_name = MHX2List[i][rootlen+1:-5].capitalize()
    person = bpy.data.scenes[i].objects[2].name
    bpy.context.scene.camera = bpy.data.objects[bpy.data.cameras[i].name]
    bpy.data.scenes[i].objects[bpy.data.cameras[i].name].location = Vector((0, -5, 0))
    bpy.data.scenes[i].objects[bpy.data.cameras[i].name].rotation_euler = Euler((1.57, 0, 6.28), 'XYZ')
    bpy.data.scenes[i].objects[bpy.data.cameras[i].name].scale = Vector((0.5, 0.5, 0.5))
    bpy.data.scenes[i].objects[bpy.data.lamps[i].name].location = Vector((-1.6768434047698975, -5.329115867614746, 38.93578338623047))
    bpy.data.scenes[i].objects[bpy.data.lamps[i].name].rotation_euler = Euler((0.032153837382793427, 0.0016589768929407, 4.444016933441162), 'XYZ')
    
    bpy.data.scenes[i].render.engine="CYCLES"
    bpy.data.scenes[i].cycles.device="GPU"

    prefs = bpy.context.user_preferences
    cprefs = prefs.addons['cycles'].preferences

    # Attempt to set GPU device types if available
    for compute_device_type in ('CUDA', 'OPENCL', 'NONE'):
        try:
            cprefs.compute_device_type = compute_device_type
            break
        except TypeError:
            pass

    # Enable all CPU and GPU devices
    for device in cprefs.devices:
            device.use = True
            
    for j in range(len(BVHList)):
        file_bvh = BVHList[j]
        arr = file_bvh.split(".")
        arr = arr[0].split("_")
        frame_end = int(arr[len(arr)-1])
        bpy.data.scenes[i].McpEndFrame = frame_end
        bpy.ops.mcp.load_and_retarget(filter_glob = ".bvh",filepath = file_bvh)
        frame_range = bpy.data.objects[person_name].animation_data.action.frame_range[1]
        #for simplyfying f curves 

        #bpy.data.scenes[i].McpShowIK=True
        #bpy.data.scenes[i].McpFkIkArms=False
        #bpy.ops.mcp.transfer_to_ik()
        bpy.ops.mcp.simplify_fcurves()
        bpy.ops.graph.simplify(error=0.10)
        bpy.data.scenes[i].frame_start = 1
        bpy.data.scenes[i].frame_end = frame_end
        bpy.data.scenes[i].frame_step = 1
        bpy.data.scenes[i].render.fps=60
        bpy.data.scenes[i].render.image_settings.file_format = 'FFMPEG'
        bpy.data.scenes[i].render.filepath = OutputDirPath+MHX2List[i][len(mhx2path):len(MHX2List[i])-5]+"/"+BVHList[j][len(bvhpath):len(BVHList[j])-4]
        bpy.context.scene.render.use_overwrite = False
        
        
    
        bpy.ops.render.render(animation=True)
        

        bpy.ops.scene.new(type="NEW")
        # bpy.context.scene=bpy.data.scenes[i+1]
