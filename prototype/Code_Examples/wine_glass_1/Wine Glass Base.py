import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_wine_glass_base(origin, normal, height, bottom_radius, top_radius):
    """
    This function creates a 3D model of a wine glass base.
    The wine glass base is modeled as a cylindrical plate, transitioning smoothly from a wider bottom to a narrower top.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the wine glass base plane
        normal (Rhino.Geometry.Vector3d): the normal of the wine glass base plane
        height (float): the height of the base
        bottom_radius (float): the bottom radius of the base
        top_radius (float): the top radius of the base

    Return: 
        Rhino.Geometry.Brep: 3D model of the wine glass base
    """
    try:
        print("INFO: wine_glass_base - start", locals())
        # Create a plane to locate the bottom part of the base
        bottom_base_plane = rg.Plane(origin, normal)

        # Create the wide circle at the bottom plane of the base
        base_bottom_circle = rg.Circle(bottom_base_plane, bottom_radius).ToNurbsCurve()

        # Create and move a plane to locate the top part of the base
        top_plane = rg.Plane(origin + normal * height, normal)

        # Create the narrow circle at the top plane of the base
        base_top_circle = rg.Circle(top_plane, top_radius).ToNurbsCurve()

        # Create the base by lofting the two circles
        closed = False
        loft = rg.Brep.CreateFromLoft([base_bottom_circle, base_top_circle], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: wine_glass_base - return", loft)
        return loft
    except Exception as error:
        print("ERROR: wine_glass_base ", "An error occurred:", traceback.format_exc())
        return None

# Parameters
body_normal = rg.Vector3d.ZAxis
handle_radius = 4.5

base_origin = rg.Point3d(0, 0, 0)
base_normal = body_normal
base_height  = 10
base_bottom_radius = 32.5
base_top_radius = handle_radius 

# Assembling
wine_glass_base = create_wine_glass_base(base_origin, base_normal, base_height, base_bottom_radius, base_top_radius)

# Return the created object by placing it in variable a
a = wine_glass_base
