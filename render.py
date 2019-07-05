import bpy
import bpy_extras
import os
from math import *
import sys
from mathutils import *
import random
import argparse
from bpy_extras.object_utils import world_to_camera_view


script_path = os.path.dirname(os.path.realpath(__file__))
print(script_path)

#class for parsing argument for blender python script
class ArgumentParserForBlender(argparse.ArgumentParser):
    def _get_argv_after_doubledash(self):
        try:
            idx = sys.argv.index("--")
            return sys.argv[idx+1:] # the list after '--'
        except ValueError as e: # '--' not in the list:
            return []

    # overrides superclass
    def parse_args(self):
        return super().parse_args(args=self._get_argv_after_doubledash())


bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.delete(use_global=False)


def pointTracking(scene,person_body,scene_camera_name,frame_number):
        # needed to rescale 2d coordinates
        render = scene.render
        res_x = render.resolution_x
        res_y = render.resolution_y

        obj = bpy.data.objects[person_body]
        cam = bpy.data.objects[scene_camera_name]

        # use generator expressions () or list comprehensions []
        total_vg = len(obj.vertex_groups.items())
        #print(total_vg)
        #print("inserting")
        for j in range(total_vg):
                vg_index= j
                vs = [v for v in obj.data.vertices if (vg_index in [vg.group for vg in v.groups])]
                #print(vs)
                vertc = (vert.co for vert in vs)
                coords_2d = [world_to_camera_view(scene, cam, coord) for coord in vertc]
                #print(coords_2d)
                # 2d data printout:
                rnd = lambda i: round(i)
                rnd3 = lambda i: round(i, 3)

                #limit_finder = lambda f: f(coords_2d, key=lambda i: i[2])[2]
                #limits = limit_finder(min), limit_finder(max)
                #limits = [rnd3(d) for d in limits]

                # x, y, d=distance_to_lens
                print('x,y,d')
                print("Vertex_group for:",obj.vertex_groups.items()[j][0])
                for x, y, d in coords_2d:
                    print("{},{},{}".format(rnd(res_x*x), rnd(res_y*y), rnd3(d)))


def getFiles(folderpath,extension):
    path = folderpath
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if extension in file:
                files.append(os.path.join(r, file).replace("\\","/"))
    return files

# filep1 = "~/Downloads/person2.mhx2"
# filep2 = "/Users/daddysHome/Downloads/tpose_sample.mhx2"

# filebvh1 = "/Users/daddysHome/Downloads/kinect2bvh 2/Subj002_Katichakrasana_joints_processed.bvh"


def render_to_video(Animation=True,point_tracking=False):
    #path for the file
    main_path = script_path

    #intitating inputs
    mhx2path = os.path.join(main_path,mhx2File)
    bvhpath = os.path.join(main_path,bvhFile)
    #backgroundpath =main_path+"/BackgroundImages"

    #output directory
    OutputDirPath = main_path+"\\Animation\\"
    
    #for background image of aimation
    for a in bpy.context.screen.areas:
            if a.type == "VIEW_3D":
                break
    a.spaces[0].show_background_images=True

    #img = bpy.data.images.load(backgroundImages[0])
    texture = bpy.data.textures.new("Texture.001","IMAGE")
    Material = bpy.data.materials.new("MyMaterial")
    #bpy.data.worlds['World'].active_texture = texture
    #bpy.context.scene.world.texture_slots[0].use_map_horizon=True
    #bpy.data.worlds[0].use_sky_paper = True
    rootlen = len(mhx2path)


    curr_scn = bpy.context.scene
    bpy.context.scene.world = bpy.data.worlds[0]
    #texture.image=img
    # scene = bpy.context.screen.scenes
    # screen = bpy.context.screen

    #adding canera for current scene
    bpy.ops.object.camera_add()

    #adding plane for floor and background
    bpy.ops.mesh.primitive_plane_add()
    bpy.ops.mesh.primitive_plane_add(rotation=(1.57,0,0))

    planeMeshList = []
    for plane in bpy.data.meshes.keys():
        if plane[:5]=="Plane":
            planeMeshList.append(plane)
    currPlane = planeMeshList[len(planeMeshList)-2]
    currWallPlane = planeMeshList[len(planeMeshList)-1]


    #adding a lamp(light source)
    bpy.ops.object.lamp_add(type="HEMI")

    #importing makehuman model
    bpy.ops.import_scene.makehuman_mhx2(filepath = mhx2path,useOverride = True,rigType = "MHX")


    # for fk to ik switching of leg bones
    #bpy.ops.mhx2.toggle_fk_ik(toggle="MhaLegIk_L 1 4 5")
    #bpy.ops.mhx2.toggle_fk_ik(toggle="MhaLegIk_R 1 20 21")
    ## bpy.ops.mhx2.toggle_fk_ik(toggle="MhaArmIk_L 1 2 3")   - arm is not necessary
    ## bpy.ops.mhx2.toggle_fk_ik(toggle="MhaArmIk_R 1 18 19")  - arm is not necessary

    #obtaining character model name (for ex. if file name is john.mhx2 it will give 'John' which is actually pointer to the model in blender)
    person_name = mhx2path.split("/")[-1]
    person_name = person_name[:-5].capitalize()

    #setting up current camera and lamp for current scene
    curr_camera_name = bpy.data.cameras[0].name
    curr_lamp_name = bpy.data.lamps[0].name
    curr_lamp = bpy.data.scenes[0].objects[bpy.data.lamps[0].name]
    curr_camera = bpy.data.scenes[0].objects[curr_camera_name]
    bpy.context.scene.camera = curr_camera

    #setting location and rotation for camera and lamp objects
    curr_camera.location = Vector((0, -3, 0))
    curr_camera.rotation_euler = Euler((1.57, 0, 6.28), 'XYZ')
    curr_camera.scale = Vector((0.5, 0.5, 0.5))
    curr_lamp.location = Vector((0.17385, 2.70460, 1.41230))
    curr_lamp.rotation_euler = Euler((0.032093837382793427, 0.0016589768929407, 4.444016933441162), 'XYZ')


    #setting up floor and wall plane
    curr_floor_level = bpy.data.scenes[0].objects[currPlane]
    curr_wall_level = bpy.data.scenes[0].objects[currWallPlane]

    #for floor level
    curr_floor_level.scale[0] = 10
    curr_floor_level.scale[1] = 10
    curr_floor_level.location = Vector((-3.34690,2.45708,-1.281453))

    #for background wall plane 
    curr_wall_level.scale[0] = 10
    curr_wall_level.scale[1] = 10
    curr_wall_level.location = Vector((-0.31573,5.26044,0.98139))

    #texture for floor
    curr_floor_level.active_material = Material
    curr_floor_level.active_material.diffuse_color =(0.155,0.373,0.400)


    # bpy.data.scenes[i].objects[currPlane].color[1] = 0.274
    # bpy.data.scenes[i].objects[currPlane].color[3] = 0.246
    # bpy.data.scenes[i].render.engine="CYCLES"
    # bpy.data.scenes[i].cycles.device="GPU"

    # prefs = bpy.context.user_preferences
    # cprefs = prefs.addons['cycles'].preferences

    # # Attempt to set GPU device types if available
    # for compute_device_type in ('CUDA', 'OPENCL', 'NONE'):
    #     try:
    #         cprefs.compute_device_type = compute_device_type
    #         break
    #     except TypeError:
    #         pass

    # # Enable all CPU and GPU devices
    # for device in cprefs.devices:
    #         device.use = True
            
    
    #for obtaining bvh file frames count
    file_bvh = bvhpath
    bvhFileName = file_bvh.split("/")[-1][:-4]
    arr = file_bvh.split("\\")
    arr = arr[-1].split("_")
    arr = arr[-1].split(".")

    #frame end is total number of frames present in bvh file
    frame_end = int(arr[0])

    #To set how many frame do we wanna retarget for the armature out of frame_end 
    bpy.data.scenes[0].McpEndFrame = 5

    #importing bvh file
    bpy.ops.mcp.load_and_retarget(filter_glob = ".bvh",filepath = file_bvh)

    #frame_range is equal to McpEndFrame(which we fixed before)
    frame_range = bpy.data.objects[person_name].animation_data.action.frame_range[1]

    #for simplyfying f curves 
    #bpy.data.scenes[i].McpShowIK=True
    #bpy.data.scenes[i].McpFkIkArms=False
    #bpy.ops.mcp.transfer_to_ik()
    bpy.ops.mcp.simplify_fcurves()
    bpy.ops.graph.simplify(error=0.05)

    #to set start and end frame of animation rendering
    bpy.data.scenes[0].frame_start = 1
    bpy.data.scenes[0].frame_end = 1

    #render_frames is a pointer to end frame  for rendering
    render_frames = bpy.data.scenes[0].frame_end
    bpy.data.scenes[0].frame_step = 1

    #tracking_frames is number of frames for which we want to track coordinates of vertices of mhx2 model
    tracking_frames = render_frames

    #if animation what we need
    if(Animation==True):
        #input for frame per second
        bpy.data.scenes[0].render.fps=args.fps

        #input for video format file
        bpy.data.scenes[0].render.image_settings.file_format = args.videoFormat

        #filepath for output video
        bpy.data.scenes[0].render.filepath = OutputDirPath+person_name+"\\"+bvhFileName
        bpy.context.scene.render.use_overwrite = False

        #rendering
        bpy.ops.render.render(animation=True)
        print("Animated...")

    #if point tracking what we need
    if(point_tracking==True):
            print("point tracking started")
            for f in range(0,tracking_frames):
                    #updating frame number for tracking coordinates of vertices in image space
                    bpy.context.scene.frame_set(f)
                    pointTracking(curr_scn,person_name+":Body",bpy.data.cameras[0].name,f)
    
if __name__ == "__main__":
      
    parser = ArgumentParserForBlender()
    parser.add_argument('--bvhFile',type=str,help='provide bvh file path',required=True)
    parser.add_argument('--mhx2File',type=str,help='provide mhx2 model file path',required=True)
    parser.add_argument('--fps',default=15,type=int,help='Please provide frame rate for Animation(default=15)',required=True)
    parser.add_argument('--videoFormat',default='FFMPEG',help='video format in which animation will be generated(default=FFMPEG)',choices=['FFMPEG','MP4'],required=True)
    parser.add_argument('--Animation',default=False,type=lambda x: (str(x).lower() == 'true'),help='True if you want to get animation video(default False)')
    parser.add_argument('--Point_tracking',default=False,type=lambda x: (str(x).lower() == 'true'),help='True if you want to get point tracking of vertices(default=False)')

    args = parser.parse_args()
    fps = args.fps
    videoFormat =args.videoFormat
    bvhFile = args.bvhFile
    mhx2File =args.mhx2File
    bool_animation = args.Animation
    bool_pointtracking = args.Point_tracking
    print(bool_animation)
    print(bool_pointtracking)
    render_to_video(Animation=bool_animation,point_tracking=bool_pointtracking)