import Rhino
import Rhino.Geometry as rg
import traceback

TOLERANCE = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance

def create_mug_base(origin, normal, radius):
    """
    This function creates a 3D model of a mug base. 
    The base is modeled as a circle at the base of the mug.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the mug base plane
        normal (Rhino.Geometry.Vector3d): normal of mug base plane 
        radius (float): the radius of the base

    Return: 
        Rhino.Geometry.Circle: the created circle
    """
    try:
        print("INFO: create_mug_base - start", locals())
        # Create plane to locate the base
        plane = rg.Plane(origin, normal)

        # Create the base circle
        base_circle = rg.Circle(plane, radius)
        base = rg.Brep.CreatePlanarBreps(base_circle.ToNurbsCurve(), TOLERANCE)
        
        print("INFO: create_mug_base - return", base)
        return base
    except Exception as error:
        print("ERROR: create_mug_base ", "An error occurred:", traceback.format_exc())
        return None

def create_mug_body(origin, normal, base_radius, middle_radius, rim_radius, height):
    """
    This function creates a 3D model of a mug body. 
    The body is modeled as a truncated cone with a curved surface.

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

def create_mug_handle(origin, normal, alignment, height, thickness, relative_angle_at_start):
    """
    Create a 3D model of a mug handle
    The handle is modeled as a C-shaped structure

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the handle - center of handle circle
        normal (Rhino.Geometry.Vector3d): normal of handle plane - tangent of handle
        alignmen (Rhino.Geometry.Vector3d): The direction to define the start and end point of the handle in relation to the origin
        height (float): the height of the handle
        thickness (float): The thickness of the handle
        relative_angle_at_start (float): handle start vector rotation upwards to create a C shape

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

# Generate input sliders by (name,value,min,max)
input_list = [
    InputSlider('body_base_radius', 35, 10, 200),
    InputSlider('body_middle_radius', 60, 10, 200),
    InputSlider('body_rim_radius', 40, 10, 200),
    InputSlider('body_height', 100, 10, 300),
    InputSlider('handle_height', 60, 10, 200),
    InputSlider('handle_thickness', 10, 1, 50),
    InputSlider('handle_relative_height', 0.50, 0.00, 1.00),
    InputSlider('handle_relative_angle_at_start', 0.6, 0.0, 1.0),
]
create_params(input_list)

# User Parameters:
try: body_base_radius
except: body_base_radius = 35

try: body_middle_radius
except: body_middle_radius = 60

try: body_rim_radius
except: body_rim_radius = 40

try: body_height
except: body_height = 100

try: handle_height
except: handle_height = 60

try: handle_thickness
except: handle_thickness = 10

try: handle_relative_height
except: handle_relative_height = 0.5

try: handle_relative_angle_at_start
except: handle_relative_angle_at_start = 0.6

# Internal Parameters:
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_base_radius
base_origin = body_origin
base_normal = body_normal

handle_alignment = body_normal.ZAxis
handle_origin = rg.Point3d(body_middle_radius, 0, body_height * handle_relative_height)
handle_normal = body_normal.XAxis

# Assembling
mug_body = create_mug_body(body_origin, body_normal, body_base_radius, body_middle_radius, body_rim_radius, body_height)
mug_base = create_mug_base(base_origin, base_normal, base_radius)
mug_handle = create_mug_handle(handle_origin, handle_normal, handle_alignment, handle_height, handle_thickness, handle_relative_angle_at_start)

# Return created object by placing it in variable a
a = [mug_base, mug_body, mug_handle]