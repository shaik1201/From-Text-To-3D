import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_kettle_base(origin, normal, radius):
    """
    This function creates a 3D model of a kettle base. 
    The base is modeled as a circle at the bottom of the kettle.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the kettle base plane
        normal (Rhino.Geometry.Vector3d): normal of kettle base plane 
        radius (float): the radius of the base

    Return: 
        Rhino.Geometry.Brep: the created base
    """
    try:
        print("INFO: create_kettle_base - start", locals())
        # Create plane to locate the base
        plane = rg.Plane(origin, normal)

        # Create the base circle
        base_circle = rg.Circle(plane, radius)
        base = rg.Brep.CreatePlanarBreps(base_circle.ToNurbsCurve(),TOLERANCE)
        
        print("INFO: create_kettle_base - return", base)
        return base
    except Exception as error:
        print("ERROR: create_kettle_base ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_bottom_radius = 75
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_bottom_radius
base_origin = body_origin
base_normal = body_normal

# Assembling
kettle_base = create_kettle_base(base_origin, base_normal, base_radius)

# Return created object by placing it in variable a
a = kettle_base