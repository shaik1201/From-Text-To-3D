import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_soup_plate_rim(rim_bottom_radius, rim_top_radius, rim_origin, rim_normal, rim_height):
    """
    This function creates a 3D model of a soup plate rim. 
    The plate rim is modeled as a curved surface with a circular shape around the body

    Parameters:
        rim_origin (Rhino.Geometry.Point3d): the origin of the soup plate rim plane
        rim_normal (Rhino.Geometry.Vector3d): the normal of the soup plate rim plane
        rim_bottom_radius (float): the radius of the base of the soup plate rim
        rim_top_radius (float): the radius of the top of the soup plate rim
        rim_height (float): the plate's rim height

    Return: 
        Rhino.Geometry.Brep: 3D model of the soup plate rim
    """
    try:
        print("INFO: create_plate_rim - start", locals())
        #create plane to locate the soup plate rim
        rim_plane = rg.Plane(rim_origin, rim_normal)

        #create the bottom part of the rim
        rim_bottom_circle = rg.Circle(rim_plane, rim_bottom_radius)

        #create the top part of the soup plate rim
        rim_top_plane = rg.Plane(rim_plane)
        rim_top_plane.Translate(rim_top_plane.Normal * rim_height)
        rim_top_circle = rg.Circle(rim_top_plane, rim_top_radius)

        #create the soup plate by lofting the two circles
        closed = False
        loft = rg.Brep.CreateFromLoft([rim_bottom_circle.ToNurbsCurve(), rim_top_circle.ToNurbsCurve()], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: create_soup_plate_rim - return", loft)
        return loft 
    except Exception as error:
        print("ERROR: create_soup_plate_rim ", "An error occurred:", traceback.format_exc())
        return None

# Parameters
body_top_radius = 145
body_height = 40
body_normal = rg.Vector3d.ZAxis

rim_bottom_radius = body_top_radius
rim_top_radius = 185
rim_height = 6
rim_origin = rg.Point3d(0, 0, body_height)
rim_normal = body_normal

# Assembling
soup_plate_rim = create_soup_plate_rim(rim_bottom_radius, rim_top_radius, rim_origin, rim_normal, rim_height)

# Return the created object by placing it in variable a
a = soup_plate_rim
