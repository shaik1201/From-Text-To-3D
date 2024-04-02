import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_mug_handle(origin, normal, alignment, height, thickness, relative_angle_at_start):
    """
    Create a 3D model of a mug handle
    The handle is modeled as a C-shaped structure

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the handle - center of handle circle
        normal (Rhino.Geometry.Vector3d): normal of handle plane - tangent of handle
        alignmen (Rhino.Geometry.Vector3d): The direction to define the start and end point of the handle in relation to the origin
        height (float): the height of the handle
        relative_angle_at_start (float): handle start vector rotation upwards to create a C shape
        thickness (float): The thickness of the handle

    Returns:
    Rhino.Geometry.Brep: The created semi cylinder
    """
    try:
        print("INFO: create_mug_handle - start", locals())
        # Create semi circle
        radius = height/2
        handle_start_point = origin + (alignment * radius)
        handle_end_point = origin - (alignment * radius)
        start_point_normal = normal + rg.Vector3d.ZAxis * relative_angle_at_start
        semi_circle = rg.Arc(handle_start_point, start_point_normal, handle_end_point).ToNurbsCurve()

        # Create a circle at the start of the semi-circle for the thickness
        start_point_plane = rg.Plane(semi_circle.PointAtStart, semi_circle.TangentAtStart)
        shape_circle = rg.Circle(start_point_plane, thickness/2)

        # Sweep the shape circle along the semi-circle to create the handle
        closed = False
        handle = rg.Brep.CreateFromSweep(semi_circle, shape_circle.ToNurbsCurve(), closed, TOLERANCE)[0]
        print("INFO: create_mug_handle - return", handle)
        return handle
    except Exception as error:
        print("ERROR: create_mug_handle ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_height = 100
body_middle_radius = 50
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

handle_height = 60
handle_thickness = 10
handle_relative_height = 0.5
handle_relative_angle_at_start = 0.6
handle_alignment = body_normal.ZAxis
handle_origin = rg.Point3d(body_middle_radius, 0, body_height * handle_relative_height)
handle_normal = body_normal.XAxis

# Assembling
mug_handle = create_mug_handle(handle_origin, handle_normal, handle_alignment, handle_height, handle_thickness, handle_relative_angle_at_start)

# Return created object by placing it in variable a
a = mug_handle
