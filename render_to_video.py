import bpy
import os

mhx2ModelPath = "D:/IITD/Summer_2019/characters/adult_female.mhx2"
bvhFilePath = "D:/IITD/Summer_2019/subject/Subj001_Natarajasana_joints_processed.bvh"
outputDirPath = 'D:/IITD/Summer_2019/blender_scripts/rendered_output/tmp/'


#delete everything
bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.delete(use_global=False)


#import makehuman model
bpy.ops.import_scene.makehuman_mhx2(filepath=mhx2ModelPath)

#retarget it on a .bvh file
bpy.ops.mcp.load_and_retarget(filepath=bvhFilePath)

#toggle to object mode
bpy.ops.object.posemode_toggle()

#add camera and lamp
bpy.ops.object.camera_add(location=(0,-40,20), rotation=(1.3,0,0))
#bpy.ops.object.camera_add(location=(-40,-40,40), rotation=(1,0,-0.785))

bpy.ops.object.lamp_add(type='HEMI', radius=1, location=(0,-10,10))

#bpy.ops.object.lamp_add(type='AREA', radius=1, location=(-10,-10,10))
#bpy.ops.object.lamp_add(type='AREA', radius=1, location=(10,-10,10))
#bpy.ops.object.lamp_add(type='AREA', radius=1, location=(-10,-10,40))
#bpy.ops.object.lamp_add(type='AREA', radius=1, location=(10,-10,40))

#setting this new camera as the scene's camera
bpy.context.scene.camera = bpy.data.objects['Camera']

#render settings
#un-comment following two lines to use GPU rendering

#bpy.context.scene.render.engine = 'CYCLES'
#bpy.context.scene.cycles.device = 'GPU'

bpy.data.scenes[0].frame_start = 1
bpy.data.scenes[0].frame_end = 50
bpy.data.scenes[0].frame_step = 1

bpy.data.scenes[0].render.resolution_x = 1920
bpy.data.scenes[0].render.resolution_y = 1080
bpy.data.scenes[0].render.resolution_percentage = 50

bpy.data.scenes[0].render.use_antialiasing = True
bpy.data.scenes[0].render.antialiasing_samples='8'

bpy.data.scenes[0].render.use_textures=True
bpy.data.scenes[0].render.use_shadows=True
bpy.data.scenes[0].render.use_sss=True
bpy.data.scenes[0].render.use_envmaps=True
bpy.data.scenes[0].render.use_raytrace=True

bpy.data.scenes[0].render.image_settings.file_format='FFMPEG'
bpy.data.scenes[0].render.image_settings.color_mode='RGB'

#specify where to output rendered images
bpy.data.scenes[0].render.filepath = outputDirPath

#render animation frames to .avi
bpy.ops.render.render(animation=True)
