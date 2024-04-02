import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_kettle_handle(origin, normal, alignment, length, height, thickness):
    """
    Create a 3D model of a kettle handle
    The handle is modeled as a semi-circle or arc
    
    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the handle - center of handle circle
        normal (Rhino.Geometry.Vector3d): normal of handle plane - tangent of handle
        alignmen (Rhino.Geometry.Vector3d): The direction to define the start and end point of the handle in relation to the origin
        length (float): the length of the handle
        height (float): The height of the handle
        thickness (float): The thickness of the handle
    
    Returns:
    Rhino.Geometry.Brep: The created semi cylinder
    """
    try:
        print("INFO: create_kettle_handle - start", locals())
        # Create semi circle
        radius = length/2
        handle_start_point = origin + (alignment * radius)
        handle_end_point = origin - (alignment * radius)
        semi_circle = rg.Arc(handle_start_point, normal, handle_end_point).ToNurbsCurve()
        
        # Scale the semi-circle to create an elongated semi-circle or crescent
        plane = rg.Plane(origin,normal)
        transform = rg.Transform.Scale(plane, 1, 1, height/radius)
        semi_circle.Transform(transform)
        
        # Create a circle at the start of the semi-circle for the thickness
        start_point_plane = rg.Plane(semi_circle.PointAtStart ,semi_circle.TangentAtStart)
        shape_circle = rg.Circle(start_point_plane, thickness/2)
        
        # Sweep the shape circle along the semi-circle to create the handle
        closed = False
        handle = rg.Brep.CreateFromSweep(semi_circle, shape_circle.ToNurbsCurve(), closed , TOLERANCE)[0]
        print("INFO: create_kettle_handle - return", handle)
        return handle
    except Exception as error:
        print("ERROR: create_kettle_handle ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_bottom_radius = 150
body_upper_radius = 120
body_height = 200
body_normal = rg.Vector3d.ZAxis


handle_height = 50
handle_thickness = 20
handle_length = body_upper_radius * 2 - handle_thickness
handle_alignment = body_normal.XAxis
handle_origin = rg.Point3d(0,0,body_height)
handle_normal = body_normal

# Assembling
kettle_handle = create_kettle_handle(handle_origin, handle_normal, handle_alignment, handle_length, handle_height, handle_thickness)

# Return created object by placing it in variable a
a = kettle_handle