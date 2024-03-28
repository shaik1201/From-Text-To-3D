from pywavefront import Wavefront
import numpy as np

def obj_to_gcode(obj_file, gcode_file):
    # Load OBJ file
    mesh = Wavefront(obj_file)

    # Open G-code file for writing
    with open(gcode_file, 'w') as f:
        # Iterate through each face in the mesh
        for face in mesh.mesh_list:
            if face.material is not None:
                material = mesh.materials[face.material]
                # Check if material file exists
                if not material.texture.vertices:
                    continue  # Skip faces with missing material
            vertices = np.array(face.vertices)
            # Write G-code commands based on the vertices of each face
            for i in range(0, len(vertices), 3):
                # Example: Move to the first vertex of the triangle
                f.write("G1 X{} Y{} Z{}\n".format(vertices[i][0], vertices[i][1], vertices[i][2]))
                # Example: Draw lines to the other two vertices of the triangle
                f.write("G1 X{} Y{} Z{}\n".format(vertices[i+1][0], vertices[i+1][1], vertices[i+1][2]))
                f.write("G1 X{} Y{} Z{}\n".format(vertices[i+2][0], vertices[i+2][1], vertices[i+2][2]))

# Example usage
obj_file = './box.obj'
gcode_file = './output.gcode'
obj_to_gcode(obj_file, gcode_file)
