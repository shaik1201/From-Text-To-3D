import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_measuring_jug_base(origin, normal, radius):
    """
    This function creates a 3D model of a measuring jug base. 
    The measuring jug base is modeled as a flat surface in a circular shape at the bottom of the measuring jug.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the measuring jug base plane
        normal (Rhino.Geometry.Vector3d): the normal of the measuring jug base plane
        radius (float): the radius of the measuring jug base

    Return: 
        Rhino.Geometry.Brep: 3D model of the measuring jug
    """
    try:
        print("INFO: measuring_jug_base - start", locals())
        # Create a plane to locate the measuring jug base
        base_plane = rg.Plane(origin, normal)

        # Create the measuring jug base
        base_circle = rg.Circle(base_plane, radius).ToNurbsCurve()
        measuring_jug_base = rg.Brep.CreatePlanarBreps(base_circle, TOLERANCE)[0]  

        print("INFO: measuring_jug_base - return", measuring_jug_base)
        return measuring_jug_base
    except Exception as error:
        print("ERROR: measuring_jug_base ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis
body_base_radius = 60

base_origin = body_origin 
base_normal = body_normal
base_radius = body_base_radius

# Assembling
measuring_jug_base = create_measuring_jug_base(base_origin, base_normal, base_radius)

# Return the created object by placing it in variable a
a = measuring_jug_base
