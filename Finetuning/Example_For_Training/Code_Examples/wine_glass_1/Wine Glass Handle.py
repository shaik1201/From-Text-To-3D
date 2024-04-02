import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_wine_glass_handle(origin, normal, height, radius):
    """
    This function creates a 3D model of a wine glass handle.
    The wine glass handle is modeled as a tall thin cylinder.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the wine glass handle plane
        normal (Rhino.Geometry.Vector3d): the normal of the wine glass handle plane
        height (float): the height of the handle
        radius (float): the thickness of the handle

    Return: 
        Rhino.Geometry.Brep: 3D model of the wine glass handle
    """
    try:
        print("INFO: wine_glass_handle - start", locals())
        # Create a plane to locate the handle
        handle_plane = rg.Plane(origin, normal)

        # Create the base circle of the handle
        bottom_circle = rg.Circle(handle_plane, radius)

        # Create the cylinder that defines the handle shape
        cylinder = rg.Cylinder(bottom_circle, height)
        cap_bottom = False
        cap_top = False
        handle = cylinder.ToBrep(cap_bottom, cap_top)

        print("INFO: wine_glass_handle - return", handle)
        return handle
    except Exception as error:
        print("ERROR: wine_glass_handle ", "An error occurred:", traceback.format_exc())
        return None

# Parameters
body_normal = rg.Vector3d.ZAxis
base_height = 10

handle_height  = 100
handle_radius = 4.5
handle_origin = rg.Point3d(0, 0, base_height)
handle_normal = body_normal

# Assembling
wine_glass_handle = create_wine_glass_handle(handle_origin, handle_normal, handle_height, handle_radius)

# Return the created object by placing it in variable a
a = wine_glass_handle
