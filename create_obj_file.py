import rhinoinside
rhinoinside.load()
# System and Rhino can only be loaded after rhinoinside is initialized
# import System  # noqa
import Rhino
import Rhino.Geometry as rg  # noqa

import traceback
from Utils.file_utils import get_file_content
import sys
from io import StringIO
import trimesh
import numpy as np
import json
import os


try:
    sliders_value = sys.argv[1]
except:
    sliders_value = None

if sliders_value:      
    if not isinstance(json.loads(sliders_value), dict):
        prompt = json.loads(sliders_value)
        options = ['box', 'bowl', 'ellipse baking mold', 'plate', 'cup', 'glass',
                'bottle', 'baking mold', 'flower pot', 'hook', 'toothpick dispenser']
        for option in options:
            if option in prompt:
                if option == 'bowl':
                    file_name = 'bowl_2.py'
                    break
                else:
                    name = "_".join(option.split())
                    file_name = f'{name}_1.py'
                    break
        with open("file_name.txt", "w") as f:
            f.write(file_name)
    
with open("file_name.txt", "r") as f:
    file_name = f.read()
    
# file_name = run_all_agents() when the finetuning will be ready and steady this
# will be the function that will be called to run the agents and get the file name
    
generated_code = get_file_content("./Full_Programs/", file_name)
code = generated_code

ex_locals = {"sliders_value": json.loads(sliders_value)} if isinstance(json.loads(sliders_value), dict) else {}

old_stdout = sys.stdout
redirected_output = sys.stdout = StringIO()
exec(code, None, ex_locals)
sys.stdout = old_stdout

geometry = ex_locals['a'] # array of breps
params = ex_locals['b']
num_of_params = len(ex_locals['b'])
result = {
            'params': params,
            'num_of_params': num_of_params
        }
print(json.dumps(result))


# Convert each Brep in the geometry list to mesh and combine them
combined_mesh = rg.Mesh()
for brep in geometry:
    brep_meshes = rg.Mesh.CreateFromBrep(brep)
    for brep_mesh in brep_meshes:
        combined_mesh.Append(brep_mesh)

# Convert the combined mesh into a format that can be used with trimesh
vertices = np.array([[v.X, v.Y, v.Z] for v in combined_mesh.Vertices], dtype=np.float64)
faces = []

for f in combined_mesh.Faces:
    if f.IsTriangle:
        faces.append([f.A, f.B, f.C])
    elif f.IsQuad:
        # Convert quad to two triangles
        faces.append([f.A, f.B, f.C])
        faces.append([f.C, f.D, f.A])

# Now that all faces are guaranteed to be triangles, we can safely create a NumPy array
faces_np = np.array(faces, dtype=np.int32)

# Create a trimesh object from the combined mesh
tmesh = trimesh.Trimesh(vertices=vertices, faces=faces_np)

# Specify the output file path
output_file = "static/models/output_combined_mesh.obj"
# Remove the file if it already exists
if os.path.exists(output_file):
    os.remove(output_file)

# Export the combined mesh to an OBJ file
tmesh.export(output_file)

# Print the path to the exported file or any other relevant information
# print(f"Exported combined mesh to {output_file}")

#how to present the brep in we ui: 
#maybe: https://developer.rhino3d.com/api/rhinocommon/rhino.runtime.commonobject/tojson