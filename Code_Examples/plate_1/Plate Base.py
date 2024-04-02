import rhinoinside
rhinoinside.load()
# System and Rhino can only be loaded after rhinoinside is initialized
import Rhino.Geometry as rg  # noqa
import Rhino
import traceback

print('finished loading rhinoinside')
TOLERANCE = 0.01

def create_plate_base(origin, normal, base_radius):
    """
    This function creates a 3D model of a plate base. 
    The plate base is modeled as a flat surface in a circle shape at the bottom of the plate.

    Parameters:
        base_origin (Rhino.Geometry.Point3d): the origin of the plate base plane
        base_normal (Rhino.Geometry.Vector3d): the normal of the plate base plane
        base_radius (float): the radius of the plate base

    Return: 
        Rhino.Geometry.Brep: 3D model of the plate
    """
    TOLERANCE = 0.01
    try:
        print("INFO: create_plate_base - start", locals())
        # Create a plane to locate the plate base
        base_plane = rg.Plane(origin, normal)

        # Create the plate base
        base_circle = rg.Circle(base_plane, base_radius).ToNurbsCurve()
        plate_base = rg.Brep.CreatePlanarBreps(base_circle, TOLERANCE)[0]

        print("INFO: create_plate_base - return", plate_base)
        return plate_base

    except Exception as error:
        print("ERROR: create_plate_base ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_bottom_radius = 100
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_bottom_radius
base_origin = body_origin
base_normal = body_normal

# Assembling
plate_base = create_plate_base(base_origin, base_normal, base_radius)

# Return the created object by placing it in variable a
a = plate_base
