import bpy, os, sys
sys.path.append(os.path.dirname(bpy.data.filepath))
from shape_central import *

output_dir = bpy.path.abspath('//') + 'Render-Repo/SimpleSet'
save_code_archive(output_dir)
group_render(output_dir, number_of_renders=1000)