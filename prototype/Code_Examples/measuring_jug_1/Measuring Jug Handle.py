import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_measuring_jug_handle(origin, normal, alignment, top_face_length, side_face_length, thickness, width):
    """
    Create a 3D model of a measuring jug handle
    The handle is modeled a flipped L-shaped structure, sits directly opposite to the spout's direction

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the measuring jug body plane
        normal (Rhino.Geometry.Vector3d): the normal of measuring jug body plane
        alignment (Rhino.Geometry.Vector3d): the axis in which the spout and the handle located
        top_face_length (float): the length of the top part of the handle
        side_face_length (float): the length of the bottom part of the handle
        thickness (float): the thickness of the handle
        width (float): the width of the handle

    Returns:
    Rhino.Geometry.Brep: The created The created measuring jug handle
    """
    try:
        print("INFO: create_measuring_jug_handle - start", locals())
        # Generate a series of points to create a polyline that represent the handle L shape
        polyline_start_pt = origin
        polyline_middle_pt = polyline_start_pt + (normal * top_face_length)
        polyline_end_pt = polyline_middle_pt + (alignment * side_face_length)
        polyline_pts = polyline_start_pt, polyline_middle_pt, polyline_end_pt

        # Create the polyline that represents the handle L shape and will be used as a rail for sweeping.
        polyline_rail = rg.Polyline(polyline_pts).ToNurbsCurve()

        # Create a rectangle that defines the handle section
        sweep_rectangle_plane = rg.Plane(origin, normal)
        handle_rectangle = rg.Rectangle3d(sweep_rectangle_plane, rg.Interval(thickness / 2, - thickness / 2), rg.Interval(-width / 2, width / 2 )).ToNurbsCurve()

        # Sweep the rectangle along the handle shape to create the handle
        closed = False
        handle = rg.Brep.CreateFromSweep(polyline_rail, handle_rectangle, closed, TOLERANCE)[0]

        print("INFO: create_measuring_jug_handle - return", handle)
        return handle
    except Exception as error:
        print("ERROR: create_measuring_jug_handle ", "An error occurred:", traceback.format_exc())
        return None

# Parameters
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis
body_alignment = rg.Vector3d.YAxis
body_height = 100
body_top_radius = 70

handle_thickness = 2
handle_origin = rg.Point3d(0, -body_top_radius, body_height-handle_thickness/2)
handle_normal = -body_normal.YAxis
handle_alignment = -body_normal.ZAxis
handle_top_face_length = 20
handle_side_face_length = 70
handle_width = 20

# Assembling
measuring_jug_handle = create_measuring_jug_handle(handle_origin, handle_normal, handle_alignment, handle_top_face_length, handle_side_face_length, handle_thickness, handle_width)

# Return created object by placing it in variable a
a = measuring_jug_handle