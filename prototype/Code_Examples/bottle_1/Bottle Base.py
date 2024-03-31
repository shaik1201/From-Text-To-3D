import rhinoinside
rhinoinside.load()

# System and Rhino can only be loaded after rhinoinside is initialized
import Rhino.Geometry as rg  # noqa
import Rhino
import traceback

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_bottle_base(origin, normal, radius):
    """
    This function creates a 3D model of a bottle base. 
    The base is modeled as a circle at the base of the bottle.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the bottle base plane
        normal (Rhino.Geometry.Vector3d): the normal of bottle base plane 
        radius (float): the radius of the base

    Return: 
        Rhino.Geometry.Brep: The created 3D model
    """
    TOLERANCE = 0.01
    try:
        print("INFO: create_bottle_base - start", locals())
        # Create plane to locate the base
        plane = rg.Plane(origin, normal)

        # Create the base surface
        base_circle = rg.Circle(plane, radius)
        base = rg.Brep.CreatePlanarBreps(base_circle.ToNurbsCurve(), TOLERANCE)[0]

        print("INFO: create_bottle_base - return", base)
        return base

    except Exception as error:
        print("ERROR: create_bottle_base ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_bottom_radius = 100
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_bottom_radius
base_origin = body_origin
base_normal = body_normal

# Assembling
bottle_base = create_bottle_base(base_origin, base_normal, base_radius)

# Return created object by placing it in variable a
a = bottle_base