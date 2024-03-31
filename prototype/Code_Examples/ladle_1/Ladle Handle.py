import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_ladle_handle(origin, normal, alignment, relative_height, height, bend_radius, thickness, width):
    """
    This function creates a 3D model of a ladle handle. 
    The ladle handle is modeled as a curved thin box constructed from a joined line and arc

    Parameters:
        origin (Rhino.Geometry.Point3d): the point that defines the handle starting location
        normal (Rhino.Geometry.Vector3d): the direction for the handle to width
        alignment (Rhino.Geometry.Vector3d): the direction for the handle to grow up
        relative_height (float): The relative height of the handle by the body of the ladle
        height (float): the handle height before it starts to curve
        bend_radius (float): the space between the handle's straight part to the curved part
        thickness (float): the thickness of the ladle handle
        width (float): the width of the ladle handle

    Returns: 
        Rhino.Geometry.Brep: 3D model of the ladle handle
    """
    try:
        print("INFO: create_ladle_handle - start", locals())
        # Create a line that defines the straight part of the handle
        line_start_point = origin
        line_end_point = line_start_point + (alignment * height)
        line = rg.Line(line_start_point, line_end_point).ToNurbsCurve()

        # Create an arc that defines the end curve of the handle
        arc_start_pt = line_end_point
        arc_mid_pt = arc_start_pt + (alignment * (bend_radius / 2)) + (normal * bend_radius / 2) # The mid pt is located at the half radius of the arc on both horizontal and vertical axis
        arc_end_pt = arc_start_pt + (normal * bend_radius)
        arc = rg.Arc(arc_start_pt, arc_mid_pt, arc_end_pt).ToNurbsCurve()

        # Join line and arc
        handle_rail = rg.Curve.JoinCurves([line, arc])[0]

        # Create a rectangle that defines the handle section
        sweep_rectangle_plane = rg.Plane(origin, alignment)
        handle_rectangle = rg.Rectangle3d(sweep_rectangle_plane, rg.Interval(-width / 2, width / 2 ), rg.Interval(thickness / 2, - thickness / 2)).ToNurbsCurve()

        # Sweep the rectangle along the handle shape to create the handle
        closed = False
        handle = rg.Brep.CreateFromSweep(handle_rail, handle_rectangle, closed, TOLERANCE)[0]

        print("INFO: create_ladle_handle - return", handle)
        return handle
    except Exception as error:
        print("ERROR: create_ladle_handle  ", "An error occurred:", traceback.format_exc())
        return None

# Parameters
body_normal = rg.Vector3d.ZAxis
ladle_radius = 45

handle_relative_height = 0.5
handle_origin = rg.Point3d(0, ladle_radius, ladle_radius * handle_relative_height)
handle_normal = body_normal.YAxis
handle_alignment = body_normal.ZAxis
handle_height = 300
handle_bend_radius = 70
handle_thickness = 1
handle_width = 10

# Assembling
handle = create_ladle_handle(handle_origin, handle_normal, handle_alignment, handle_relative_height, handle_height, handle_bend_radius, handle_thickness, handle_width)

# Return the created object by placing it in variable a
a = handle
