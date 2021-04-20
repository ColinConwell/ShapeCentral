import bpy, os, sys
from importlib import reload
sys.path.append(os.path.dirname(bpy.data.filepath))

import math, random, json, platform, zipfile
import numpy as np
from tqdm import tqdm
from scipy import stats
from glob import glob
from fire import Fire

objects = ['Cube', 'Sphere', 'Cylinder', 'Cone', 'Torus', 'Suzanne']

def object_reset(object):
    bpy.data.objects[object].location = [0, 0, 3.5]
    bpy.data.objects[object].rotation_euler = [0, 0, 0]
    if object == 'Suzanne':
        bpy.data.objects[object].rotation_euler = [0, 0, math.radians(180)]
    #bpy.data.objects[object].data.materials[0] = bpy.data.materials.get('Material')
    #bpy.data.objects[object].data.materials.clear()
    
def object_hide(object):
     bpy.data.objects[object].hide = True
     bpy.data.objects[object].hide_render = True
     
def object_show(object):
     bpy.data.objects[object].hide = False
     bpy.data.objects[object].hide_render = False
     
def object_nudger(object, rotations = 'xyz'):
    bpy.data.objects[object].location[0] = np.random.uniform(-3, 3)
    bpy.data.objects[object].location[1] = np.random.uniform(-3, 3)
    bpy.data.objects[object].location[2] = np.random.uniform(1.5, 5.5)
    if 'x' in rotations:
        bpy.data.objects[object].rotation_euler[0] = math.radians(np.random.randint(0,360))
    if 'y' in rotations:
        bpy.data.objects[object].rotation_euler[1] = math.radians(np.random.randint(0,360))
    if 'z' in rotations:
        bpy.data.objects[object].rotation_euler[2] = math.radians(np.random.randint(0,360))

def object_texturizer(object):
    color = random.sample(['Blue', 'Cyan', 'Green', 'Purple', 'Rust', 'Pink', 'Neon'], 1)[0]
    bpy.data.objects[object].data.materials[0] = bpy.data.materials.get(color)  
    
    texture = random.sample(['NONE', 'CLOUDS', 'VORONOI', 'WOOD', 'MARBLE', 'MUSGRAVE'], 1)[0]
    bpy.data.objects[object].data.materials[0].active_texture = bpy.data.textures['Texture']
    bpy.data.textures['Texture'].type = texture
    
    bpy.data.materials[color].texture_slots[0].scale[0] = np.random.uniform(-10,10)
    bpy.data.materials[color].texture_slots[0].scale[1] = np.random.uniform(-10,10)
    bpy.data.materials[color].texture_slots[0].scale[2] = np.random.uniform(-10,10)
    
    if texture == 'WOOD':
        bpy.data.textures['Texture'].wood_type = random.sample(['BANDS', 'RINGS', 'BANDNOISE', 'RINGNOISE'], 1)[0]
        bpy.data.textures['Texture'].noise_type = random.sample(['SOFT_NOISE', 'HARD_NOISE'], 1)[0]
        bpy.data.textures['Texture'].noise_basis_2 = random.sample(['SIN','SAW','TRI'], 1)[0]
        
    if texture == 'VORONOI':
        #bpy.data.textures['Texture'].weight_1 = np.random.uniform(-2,2)
        bpy.data.textures['Texture'].weight_2 = np.random.uniform(.2,1.2)
        bpy.data.textures['Texture'].weight_3 = np.random.uniform(-2,2)
        bpy.data.textures['Texture'].weight_4 = np.random.uniform(-2,2)
        
    if texture == 'CLOUDS':
        bpy.data.textures['Texture'].noise_type = random.sample(['SOFT_NOISE', 'HARD_NOISE'], 1)[0]
        bpy.data.textures['Texture'].noise_scale = np.random.uniform(0.5,1.5)
    
    if texture == 'MARBLE':
        bpy.data.textures['Texture'].marble_type = random.sample(['SOFT','SHARP','SHARPER'], 1)[0]
        bpy.data.textures['Texture'].noise_basis_2 = random.sample(['SIN','SAW','TRI'], 1)[0]
        bpy.data.textures['Texture'].noise_scale = np.random.uniform(0.5,1.5)
        
    if texture == 'MUSGRAVE':
        bpy.data.textures['Texture'].musgrave_type = 'HYBRID_MULTIFRACTAL'
        #bpy.data.textures['Texture'].noise_intensity = np.random.uniform(0.0,10.0)
        #bpy.data.textures['Texture'].lacunarity = np.random.uniform(0.0,1.0)
        #bpy.data.textures['Texture'].octaves = np.random.uniform(2.5, 3.5)
        #bpy.data.textures['Texture'].octaves = np.random.uniform(0.0,8.0)
        #bpy.data.textures['Texture'].offset = np.random.uniform(0.0,1.0)
        #bpy.data.textures['Texture'].gain = np.random.uniform(0.0,6.0)
    
    return color

def camera_reset(camera_xyz = [0,11,3.5], focal_xyz = [0,0,3.5], rotation_around_focus = [0,0,0]):
    bpy.data.objects['Camera'].location[0:3] = camera_xyz
    bpy.data.objects['FocalEmpty'].location[0:3] = focal_xyz
    bpy.data.objects['FocalEmpty'].rotation_euler[0:3] = rotation_around_focus
    if bpy.data.objects['Camera'].location[2] < bpy.data.objects['FocalEmpty'].location[2]:
        bpy.data.objects['FocalEmpty'].rotation_euler[0:3] = [0,math.radians(180),0]
        
def camera_nudger(radial_gaussian=(11,0.3), theta_gaussian=(0.8, np.pi/2), focal_gaussian = (0,0.2), focal_tilt_gaussian=(0,2)):
    variational_params = locals()
    bpy.data.objects['Camera'].location[0] = np.random.normal(*radial_gaussian) * np.cos(np.random.uniform(*theta_gaussian))
    bpy.data.objects['Camera'].location[1] = np.random.normal(*radial_gaussian) * np.sin(np.random.uniform(*theta_gaussian))
    bpy.data.objects['FocalEmpty'].location[0] = np.random.normal(*focal_gaussian)
    bpy.data.objects['FocalEmpty'].location[1] = np.random.normal(*focal_gaussian)
    bpy.data.objects['FocalEmpty'].location[2] = np.random.normal(bpy.data.objects['FocalEmpty'].location[2], focal_gaussian[1])
    bpy.data.objects['FocalEmpty'].rotation_euler[1] = math.radians(np.random.normal(*focal_tilt_gaussian))
    if bpy.data.objects['Camera'].location[2] < bpy.data.objects['FocalEmpty'].location[2]:
        bpy.data.objects['FocalEmpty'].rotation_euler[0:3] = [0,math.radians(180),0]
    return variational_params

def setup_instance(object):
    for obj in objects:
        object_hide(obj)
    object_show(object)
    object_reset(object)    
    object_nudger(object)
    object_texturizer(object)
    
    scene_params = {'obj_name': bpy.data.objects[object].name,
    'obj_loc': list(bpy.data.objects[object].location), 
    'obj_rot': list(bpy.data.objects[object].rotation_euler),
    'obj_col': bpy.data.objects[object].data.materials[0].name,
    'obj_tex': bpy.data.textures['Texture'].type.title(),
    'cam_loc': list(bpy.data.objects['Camera'].location),
    'focal_point': list(bpy.data.objects['FocalEmpty'].location),
    'focal_tilt': list(bpy.data.objects['FocalEmpty'].rotation_euler)}
    
    return scene_params

def reduced_output_render(rendertype):
    logfile = bpy.path.abspath('//') + 'render.log'
    open(logfile, 'a').close()
    redirect = os.dup(1)
    sys.stdout.flush()
    os.close(1)
    os.open(logfile, os.O_WRONLY)
    if rendertype == "Still":
        bpy.ops.render.render(write_still=True)
    elif rendertype == "Animate":
        bpy.ops.render.render(animation=True)
    os.close(1)
    os.dup(redirect)
    os.close(redirect)

def render_scene(output_name, output_file_name, scene_params, resolution):
    bpy.data.scenes['Scene'].render.resolution_x = resolution
    bpy.data.scenes['Scene'].render.resolution_y = resolution

    bpy.context.scene.render.image_settings.file_format = 'JPEG'
    bpy.context.scene.render.filepath = output_file_name
    bpy.context.scene.frame_set(bpy.context.scene.frame_start)
    reduced_output_render(rendertype = "Still")

    with open(output_file_name + '.json', 'w') as output:
        json.dump(scene_params, output)
        
def save_code_archive(output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if not os.path.exists(bpy.path.abspath('//') + '_GenerativeCode.zip'):
        files = [file for file in os.listdir() if 'blocktower' in file and '.py' in file]
        zipf = zipfile.ZipFile(output_dir + '/_GenerativeCode.zip', 'w', zipfile.ZIP_DEFLATED)
        for file in files:
            zipf.write(file)
        zipf.close()

def group_render(output_dir, number_of_renders=10, resolution=224, **kwargs):
    total_number_of_renders = number_of_renders*len(objects)
    item_counts = {object: 0 for object in objects}
    #total_render_count = 0
    
    with tqdm(total=total_number_of_renders) as pbar:
        pbar.set_description('Rendering ShapeWorld')
        
        for object in objects:
            for number in range(number_of_renders):
                scene_params = setup_instance(object)
                output_name = str(number+1).zfill(5) + object
                output_file_name = os.path.join(output_dir,output_name)
                print(output_file_name)
                if os.path.exists(output_file_name):
                    print('output exists!')
                if not os.path.exists(output_file_name):
                    render_scene(output_name, output_file_name, scene_params, resolution)
                pbar.update(1)
    
    os.remove(bpy.path.abspath('//') + 'render.log')

def fire_arg_parser(args):
    blender_args = args[args.index('--') + 1:]
    save_code_archive(bpy.path.abspath('//') + args[args.index('--output_dir') + 1])
    Fire({'render': group_render}, command=blender_args)