import rhinoinside
rhinoinside.load()
import Rhino.Geometry as rg
import traceback

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_ellipse_baking_mold_body(origin, normal, width, length, height):
    """
    This function creates a 3D model of a ellipse baking mold body. 
    The body of the mold is modeled as an extruded ellipse.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the body plane
        normal (Rhino.Geometry.Vector3d): normal of body plane
        length (float): the length of the body 
        width (float): the width of the body
        height (float): the height of the body

    Return: 
        Rhino.Geometry.Brep: 3D model of the baking mold body
    """
    TOLERANCE = 0.01

    try:
        print("INFO: create_ellipse_baking_mold_body - start", locals())
        # Create a plane to locate the body
        body_plane = rg.Plane(origin, normal)

        # Create the base of the body - the bottom ellipse
        bottom_ellipse = rg.Ellipse(body_plane, length / 2, width / 2).ToNurbsCurve() # The dim input is a radius - divide by 2 = diameter

        # Create the body - the extrusion of the ellipse
        ellipse_body = rg.Extrusion.CreateExtrusion(bottom_ellipse, normal * height).ToBrep()

        print("INFO: create_ellipse_baking_mold_body - return", ellipse_body)
        return ellipse_body
    except Exception as error:
        print("ERROR: create_ellipse_baking_mold_body ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis
body_width = 230
body_length = 280
body_height = 50

# Assembling
ellipse_baking_mold_body = create_ellipse_baking_mold_body(body_origin, body_normal, body_length, body_width, body_height)

# Return the created object by placing it in variable a
a = ellipse_baking_mold_body