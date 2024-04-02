import rhinoinside
rhinoinside.load()
# System and Rhino can only be loaded after rhinoinside is initialized
import Rhino.Geometry as rg  # noqa
import Rhino
import traceback

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_ellipse_baking_mold_rim(origin, normal, width, length, height, alignment, thickness):
    """
    This function creates a 3D model of a ellipse baking mold rim. 
    The rim of the mold is modeled a pipe cut vertically in the shape of an ellipse.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the rim plane
        normal (Rhino.Geometry.Vector3d): the normal of the rim plane
        alignment (Rhino.Geometry.Vector3d): the direction in which the rim expands
        height (float): the height of the rim
        thickness (float): the thickness of the rim
        length (float): the length of the ellipse 
        width (float): the width of the ellipse 

    Return: 
        Rhino.Geometry.Brep: 3D model of the baking mold rim
    """
    TOLERANCE = 0.01

    try:
        print("INFO: create_ellipse_baking_mold_rim - start", locals())
        if thickness == 0 or height == 0:  # No rim option
            return None
        # Create a plane to locate the rim
        rim_plane = rg.Plane(origin, alignment)

        # Create an ellipse at the top of the rim

        top_ellipse = rg.Ellipse(rim_plane, length / 2,
                                 width / 2).ToNurbsCurve()  # The input is a radius -> divided by 2 = diameter

        # Determining an arc section for sweeping
        start_pt = origin + (normal * length / 2)  # From the center of the ellipse to the edge
        end_pt = start_pt - (alignment * height)
        mid_pt = start_pt - (alignment * height) / 2 + (normal * thickness)
        arc = rg.Arc(start_pt, mid_pt, end_pt).ToNurbsCurve()

        # Sweep the arc along the ellipse shape to create the rim
        closed = False
        rim = rg.Brep.CreateFromSweep(top_ellipse, arc, closed, TOLERANCE)[0]

        print("INFO: create_ellipse_baking_mold_rim - return", rim)
        return rim

    except Exception as error:
        print("ERROR: create_ellipse_baking_mold_rim ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_height = 50
body_width = 230
body_length = 280
body_normal = rg.Vector3d.ZAxis

rim_ellipse_width = body_width
rim_ellipse_length = body_length
rim_origin = rg.Point3d(0, 0, body_height)
rim_normal = rg.Vector3d.XAxis # The 'sweep' works well when using this axis
rim_alignment = body_normal.ZAxis
rim_height = 6
rim_thickness = 3

# Assembling
ellipse_baking_mold_rim = create_ellipse_baking_mold_rim(rim_origin, rim_normal, rim_ellipse_length, rim_ellipse_width, rim_height, rim_alignment, rim_thickness)

# Return the created object by placing it in variable a
a = ellipse_baking_mold_rim