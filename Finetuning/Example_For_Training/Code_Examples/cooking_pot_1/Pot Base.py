import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_pot_base(origin, normal, radius):
    """
    This function creates a 3D model of a pot base. 
    The base is modeled as a circle at the base of the pot.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the pot base plane
        normal (Rhino.Geometry.Vector3d): normal of pot base plane 
        radius (float): the radius of the base

    Return: 
        Rhino.Geometry.Circle: the created circle
    """
    try:
        print("INFO: create_pot_base - start", locals())
        # Create plane to locate the base
        plane = rg.Plane(origin, normal)

        # Create the base circle
        base_circle = rg.Circle(plane, radius)
        base = rg.Brep.CreatePlanarBreps(base_circle.ToNurbsCurve(),TOLERANCE)
        
        print("INFO: create_pot_base - return", base)
        return base
    except Exception as error:
        print("ERROR: create_pot_base ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_radius = 150
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_radius
base_origin = body_origin
base_normal = body_normal

# Assembling
pot_base = create_pot_base(base_origin, base_normal, base_radius)

# Return created object by placing it in variable a
a = pot_base