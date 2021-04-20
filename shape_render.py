import bpy, os, sys
sys.path.append(os.path.dirname(bpy.data.filepath))
from shape_central import *

output_dir = bpy.path.abspath('//') + 'Render-Repo/most_simple_shapes'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
save_code_archive(output_dir)
group_render(output_dir, number_of_renders=10)