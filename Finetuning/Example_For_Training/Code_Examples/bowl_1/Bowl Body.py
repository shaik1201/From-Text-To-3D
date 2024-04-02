import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_bowl_body(origin, normal, bottom_radius, middle_radius, upper_radius, height):
    """
    This function creates a 3D model of a bowl body. 
    The body is modeled as a truncated cone.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the bowl body plane
        normal (Rhino.Geometry.Vector3d): normal of bowl body plane 
        bottom_radius (float): the radius of the bottom of the bowl 
        middle_radius (float): the radius of the middle part of the bowl
        upper_radius (float): the radius of the upper part of the bowl
        height (float): the height of the bowl

    Return: 
        Rhino.Geometry.Brep: 3D model of the bowl body
    """
    try:
        print("INFO: create_bowl_body - start", locals())
        # Create plane to locate the body
        plane = rg.Plane(origin, normal)

        # Create the base circle at the bottom of the bowl
        base_circle = rg.Circle(plane, bottom_radius).ToNurbsCurve()

        # Create circle at the middle of the bowl
        mid_plane = rg.Plane(origin + normal * height/2, normal)
        mid_circle = rg.Circle(mid_plane, middle_radius).ToNurbsCurve()

        # Create the top circle at the top of the bowl
        top_plane = rg.Plane(origin + normal * height, normal)
        top_circle = rg.Circle(top_plane, upper_radius).ToNurbsCurve()

        # Create the bowl by lofting the circles
        closed = False
        bowl = rg.Brep.CreateFromLoft([base_circle, mid_circle, top_circle], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: create_bowl_body - return", bowl)
        return bowl
    except Exception as error:
        print("ERROR: create_bowl_body ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_height = 90
body_bottom_radius = 30
body_middle_radius = 110
body_upper_radius = 140
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

# Assembling
bowl_body = create_bowl_body(body_origin, body_normal, body_bottom_radius, body_middle_radius, body_upper_radius, body_height)

# Return created object by placing it in variable a
a = bowl_body
