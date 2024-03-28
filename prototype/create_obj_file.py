import rhinoinside
rhinoinside.load()

# System and Rhino can only be loaded after rhinoinside is initialized
# import System  # noqa
import Rhino
import Rhino.Geometry as rg  # noqa
import traceback

from utils import get_file_content
import sys
from io import StringIO
import rhino3dm
import trimesh
import numpy as np
import json

prompt = "" #get from ui
# file_name = run_all_agents(prompt)
try:
    sliders_value = sys.argv[1]
except:
    sliders_value = None
    
# # Define the path to the log file
# log_file_path = "sliders_value.log"

# # Open the log file in append mode and write the value
# with open(log_file_path, "a") as log_file:
#     log_file.write(str(sliders_value) + "\n")
    
generated_code = get_file_content("./", f"bowl.py")
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

combined_brep = geometry[0].Append(geometry[1])

mesh = rg.Mesh.CreateFromBrep(combined_brep)

# Convert Rhino mesh data to Trimesh object
vertices = np.array([[v.X, v.Y, v.Z] for v in mesh.Vertices], dtype=np.float64)
faces = np.array([[f.A, f.B, f.C] for f in mesh.Faces], dtype=np.int32)
tmesh = trimesh.Trimesh(vertices=vertices, faces=faces)

# Save the Trimesh object as a single OBJ file
output_file = "static/models/output_mesh_0.obj"  # Replace with desired filename
tmesh.export(output_file)





# mesh = rg.Mesh.CreateFromBrep(geometry[0])
# # print(len(mesh))

# meshes_trimesh = []
# for rhino_mesh in mesh:
#     # Convert Rhino vertices to numpy array
#     vertices = np.array([[v.X, v.Y, v.Z] for v in rhino_mesh.Vertices], dtype=np.float64)
#     # Convert Rhino faces to numpy array
#     faces = np.array([[f.A, f.B, f.C] for f in rhino_mesh.Faces], dtype=np.int32)
#     tmesh = trimesh.Trimesh(vertices=vertices, faces=faces)
#     meshes_trimesh.append(tmesh)

# # Save each Trimesh object to separate OBJ files
# for i, tmesh in enumerate(meshes_trimesh):
#     output_file = f"static/models/output_mesh_{i}.obj"
#     tmesh.export(output_file)

#how to present the brep in we ui: 
#maybe: https://developer.rhino3d.com/api/rhinocommon/rhino.runtime.commonobject/tojson