import rhinoinside
rhinoinside.load()
# System and Rhino can only be loaded after rhinoinside is initialized
import Rhino.Geometry as rg  # noqa
import Rhino
import traceback

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_ellipse_baking_mold_base(origin, normal, width, length):
    """
    This function creates a 3D model of a ellipse baking mold base.
    The base of the mold is modeled as a flat ellipse surface.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the base plane
        normal (Rhino.Geometry.Vector3d): normal of base plane
        length (float): the length of the base
        width (float): the width of the base

    Return:
        Rhino.Geometry.Brep: 3D model of the baking mold base
    """
    TOLERANCE = 0.01

    try:
        print("INFO: create_ellipse_baking_mold_base - start", locals())
        # Create a plane to locate the base
        base_plane = rg.Plane(origin, normal)

        # Create the base ellipse
        base_ellipse = rg.Ellipse(base_plane, length / 2, width / 2).ToNurbsCurve() # The dim input is a radius - divide by 2 = diameter

        # Create the base surface
        base_surface = rg.Brep.CreatePlanarBreps(base_ellipse, TOLERANCE)[0]

        print("INFO: create_ellipse_baking_mold_base - return", base_surface)
        return base_surface

    except Exception as error:
        print("ERROR: create_ellipse_baking_mold_body ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis
body_width = 230
body_length = 280

base_origin = body_origin
base_normal = body_normal.ZAxis
base_width = body_width
base_length = body_length

# Assembling
ellipse_baking_mold_base = create_ellipse_baking_mold_base(base_origin, base_normal, base_length, base_width)

# Return the created object by placing it in variable a
a = ellipse_baking_mold_base