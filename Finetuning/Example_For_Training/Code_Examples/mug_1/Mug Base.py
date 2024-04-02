import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_mug_base(origin, normal, radius):
    """
    This function creates a 3D model of a mug base. 
    The base is modeled as a circle at the base of the mug.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the mug base plane
        normal (Rhino.Geometry.Vector3d): normal of mug base plane 
        radius (float): the radius of the base

    Return: 
        Rhino.Geometry.Circle: the created circle
    """
    try:
        print("INFO: create_mug_base - start", locals())
        # Create plane to locate the base
        plane = rg.Plane(origin, normal)

        # Create the base circle
        base_circle = rg.Circle(plane, radius).ToNurbsCurve()
        base = rg.Brep.CreatePlanarBreps(base_circle,TOLERANCE)[0]
        
        print("INFO: create_mug_base - return", base)
        return base
    except Exception as error:
        print("ERROR: create_mug_base ", "An error occurred:", traceback.format_exc())
        return None
        
# Parameters
body_radius = 75
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_radius
base_origin = body_origin
base_normal = body_normal

# Assembling
mug_base = create_mug_base(base_origin, base_normal, base_radius)

# Return created object by placing it in variable a
a = mug_base