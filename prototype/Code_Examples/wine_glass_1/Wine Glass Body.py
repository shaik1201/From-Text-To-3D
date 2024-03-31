import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_wine_glass_body(origin, normal, height, bottom_radius, mid_radius, top_radius, relative_mid_height):
    """
    This function creates a 3D model of a wine glass body.
    The body of the wine glass is modeled as a truncated cone or a goblet. It features a wider bowl at the top that gradually tapers down into a narrower stem towards the base. The bowl itself can be approximated as a portion of a sphere or a paraboloid.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the wine glass body plane
        normal (Rhino.Geometry.Vector3d): the normal of the wine glass body plane
        height (float): the hieght of the body
        bottom_radius (float): the bootom radius of the body
        mid_radius (float): the middle radius of the body
        top_radius (float): the top radius of the body
        relative_mid_height (float): the relative height of the midlle circle along the body

    Return: 
        Rhino.Geometry.Brep: 3D model of the wine glass body
    """
    try:
        print("INFO: wine_glass_body - start", locals())
        # Create plane to locate the body
        plane = rg.Plane(origin, normal)

        # Create the base circle at the bottom of the body
        base_circle = rg.Circle(plane, bottom_radius).ToNurbsCurve()

        # Create circle at the relative middle of the body
        mid_plane = rg.Plane(origin + normal * height * relative_mid_height, normal)
        mid_circle = rg.Circle(mid_plane, mid_radius).ToNurbsCurve()

        # Create the top circle at the top of the body
        top_plane = rg.Plane(origin + normal * height, normal)
        top_circle = rg.Circle(top_plane, top_radius).ToNurbsCurve()

        # Create the body by lofting the circles
        closed = False
        loft = rg.Brep.CreateFromLoft([base_circle, mid_circle, top_circle], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: wine_glass_body - return", loft)
        return loft
    except Exception as error:
        print("ERROR: wine_glass_body ", "An error occurred:", traceback.format_exc())
        return None

# Parameters
base_height = 10
handle_height = 100
handle_radius = 4.5

body_height = 100
body_bottom_radius = handle_radius
body_mid_radius = 40
body_top_radius = 35
body_relative_mid_height = 0.1
body_origin = rg.Point3d(0, 0, base_height + handle_height)
body_normal = rg.Vector3d.ZAxis

# Assembling
wine_glass_body = create_wine_glass_body(body_origin, body_normal, body_height, body_bottom_radius, body_mid_radius, body_top_radius, body_relative_mid_height)

# Return the created object by placing it in variable a
a = wine_glass_body