import bpy
import bpy_extras
import os
import csv
import copy
from math import *
import sys
from mathutils import *
import random
import argparse
from bpy_extras.object_utils import world_to_camera_view
from ast import literal_eval as make_tuple


#mapping for different parts of body for vertices point tracking
mapping = {"head"      :         ["DEF-head"],
            "hips"     :         ["DEF-hips"],
            "spine":             ["DEF-spine","DEF-spine-1"],
            "chest":               ["DEF-chest","DEF-chest-1"],
            "neck":                 ["DEF-neck","DEF-jaw","DEF-neck-1"],
            "left-upperArm":        ["DEF-upper_arm.L"],
            "right-upperArm":       ["DEF-upper_arm.R"],
            "breast":               ["DEF-breast.L","DEF-breast.R"],
            "left-thigh":           ["DEF-thigh.L"],
            "left-foot":            ["DEF-foot.L"],
            "left-toe":             ["DEF-toe.L"],
            "right-thigh":          ["DEF-thigh.R"],
            "right-foot":           ["DEF-foot.R"],
            "right-toe":            ["DEF-toe.R"],
            "hand-left":            ["DEF-hand.L"],
            "hand-right":           ["DEF-hand.R"],
            "forearm-left":         ["DEF-forearm.01.L","DEF-forearm.02.L","DEF-forearm.03.L"],
            "forearm-right":        ["DEF-forearm.01.R","DEF-forearm.02.R","DEF-forearm.03.R"],
            "lower-leg-left":       ["DEF-shin.01.L","DEF-shin.02.L","DEF-shin.03.L"],
            "lower-leg-right":      ["DEF-shin.01.R","DEF-shin.02.R","DEF-shin.03.R"],
            "left-palm":            ["DEF-palm_index.L","DEF-palm_middle.L"],
            "right-palm":           ["DEF-palm_index.R","DEF-palm_middle.R"]

}

#path of script
script_path = os.path.dirname(os.path.realpath(__file__))

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


#deleting existing default objects in blender when blender starts first time 
bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.delete(use_global=False)


#function for point tracking
def pointTracking(scene,person_body,scene_camera_name,frame_number):

        # needed to rescale 2d coordinates
        render = scene.render
        res_x = render.resolution_x
        res_y = render.resolution_y
        render_scale = scene.render.resolution_percentage / 100
        render_size = (
            int(scene.render.resolution_x * render_scale),
            int(scene.render.resolution_y * render_scale),
        )

        #objects, person and camera
        obj = bpy.data.objects[person_body]
        cam = bpy.data.objects[scene_camera_name]

        # vertex group items
        total_vg = len(obj.vertex_groups.items())

        #applying only "ARMATURE" modifier for .mhx2 object
        for modifiers in obj.modifiers:
            if modifiers.name != "ARMATURE":
                modifiers.show_render = False
        
        #making a copy of mesh on which modifier applied
        me = obj.to_mesh(scene, True,'RENDER')

        #to find global coordinates of each vertex in mesh
        me.transform(obj.matrix_world)

        #camera referece point for finding 3d coordinates of vertices, 
        # it is assumed that camera location is in front of x-z plane of blender or negative y-axis side  
        # front view of mhx2 person

        camera_location = Vector(make_tuple(camera_loc))
        camera_location = -1*camera_location
        camera_as_reference = camera_location

        tracking_data=[]
        tracking_3D = []
        for key,value in mapping.items():
            for group in value:

                    track_data_per_frame = []
                    track_3D_data_per_frame = []
                    vg_index= obj.vertex_groups[group].index
                    vs = [v for v in me.vertices if (vg_index in [vg.group for vg in v.groups])]
                    #print(vs)
                    vertc = (vert.co for vert in vs)

                    #coords_2d is a list of tuple of format of (3d coords of vertex, pixel coords of vertices)
                    coords_2d = [(coord + camera_as_reference ,   world_to_camera_view(scene, cam, coord)) for coord in vertc]

                    rnd = lambda i: round(i)
                    rnd3 = lambda i: round(i, 3)
                    rnd5 = lambda i: round(i, 5)

                    track_3D_data_per_frame.append(frame_number)
                    track_3D_data_per_frame.append(key)

                    # x, y, d=distance_to_lens
                    track_data_per_frame.append(frame_number)
                    track_data_per_frame.append(key)

                    #print("Vertex_group for:",key)
                    for c in range(len(coords_2d)):
                        #pixel space coords
                        pixel_x = rnd(res_x*coords_2d[c][1][0])
                        pixel_y = rnd(res_y*coords_2d[c][1][1])
                        depth_z = rnd3(coords_2d[c][1][2])

                        #camera reference point coords in 3d
                        X_cord = rnd5(coords_2d[c][0][0])
                        Y_cord  = rnd5(coords_2d[c][0][2])
                        Z_cord = rnd5(coords_2d[c][0][1])

                        track_data_per_frame.append((pixel_x, pixel_y, depth_z))
                        track_3D_data_per_frame.append((X_cord,Y_cord ,Z_cord ))
                  #  print(track_data_per_frame)
            
            tracking_data.append(track_data_per_frame)
            tracking_3D.append(track_3D_data_per_frame)

        outputfile_pixelSpace = "point_tracking_imageSpace"+bvhName+"_"+mhx2Name+".csv"
        outputfile_3DSpace = "point_tracking_3Dspace"+bvhName+"_"+mhx2Name+"_3Dspace"+ ".csv"

        with open(outputfile_pixelSpace,"a") as f1:
            writer1 = csv.writer(f1)
            writer1.writerows(tracking_data)


        with open(outputfile_3DSpace,"a") as f2:
            writer2 = csv.writer(f2)
            writer2.writerows(tracking_3D)
        bpy.data.meshes.remove(me)


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
    backgroundpath =main_path+"/BackgroundImages"
    backgroundImages = getFiles(backgroundpath,".jpg")

    #output directory
    OutputDirPath = main_path+"\\Animation\\"
    
    #for background image of aimation
    for a in bpy.context.screen.areas:
            if a.type == "VIEW_3D":
                break
    a.spaces[0].show_background_images=True

    img = bpy.data.images.load(background_image)
    texture = bpy.data.textures.new("Texture.001","IMAGE")
    bpy.data.worlds['World'].active_texture = texture
    bpy.context.scene.world.texture_slots[0].use_map_horizon=True
    bpy.data.worlds[0].use_sky_paper = True


    curr_scn = bpy.context.scene
    bpy.context.scene.world = bpy.data.worlds[0]
    texture.image=img

    #adding canera for current scene
    bpy.ops.object.camera_add()

    #adding plane for floor and background
    #bpy.ops.mesh.primitive_plane_add()
    #bpy.ops.mesh.primitive_plane_add(rotation=(1.57,0,0))
    # planeMeshList = []
    # for plane in bpy.data.meshes.keys():
    #     if plane[:5]=="Plane":
    #         planeMeshList.append(plane)
    # currPlane = planeMeshList[len(planeMeshList)-2]
    # currWallPlane = planeMeshList[len(planeMeshList)-1]


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
    curr_camera.location = Vector(make_tuple(camera_loc))
    curr_camera.rotation_euler = Euler(make_tuple(camera_rot), 'XYZ')
    curr_camera.scale = Vector((1, 1, 1))

    
    curr_lamp.location = Vector((0.17385, 2.70460, 1.41230))
    curr_lamp.rotation_euler = Euler((0.032093837382793427, 0.0016589768929407, 4.444016933441162), 'XYZ')


    #setting up floor and wall plane
    # curr_floor_level = bpy.data.scenes[0].objects[currPlane]
    # curr_wall_level = bpy.data.scenes[0].objects[currWallPlane]

    # #for floor level
    # curr_floor_level.scale[0] = 10
    # curr_floor_level.scale[1] = 10
    # curr_floor_level.location = Vector((-3.34690,2.45708,-1.281453))

    # #for background wall plane 
    # curr_wall_level.scale[0] = 10
    # curr_wall_level.scale[1] = 10
    # curr_wall_level.location = Vector((-0.31573,5.26044,0.98139))

    # #texture for floor
    # curr_floor_level.active_material = Material
    # curr_floor_level.active_material.diffuse_color =(0.155,0.373,0.400)


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
    file_bvh = file_bvh.replace("\\","/")
    with open(file_bvh,'r') as f:
	    for lines in f:
		    line = f.readline()
		    if(line.split(":")[0]=="Frames"):
			    total_frames = int(line.split(":")[1])
    bvhFileName = file_bvh.split("/")[-1][:-4]
    #frame end is total number of frames present in bvh file

    #To set how many frame do we wanna retarget for the armature out of frame_end 
    if(EndFrame):
        frame_end = EndFrame
        bpy.data.scenes[0].McpEndFrame = frame_end
    else:
        frame_end = total_frames
        bpy.data.scenes[0].McpEndFrame = frame_end

    #importing bvh file and rescaling according to size of mhx2 person object
    bpy.ops.mcp.load_and_retarget(filter_glob = ".bvh",filepath = file_bvh)

    #frame_range is equal to McpEndFrame
    frame_range = bpy.data.objects[person_name].animation_data.action.frame_range[1]

    #for simplyfying f curves 
    #bpy.data.scenes[i].McpShowIK=True
    #bpy.data.scenes[i].McpFkIkArms=False
    #bpy.ops.mcp.transfer_to_ik()
    bpy.ops.mcp.simplify_fcurves()
    bpy.ops.graph.simplify(error=0.05)

    #to set start and end frame of animation rendering
    bpy.data.scenes[0].frame_start = 1
    bpy.data.scenes[0].frame_end = bpy.data.scenes[0].McpEndFrame

    #render_frames is a pointer to end frame  for rendering
    render_frames = bpy.data.scenes[0].frame_end
    bpy.data.scenes[0].frame_step = 1

    #tracking_frames is number of frames for which we want to track coordinates of vertices of mhx2 model
    tracking_frames = render_frames

    #if animation what we need
    if(Animation==True):
        bpy.data.scenes[0].render.fps=args.fps
        bpy.data.scenes[0].render.image_settings.file_format = args.videoFormat
        bpy.data.scenes[0].render.filepath = OutputDirPath+person_name+"\\"+bvhFileName
        bpy.context.scene.render.use_overwrite = False

        #input for frame per second
        if(is_preview==True):
            bpy.data.scenes[0].render.image_settings.file_format = "JPEG"
            image = "C:/Users/Vikram Jain/Documents/GitHub/yoga-pose-estimation/"+person_name+bvhFileName
            bpy.data.scenes[0].render.filepath =image
            bpy.data.scenes[0].render.resolution_x = 1920 #perhaps set resolution in code
            bpy.context.scene.render.resolution_y = 1080
            bpy.ops.render.render(write_still=True)
            os.startfile(image+".jpg")
            want_continue = input("Do You want to continue:")
            if(want_continue=="1"):
                    bpy.ops.render.render(animation=True)
                    print("Animated...")
                    os.remove(image+".jpg")
            else: 
                    print("please change camera location accordingly and re-render")
        else:
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
    
    print("enter")
    parser = ArgumentParserForBlender()
    parser.add_argument('--bvhFile',type=str,help='provide bvh file path',required=True)
    parser.add_argument('--mhx2File',type=str,help='provide mhx2 model file path',required=True)
    parser.add_argument('--fps',default=15,type=int,help='Please provide frame rate for Animation(default=15)',required=True)
    parser.add_argument('--FramesToRetarget',type=int,help="How many frames do you wanna retarget(default=All the frames present in bvh file)")
    parser.add_argument('--videoFormat',default='FFMPEG',help='video format in which animation will be generated(default=FFMPEG)',choices=['FFMPEG','AVI_JPEG','AVI_RAW'],required=True)
    parser.add_argument('--background_image',type=str,help='provide background image for animation',required=True)
    parser.add_argument('--Animation',default=False,type=lambda x: (str(x).lower() == 'true'),help='True if you want to get animation video(default False)')
    parser.add_argument('--Point_tracking',default=False,type=lambda x: (str(x).lower() == 'true'),help='True if you want to get point tracking of vertices(default=False)')
    parser.add_argument('--camera_location',default="(0,-3,0)",help='specify a camera location as in format-(x,y,z),default is (0,-3,0)')
    parser.add_argument('--camera_rotation',default="(1.57,0,6.28)",help='specifify camera rotation as in format(x,y,z) in radians- default is(1.57,0,6.28)')
    parser.add_argument('--is_preview',default=True,type=lambda x: (str(x).lower() == 'true'),help="do you want to visualize for your camera location camera location",required=True)


    args = parser.parse_args()
    bvhFile = args.bvhFile

    bvhName = os.path.join(script_path,bvhFile).split("/")[-1][:-4]
    mhx2File =args.mhx2File

    mhx2Name = os.path.join(script_path,mhx2File).split("/")[-1][:-5].capitalize()
    fps = args.fps
    EndFrame = args.FramesToRetarget
    videoFormat =args.videoFormat
    bool_animation = args.Animation
    bool_pointtracking = args.Point_tracking
    background_image = args.background_image
    is_preview = args.is_preview
    camera_loc = args.camera_location
    camera_rot = args.camera_rotation
    print(bool_animation)
    print(bool_pointtracking)
    render_to_video(Animation=bool_animation,point_tracking=bool_pointtracking)