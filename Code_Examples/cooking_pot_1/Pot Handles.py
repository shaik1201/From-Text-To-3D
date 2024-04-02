import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_pot_handle(origin, normal, alignment, radius, thickness):
    """
    Create a 3D model of a pot handle
    The handle is modeled as a slightly elongated semi-circle or crescent

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the shape
        normal (Rhino.Geometry.Vector3d): normal of the shape
        alignmen (Rhino.Geometry.Vector3d): The direction to define the start and end point of the semi circle
        radius (float): the radius of the shape
        thickness (float): The thickness of the pipe

    Returns:
    Rhino.Geometry.Brep: The created pipe
    """
    try:
        print("INFO: create_pot_handle - start", locals())
        # Create arc
        start_point = origin + (alignment * radius)
        end_point = origin - (alignment * radius)
        semi_circle = rg.Arc(start_point, normal, end_point).ToNurbsCurve()

        # Create a circle at the start of the semi-circle for the thickness
        start_point_plane = rg.Plane(semi_circle.PointAtStart, semi_circle.TangentAtStart)
        shape_circle = rg.Circle(start_point_plane, thickness/2)

        # Sweep the shape circle along the semi-circle
        closed = False
        pipe = rg.Brep.CreateFromSweep(semi_circle, shape_circle.ToNurbsCurve(), closed, TOLERANCE)[0]
        print("INFO: create_pot_handle - return", pipe)
        return pipe
    except Exception as error:
        print("ERROR: create_pot_handle ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_radius = 150
body_height = 130
body_normal = rg.Vector3d.ZAxis

handle_radius = 30
handle_thickness = 20
handle_relative_height = 0.9
handle_alignment = body_normal.YAxis
right_handle_origin = rg.Point3d(body_radius,0, body_height * handle_relative_height)
right_handle_normal = body_normal.XAxis
left_handle_origin = rg.Point3d(-body_radius,0, body_height * handle_relative_height)
left_handle_normal = -body_normal.XAxis

# Assembling
pot_right_handle = create_pot_handle(right_handle_origin, right_handle_normal, handle_alignment, handle_radius, handle_thickness)
pot_left_handle = create_pot_handle(left_handle_origin, left_handle_normal, handle_alignment, handle_radius, handle_thickness)

# Return created object by placing it in variable a
a = pot_right_handle, pot_left_handle