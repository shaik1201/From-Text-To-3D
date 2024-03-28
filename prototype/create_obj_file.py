import rhinoinside
rhinoinside.load()
# System and Rhino can only be loaded after rhinoinside is initialized
# import System  # noqa
import Rhino
import Rhino.Geometry as rg  # noqa
import rhino3dm

import traceback
from utils import get_file_content
import sys
from io import StringIO
import trimesh
import numpy as np
import json
import os



prompt = "" #get from ui
# file_name = run_all_agents(prompt)
try:
    sliders_value = sys.argv[1]
except:
    sliders_value = None
    
# Define the path to the log file
log_file_path = "sliders_value.log"

# # Open the log file in append mode and write the value
# with open(log_file_path, "a") as log_file:
#     log_file.write(str(sliders_value) + "\n")

# with open('./FullExamples/baking_mold_1.py', 'r', encoding='utf-8-sig') as f:
#     contents = f.read()
#
# # Re-save the file with the correct encoding and without BOM
# with open('./FullExamples/baking_mold_1.py', 'w', encoding='utf-8') as f:
#     f.write(contents)
    
generated_code = get_file_content("./FullExamples/", f"baking_mold_1.py")
# prefix_code = get_file_content("Utils","prefix_full_program_grasshopper.py") #change to relevant prefix to implement the function create_params(input_list)
# code = f"{prefix_code}\n\n{generated_code}"
code = generated_code
ex_locals = {"sliders_value": json.loads(sliders_value)} if sliders_value else {}

old_stdout = sys.stdout
redirected_output = sys.stdout = StringIO()
exec(code, None, ex_locals)
sys.stdout = old_stdout

# print(redirected_output.getvalue())

geometry = ex_locals['a'] # array of breps
params = ex_locals['b']
num_of_params = len(ex_locals['b'])
result = {
            'params': params,
            'num_of_params': num_of_params
        }
print(json.dumps(result))
# print(geometry)

with open("test.txt", "w") as f:
    f.write(str(geometry))


# mesh = rg.Mesh.CreateFromBrep(geometry[0])
# # print(len(mesh))
#
# meshes_trimesh = []
# for rhino_mesh in mesh:
#     # Convert Rhino vertices to numpy array
#     vertices = np.array([[v.X, v.Y, v.Z] for v in rhino_mesh.Vertices], dtype=np.float64)
#     # Convert Rhino faces to numpy array
#     faces = np.array([[f.A, f.B, f.C] for f in rhino_mesh.Faces], dtype=np.int32)
#     tmesh = trimesh.Trimesh(vertices=vertices, faces=faces)
#     meshes_trimesh.append(tmesh)
#
#
# import os
# # Save each Trimesh object to separate OBJ files
# for i, tmesh in enumerate(meshes_trimesh):
#     output_file = f"static/models/output_mesh_{i}.obj"
#     if os.path.exists(output_file):
#         os.remove(output_file)  # Delete the file if it already exists
#     tmesh.export(output_file)


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