import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_round_baking_mold_base(origin, normal, radius):
    """
    This function creates a 3D model of a round baking mold base. 
    The round baking mold base is modeled as a flat surface in a circular shape at the bottom of the round baking mold.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the round baking mold base plane
        normal (Rhino.Geometry.Vector3d): the normal of the round baking mold base plane
        radius (float): the radius of the round baking mold base

    Return: 
        Rhino.Geometry.Brep: 3D model of the round baking mold base
    """
    try:
        print("INFO: round_baking_mold_base - start", locals())
        # Create a plane to locate the round baking mold base
        base_plane = rg.Plane(origin, normal)

        # Create the round baking mold base
        base_circle = rg.Circle(base_plane, radius).ToNurbsCurve()
        round_baking_mold_base = rg.Brep.CreatePlanarBreps(base_circle, TOLERANCE)[0]  

        print("INFO: round_baking_mold_base - return", round_baking_mold_base)
        return round_baking_mold_base
    except Exception as error:
        print("ERROR: round_baking_mold_base ", "An error occurred:", traceback.format_exc())
        return None

# Parameters
body_radius = 150
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_radius
base_origin = body_origin 
base_normal = body_normal

# Assembling
round_baking_mold_base = create_round_baking_mold_base(base_origin, base_normal, base_radius)

# Return the created object by placing it in variable a
a = round_baking_mold_base
