import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_soup_plate_body(body_bottom_radius, body_top_radius, body_origin, body_normal, body_height):
    """
    This function creates a 3D model of a soup plate body. 
    The soup plate body is modeled as a curved or sloping sides that extend upward from the base

    Parameters:
        body_origin (Rhino.Geometry.Point3d): the origin of the plate body plane
        body_normal (Rhino.Geometry.Vector3d): the normal of plate body plane
        body_bottom_radius (float): the radius of the base of the plate body
        body_top_radius (float): the radius of the top of the plate body
        body_height (float): the plate's body height

    Return: 
        Rhino.Geometry.Brep: 3D model of the soup plate body
    """
    try:
        print("INFO: create_soup_plate_body - start", locals())
        #create plane to locate the plate body
        body_plane = rg.Plane(body_origin, body_normal)

        #ceate the bottom part of the body
        body_bottom_circle = rg.Circle(body_plane, body_bottom_radius)

        #create the top part of the plate body
        body_top_plane = rg.Plane(body_plane)
        body_top_plane.Translate(body_top_plane.Normal*body_height)
        body_top_circle = rg.Circle(body_top_plane, body_top_radius)

        #create the plate by lofting the three circles
        closed = False
        loft = rg.Brep.CreateFromLoft([body_bottom_circle.ToNurbsCurve(), body_top_circle.ToNurbsCurve()], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: create_soup_plate_body - return", loft)
        return loft 
    except Exception as error:
        print("ERROR: create_soup_plate_body ", "An error occurred:", traceback.format_exc())
        return None

# Parameters
body_bottom_radius = 100
body_top_radius = 145
body_height = 40
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

# Assembling
soup_plate_body = create_soup_plate_body(body_bottom_radius, body_top_radius, body_origin, body_normal, body_height)

# Return the created object by placing it in variable a
a = soup_plate_body
