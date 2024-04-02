import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_round_baking_mold_body(origin, normal, height, radius):
    """
    This function creates a 3D model of a baking mold body. 
    The body of the mold is modeled as a hollow cylinder.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the body plane
        normal (Rhino.Geometry.Vector3d): normal of body plane
        height (float): the height of the body
        radius (float): the radius of the body
    Return: 
        Rhino.Geometry.Brep: 3D model of the baking mold body
    """
    try:
        print("INFO: create_round_baking_mold_body - start", locals())
        # Create a plane to locate the body
        body_plane = rg.Plane(origin, normal)

        # Create the base circle of the body
        round_base = rg.Circle(body_plane, radius)

        # Create the cylinder that detrmine the body
        cylinder = rg.Cylinder(round_base, height)
        cap_bottom = False
        cap_top = False
        round_baking_mold_body = cylinder.ToBrep(cap_bottom, cap_top)

        print("INFO: create_round_baking_mold_body - return", round_baking_mold_body)
        return round_baking_mold_body
    except Exception as error:
        print("ERROR: create_round_baking_mold_body ", "An error occurred:", traceback.format_exc())
        return None

# Parameters
body_radius = 150
body_height = 50
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

# Assembling
round_baking_mold_body = create_round_baking_mold_body(body_origin, body_normal, body_height, body_radius)

# Return the created object by placing it in variable a
a = round_baking_mold_body