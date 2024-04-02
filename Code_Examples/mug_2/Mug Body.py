import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_mug_body(origin, normal, base_radius, middle_radius, rim_radius, height):
    """
    This function creates a 3D model of a mug body. The body is modeled as a cylindrical shape with a curved surface.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the mug body plane
        normal (Rhino.Geometry.Vector3d): normal of mug body plane 
        base_radius (float): the radius of the base of the mug 
        middle_radius (float): the radius of the middle of the mug 
        rim_radius (float): the radius of the rim of the mug 
        height (float): the height of the mug

    Return: 
        Rhino.Geometry.Brep: 3D model of the mug body
    """
    try:
        print("INFO: create_mug_body - start", locals())
        # Create plane to locate the body
        plane = rg.Plane(origin, normal)

        # Create the base, middle and top circles
        base_circle = rg.Circle(plane, base_radius).ToNurbsCurve()
        middle_plane = rg.Plane(plane)
        middle_plane.Translate(plane.Normal*(height/2))
        middle_circle = rg.Circle(middle_plane, middle_radius).ToNurbsCurve()
        top_plane = rg.Plane(plane)
        top_plane.Translate(plane.Normal*height)
        top_circle = rg.Circle(top_plane, rim_radius).ToNurbsCurve()

        # Create the body by lofting the three circles
        closed = False
        mug = rg.Brep.CreateFromLoft([base_circle, middle_circle, top_circle], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: create_mug_body - return", mug)
        return mug
    except Exception as error:
        print("ERROR: create_mug_body ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_height = 100
body_base_radius = 35
body_middle_radius = 60
body_rim_radius = 40
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

# Assembling
mug_body = create_mug_body(body_origin, body_normal, body_base_radius, body_middle_radius, body_rim_radius, body_height)

# Return created object by placing it in variable a
a = mug_body
